# Stock_Bot
### Utilizes tradingview.com alerts and webhooks
### Algorithms used:
* Short and long
* Stochastic algorithm (18 day lookback)
* HMA(Hull Moving Average) (250 day lookback)
* SMA(Simple Moving Average) (50 day lookback, 1 hour timeframe)
* ADX (filter 20)
* Volume filtering
* Stop loss/takeprofit with trailing trigger for both short and long
###### this is my second python project
###### this code is deployed using aws chalice
###### listens tradingview alerts and turns it into a api call and passes on
###### posts live trades via webhook
