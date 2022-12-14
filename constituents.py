import json
from math import exp, log, sqrt

from market_data import get_market_data
from config import constituents_amount, constituents_file, default_ratio, pairing, reselect_constituents

def calculate_weights():
    if reselect_constituents:
        coin_ids = None
    else:
        try:
            with open(constituents_file) as f:
                coin_ids = json.load(f)
        except FileNotFoundError:
            coin_ids = None

    market_data = get_market_data(coin_ids)
    adjusted_market_caps = {c: _ewma(m['market_caps']) for (c, m) in market_data.items()}
    adjusted_market_caps = dict(sorted(adjusted_market_caps.items(), key=lambda i: i[1], reverse=True)[:constituents_amount])

    with open(constituents_file, 'w') as f:
        json.dump(list(adjusted_market_caps.keys()), f)

    weights = _constituents_weights(adjusted_market_caps)
    def_ratio = default_ratio if pairing not in [market_data[c]['symbol'] for c in weights] else 0

    return {**{pairing: def_ratio}, **{market_data[c]['symbol']: (1 - def_ratio) * w for (c, w) in weights.items()}}


def _ewma(series, half_life=3):
    decay_rate = log(2) / half_life

    return sum([market_cap * exp(- decay_rate * i) for i, market_cap in enumerate(series)]) / \
        sum([exp(- decay_rate * i) for i in range(len(series))])


def _constituents_weights(adjusted_market_caps):
    sqrt_adjusted_market_caps = {coin_id: sqrt(adjusted_market_cap) for (coin_id, adjusted_market_cap) in adjusted_market_caps.items()}
    sqrt_adjusted_market_caps_sum = sum(sqrt_adjusted_market_caps.values())

    return {coin_id: sqrt_adjusted_market_cap / sqrt_adjusted_market_caps_sum for (coin_id, sqrt_adjusted_market_cap) in sqrt_adjusted_market_caps.items()}
