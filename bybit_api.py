from config import pairing
from auth import session_auth

def get_balances():
    res = session_auth.get_wallet_balance()

    balances = {}
    for item in res['result']['balances']:
        quantity = float(item['free'])
        if quantity > 0:
            balances[item['coin']] = quantity

    return balances

def get_exchange_minqtyize(symbol):
    data = session_auth.query_symbol()['result']
    for sym_data in data:
        if sym_data['name'] == symbol:
            return float(sym_data['minTradeQuantity'])

def get_price(symbol):
    try:
        return float(session_auth.last_traded_price(symbol=(f'{symbol}{pairing}'))['result']['price'])
    except KeyError:
        return None

def create_order(symbol, side, quantity):
    return session_auth.place_active_order(symbol=(f'{symbol}'), side=side, type='Market', qty=quantity, time_in_force='GoodTillCancel')
