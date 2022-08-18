
import websocket , json , talib
import numpy as np
from binance.client import Client
from binance.enums import * 
from tradingview_ta import TA_Handler, Interval



api_key = 'input your API key here.'
api_secret = 'input your API secret here.'
client = Client(api_key,api_secret)



closes = []
RSI_PERIOD = 6
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
symbol = 'BTCUSDT'
perp = 'PERP'
TRADE_QTY = 0.001
in_pos_long, in_pos_short = False, False

def create_order(side, positionSide, quantity, symbol, order_type = ORDER_TYPE_MARKET ):
    try:
        order = client.futures_create_order(symbol = symbol, side = side, positionSide = positionSide, type = order_type, quantity = quantity)
        print(order)
    except Exception as e:
        return False 
    return True

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_pos_long, in_pos_short
    js_message = json.loads(message)

    candle = js_message['k']
    is_candle_closed = candle['x']
    close = float(candle['c'])

    if is_candle_closed:
        print('candle closed at {}'.format(close))
        closes.append(close)

        output = TA_Handler(screener = 'Crypto', exchange = 'Binance', symbol = 'BTCUSDTPERP', interval=Interval.INTERVAL_5_MINUTES)
        bb_lower = output.get_analysis().indicators['BB.lower']
        bb_upper = output.get_analysis().indicators['BB.upper']

        if len(closes) > RSI_PERIOD:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, 6)
            last_rsi = rsi[-1]
            print(rsi)
            print('the current rsi is {}'.format(last_rsi))

            if not in_pos_long:
                if last_rsi < RSI_OVERSOLD and close < bb_lower and not in_pos_short:
                    print('----------------BUY LONG !!!----------------')
                    order_long = create_order('BUY','LONG', TRADE_QTY, symbol)
                    if order_long:
                        in_pos_long = True
                elif last_rsi < RSI_OVERSOLD and close < bb_lower and in_pos_short:
                    print('----------------SELL SHORT AND BUY LONG !!!----------------')
                    order_short = create_order('BUY', 'SHORT', TRADE_QTY, symbol)
                    if order_short:
                        in_pos_short = False

                    order_long = create_order('BUY', 'LONG', TRADE_QTY, symbol)
                    if order_long:
                        in_pos_long = True

            elif not in_pos_short:
                if last_rsi > RSI_OVERBOUGHT and close > bb_upper and not in_pos_long:
                    print('----------------BUY SHORT !!!----------------')
                    order_short = create_order('SELL', 'SHORT',TRADE_QTY, symbol)
                    if order_short:
                        in_pos_short = True
                if last_rsi > RSI_OVERBOUGHT and close > bb_upper and in_pos_long:
                    print('----------------SELL LONG AND BUY SHORT !!!----------------')
                    order_long = create_order('SELL', 'LONG', TRADE_QTY, symbol)
                    if order_long:
                        in_pos_long = False
                    
                    order_short = create_order('SELL', 'SHORT', TRADE_QTY, symbol)
                    if order_short:
                        in_pos_short = True



            

            

    
ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@kline_5m", on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()