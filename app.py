import alpaca_trade_api
import json
import requests
import pytz
from chalice import Chalice
from dhooks import Webhook
from datetime import datetime

# Configs
hook = Webhook("https://discordapp.com/api/webhooks/734768699973828618/aaWXsr1s2AMuWNxTxM_eruEc5363IasVGpWLlnuMxUasjIJ3QW0gjJpbs4JZ_6muccY8")  # webhook that we are using to post live trades
app = Chalice(app_name='api')  # define app
API_KEY = 'PKK07DKWLSMOYWIURAB7'  # alpaca api key used for authentication
SECRET_KEY = 'SCOTFmPXt4XPCTI7VwxNwyw5LhC6k1PzRLJKxlif'  # alpaca secret key used for authentication
BASE_URL = "https://paper-api.alpaca.markets"  # alpaca url that we are using to post data to
ORDERS_URL = "https://paper-api.alpaca.markets/v2/orders"  # alpaca url that we are using to post data to
POSITIONS_URL = "https://paper-api.alpaca.markets/v2/positions"  # alpaca url that we are using to post data to
ASSETS_URL = "https://paper-api.alpaca.markets/v2/assets"  # alpaca url that we are using to post data to
ACCOUNT_URL = "https://paper-api.alpaca.markets/v2/account"  # alpaca url that we are using to post data to
HISTORY_URL = "https://paper-api.alpaca.markets/v2/account/portfolio/history"  # alpaca url that we are using to post data to
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}  # headers that contains our keys
STARTING_BALANCE = 12500  # starting equity
STOCKS = 2  # enter the amount of stocks we are currently trading

# Api verification
api = alpaca_trade_api.REST(
    key_id=API_KEY,
    secret_key=SECRET_KEY,
    base_url=BASE_URL
)



