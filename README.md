# Trading_Bot
A live trading bot with Binance API, using RSI6 and Bollingers Band indicators.

## Setup
* Install required packages in requirements.txt.
* Create API Key on Binance and allow trading spot & futures.
* Input api_key and api_secret.
* Select cryptocurrency you want to trade (BTC/USDT, ETH/USDT,...).
* Set the timeframe (1m, 5m, 15m, 1h, 4h, 1d,...): 
  + websocket link: "wss://stream.binance.com:9443/ws/{symbol}@kline_{timeframe}"
  + TA_Handler(screener = ..., exchange = ..., symbol = {symbol}, interval = Interval.{Choose timeframe same as timeframe at the link}
* Set TRADE_QTY (suitable with your account balance).
* Run the program.

## Running the program
Run cryptobot_RSI6&BB.py file.

## Back-testing
### Setup
* Input: client.get_historical_klines('input symbol', client.{choose timeframe}, "period")
* Run RSI6&BB.ipynb file.

## Note:
* RSI6&BB.ipynb calculate RSI6 and Bollingers Band by given formulas as cryptobot_RSI6&BB.py calculate them through available libraries (talib). Therefore, the output is not identical in some cases but the order is still hit.
* MAKE SURE YOU HAVE A BINANCE ACCOUNT AND CREATE API TO GET THIS BOT WORKING.




PS: i ran this and now i'm no way home.
