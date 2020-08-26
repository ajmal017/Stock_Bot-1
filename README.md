# Stock_Bot
### Algorithms are not included in this code, use public ones or create your own
### Algorithms written using tradingview.com pinescript
### Algorithms i used for testing:
* Short and long
* Stochastic algorithm (18 day lookback)
* HMA(Hull Moving Average) (250 day lookback)
* SMA(Simple Moving Average) (50 day lookback, 1 hour timeframe)
* ADX (filter 20)
* Volume filtering
* Stop loss/takeprofit with trailing trigger for both short and long
### Usage:
Simply deploy this code via aws chalice and copy the address into your tradingview.com webhook alert
Change the Alpcaca credentials to your own

##### this is my second python project
##### this code is deployed using aws chalice
##### listens tradingview alerts and turns it into a api call and passes to a broker api
##### posts live trades via webhook
