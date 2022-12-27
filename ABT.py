import time
import requests
from binance.client import Client
from telegram.bot import Bot

API_HOST = 'https://api.bitkub.com/'

# Replace YOUR_BOT_TOKEN and YOUR_CHAT_ID with your bot's token and the chat ID of the chat you want to send the message to, respectively.
bot = Bot(token='5707959902:AAHTzOnZZtB1WrWvbGS4sCRuetnIgm1c7-0')
CHAT_ID = '-1001676481201'

bnb_obj = Client()

# Create empty dictionary to store ticker information
ticker_info = {}

while True:
    # Send GET request to Bitkub API to retrieve ticker information
    response = requests.get(API_HOST + '/api/market/ticker')
    result = response.json()
    usdt_thb_last_price = result['THB_USDT']['last']

    # Iterate over all symbols in the ticker information
    for symbol, ticker in result.items():
        # Remove THB_ prefix from symbol
        symbol = symbol.replace("THB_", "")
        symbol = f'{symbol}USDT'

        # Extract last price from ticker information
        last_price1 = ticker['last']

        # Convert last price to USD using fixed exchange rate
        last_price_usd = float(last_price1) / float(usdt_thb_last_price)

        # Add ticker information to dictionary
        if symbol not in ticker_info:
            ticker_info[symbol] = []
        ticker_info[symbol].append(('Bitkub', last_price_usd))

        
    # Retrieve ticker information for futures contracts from Binance API
    tickers = bnb_obj.futures_ticker()

    # Iterate over all tickers and add ticker information to dictionary for those with "USDT" in the symbol
    for ticker in tickers:
        symbol = ticker['symbol']
        last_price2 = float(ticker['lastPrice'])
        last_price_usd2 = last_price2 
        if "USDT" in symbol:
                if symbol not in ticker_info:
                    ticker_info[symbol] = []
                ticker_info[symbol].append(('Binance', last_price_usd2))
    
    # Iterate over dictionary and print ticker information for each symbol
    for symbol, ticker_list in ticker_info.items():
        if symbol == "CVCUSDT":
            continue
        print(f'{symbol}:')
        for exchange, last_price in ticker_list:
            print(f'  {exchange}: {last_price:,.2f} USD')

        # Calculate difference between last prices on different exchanges
        if len(ticker_list) > 1:
            diff = abs(ticker_list[0][1] - ticker_list[1][1])

            # Calculate percentage difference
            percent_diff = diff / ticker_list[0][1] * 100

            # Print difference if it is 3% or more
            if percent_diff >= 5:
                print(f'  Difference: {diff:,.3f} USD ({percent_diff:.1f}%)')
                message = f'{symbol}: ราคาต่างกัน: {diff:,.3f} USD ({percent_diff:.1f}%)'
                bot.send_message(chat_id='-1001676481201    ', text=message)
    
    # Print separator
    print('--------')
    
    # Wait for 100 seconds before repeating loop
    time.sleep(100)