# Default route
# Values needed:
# "side": ""
# "symbol": ""
# "price":
@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    # removes the too board except warning
    # noinspection PyBroadException
    try:
        account = api.get_account()  # get account
        request = app.current_request  # get current request
        wh_message = request.json_body  # get json body and bind it to wh message
        GMT = pytz.timezone('Europe/Helsinki')  # timezone
        now = datetime.now(tz=GMT)  # get current time
        current_time = now.strftime("%H:%M:%S")  # format time to HH:MM:SS
        symbol = wh_message['symbol']  # get symbol from webhook message (stock name)
        side = wh_message['side']  # get side from webhook message (either long entry / long stop loss / long take profit | short entry / short stop loss / short take profit)
        symbol_bars = api.get_barset(symbol, 'minute', 1).df.iloc[0]  # get live price from alpaca
        symbol_price = symbol_bars[symbol]['close']  # get live price from alpaca
        quantity = round(((float(account.buying_power) / float(wh_message['price'])) / STOCKS) * 0.97)  # divide current available buying power with price of the stock divide that by the amount of possible stocks we are currently buying and finally multiply it by 0.97 this calculation will calculate how many stocks we can buy with 0.97% of our total equity
        balance_change = float(account.equity) - float(account.last_equity)  # compares current equity to yesterdays equity to get the daily profit margin
        total_profit = float(account.equity) - STARTING_BALANCE  # compares current equity to starting balance to get the total profit margin
        total_percentage = 100 * ((float(account.equity) - float(STARTING_BALANCE)) / float(STARTING_BALANCE))   # calculates the total percentage gain
        today_percentage = 100 * ((float(account.equity) - float(account.last_equity)) / float(account.last_equity))   # calculates the daily percentage gain
        total_price = float(symbol_price) * float(quantity)   # calculates the total price of current order
    except Exception:
        hook.send("```fix" + "\n" +
                  "error occurred" + "\n" +
                  "```")
        return

    # LONG ENTRY
    # LONG ENTRY
    # LONG ENTRY
    if side == 'long entry':
        data = {  # json data we are posting to the api
            "symbol": symbol,
            "qty": str(quantity),
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc"
        }
        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)  # post the json data
        response = json.loads(r.content)  # get the response
        print(response)  # print the response
        # noinspection PyBroadException
        try:
            hook.send("```diff" + "\n" +
                      "+ " + "[OPENING TRADE]" + "\n" +
                      "+ " + "{" + current_time + "}" + "\n" +
                      "+ " + "Stock: " + response['symbol'] + "\n" +
                      "+ " + "Asset: " + response['asset_class'] + "\n" +
                      "+ " + "Type: " + wh_message['side'] + "\n" +
                      "+ " + "Price: " + '$' + str(symbol_price) + "\n" +
                      "+ " + "Quantity: " + response['qty'] + "\n" +
                      "+ " + str('Total Price: ' + '$-{:,.2f}'.format(float(total_price))) + "\n" +
                      "+ " + str('Current Available Funds: ' + '${:,.2f}'.format(float(account.equity))) + "\n" +
                      "+ " + str('Current Available Buying Power: ' + '${:,.2f}'.format(float(account.buying_power))) + "\n" +
                      "+ " + str('Today\'s Profit: ' + '${:,.2f}'.format(float(balance_change)) + " (" + '{:.2f}%'.format(float(today_percentage)) + ")") + "\n" +
                      "+ " + str('Total Profit: ' + '${:,.2f}'.format(float(total_profit)) + " (" + '{:.2f}%'.format(float(total_percentage)) + ")") + "\n" +
                      "+ " + "ID: " + response['id'] + "\n" +
                      "+ " + "Status: " + response['status'] + "\n" +
                      "```")
        except Exception:
            hook.send("```fix" + "\n" +
                      "X " + "[OPENING TRADE, ERROR OCCURRED]" + "\n" +
                      "X " + "{" + current_time + "}" + "\n" +
                      "X " + "Stock: " + wh_message['symbol'] + "\n" +
                      "X " + "Quantity: " + str(quantity) + "\n" +
                      "X " + "Error: " + response['message'] + "\n" +
                      "```")

    # SHORT ENTRY
    # SHORT ENTRY
    # SHORT ENTRY
    if side == 'short entry':
        data = {  # json data we are posting to the api
            "symbol": symbol,
            "qty": str(quantity),
            "side": "sell",
            "type": 'market',
            "time_in_force": 'gtc'
        }
        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)  # post the json data
        response = json.loads(r.content)  # get the response
        print(response)  # print the response
        # noinspection PyBroadException
        try:
            hook.send("```diff" + "\n" +
                      "+ " + "[OPENING TRADE]" + "\n" +
                      "+ " + "{" + current_time + "}" + "\n" +
                      "+ " + "Stock: " + response['symbol'] + "\n" +
                      "+ " + "Asset: " + response['asset_class'] + "\n" +
                      "+ " + "Type: " + wh_message['side'] + "\n" +
                      "+ " + "Price: " + '$' + str(symbol_price) + "\n" +
                      "+ " + "Quantity: " + response['qty'] + "\n" +
                      "+ " + str('Total Price: ' + '$-{:,.2f}'.format(float(total_price))) + "\n" +
                      "+ " + str('Current Available Funds: ' + '${:,.2f}'.format(float(account.equity))) + "\n" +
                      "+ " + str('Current Available Buying Power: ' + '${:,.2f}'.format(float(account.buying_power))) + "\n" +
                      "+ " + str('Today\'s Profit: ' + '${:,.2f}'.format(float(balance_change)) + " (" + '{:.2f}%'.format(float(today_percentage)) + ")") + "\n" +
                      "+ " + str('Total Profit: ' + '${:,.2f}'.format(float(total_profit)) + " (" + '{:.2f}%'.format(float(total_percentage)) + ")") + "\n" +
                      "+ " + "ID: " + response['id'] + "\n" +
                      "+ " + "Status: " + response['status'] + "\n" +
                      "```")
        except Exception:
            hook.send("```fix" + "\n" +
                      "X " + "[OPENING TRADE, ERROR OCCURRED]" + "\n" +
                      "X " + "{" + current_time + "}" + "\n" +
                      "X " + "Stock: " + wh_message['symbol'] + "\n" +
                      "X " + "Quantity: " + str(quantity) + "\n" +
                      "X " + "Error: " + response['message'] + "\n" +
                      "```")

    # EXIT
    # EXIT
    # EXIT
    if side == 'short take profit' or side == 'short stop loss' or side == 'long take profit' or side == 'long stop loss':
        r = requests.delete(POSITIONS_URL + "/" + wh_message['symbol'], headers=HEADERS)  # deletes the order (aka liquidate/sell)
        response = json.loads(r.content)  # get the response
        print(response)  # print the response
        # noinspection PyBroadException
        try:
            hook.send("```diff" + "\n" +
                      "- " + "[CLOSING TRADE]" + "\n" +
                      "- " + "{" + current_time + "}" + "\n" +
                      "- " + "Stock: " + response['symbol'] + "\n" +
                      "- " + "Asset: " + response['asset_class'] + "\n" +
                      "- " + "Type: " + wh_message['side'] + "\n" +
                      "- " + "Price: " + '$' + str(symbol_price) + "\n" +
                      "- " + "Quantity: " + response['qty'] + "\n" +
                      "- " + str('Total Price: ' + '$+{:,.2f}'.format(float(total_price))) + "\n" +
                      "- " + str('Current Available Funds: ' + '${:,.2f}'.format(float(account.equity))) + "\n" +
                      "- " + str('Current Available Buying Power: ' + '${:,.2f}'.format(float(account.buying_power))) + "\n" +
                      "- " + str('Today\'s Profit: ' + '${:,.2f}'.format(float(balance_change)) + " (" + '{:.2f}%'.format(float(today_percentage)) + ")") + "\n" +
                      "- " + str('Total Profit: ' + '${:,.2f}'.format(float(total_profit)) + " (" + '{:.2f}%'.format(float(total_percentage)) + ")") + "\n" +
                      "- " + "ID: " + response['id'] + "\n" +
                      "- " + "Status: " + response['status'] + "\n" +
                      "```")
        except Exception:
            hook.send("```fix" + "\n" +
                      "X " + "[CLOSING TRADE, ERROR OCCURRED]" + "\n" +
                      "X " + "{" + current_time + "}" + "\n" +
                      "X " + "Stock: " + wh_message['symbol'] + "\n" +
                      "X " + "Quantity: " + str(quantity) + "\n" +
                      "X " + "Error: " + response['message'] + "\n" +
                      "```")
    return {
        'message': 'I bought the stock!',
        'wh_message': wh_message
    }
