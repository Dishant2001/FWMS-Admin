from jproperties import Properties
import datetime as dt
import time
from pya3 import Aliceblue, OrderType, TransactionType, ProductType


# Importing config file
configs = Properties()
with open(r'..\app_config.properties', 'rb') as config_file:
    configs.load(config_file)

# Creating alice blue client
alice = Aliceblue(user_id=configs.get("NANA_ID").data,api_key=configs.get("NANA_API_KEY").data)

sessionid = alice.get_session_id()
print(sessionid)

banknifty = alice.get_instrument_by_symbol('INDICES','NIFTY BANK')

# Check trade Function
def check_trade():
    alice.get_session_id()['sessionID']
    signal = True
    days=1
    while(signal):
        try:
            exchange='INDICES'
            spot_symbol='NIFTY BANK'
            interval='D'
            indices=True
            from_date=dt.datetime.now()-dt.timedelta(days=days)
            to_date=dt.datetime.now()
            token=alice.get_instrument_by_symbol(exchange,spot_symbol)
            data=alice.get_historical(token,from_date,to_date,interval,indices)
            print(data)
            y_high = data['high'][0]
            y_low = data['low'][0]
            today_open = data['open'][1]
            if(y_high > today_open and today_open > y_low):
                signal = False
                return True
            else:
                print("No Trade today")
                signal = False
                return False
        except:
            days = days + 1

# Checking trade for today
Trade = check_trade()

# Get expiry function
def get_curr_expiry(spot_ltp):
    spot_ltp = int(spot_ltp)
    print(f"Current expiry for {spot_ltp}")
    global datecale
    datecale = dt.date.today()
    while(1):
        expiry = alice.get_instrument_for_fno(exch="NFO",symbol='BANKNIFTY', expiry_date=str(datecale), is_fut=False,strike=spot_ltp, is_CE=True)
        #print(expiry)
        try:
            if list(expiry.values())[0] == 'Not_ok':
                print(f"{datecale} is not expiry")
                datecale = datecale + dt.timedelta(days=1)
            else:
                return datecale
                break
        except:
            return datecale

# repeat variables
qty = int(configs.get('ONE_LOT_QTY').data)

# Basket Oreder function
def place_order(order_type): # order_type : Buy, Sell
    order1 = {  "instrument"        : ce_instrument,
                    "order_type"        : OrderType.Market,
                    "quantity"          : 25,
                    "transaction_type"  : TransactionType.order_type,
                    "product_type"      : ProductType.Intraday,
                    "order_tag"         : "Order1"}
    order2 = {  "instrument"        : pe_instrument,
                    "order_type"        : OrderType.Market,
                    "quantity"          : 25,
                    "transaction_type"  : TransactionType.order_type,
                    "product_type"      : ProductType.Intraday,
                    "order_tag"         : "Order2"}
    orders = [order1, order2]
    border = alice.place_basket_order(orders)
    print("Order placed")
    print("\n\n")
    print(f"LTP is {bnf_spot_ltp} Sell PE and CE on {round_bnf_spot_ltp} Price at expiry {bnf_expiry_date}.")
    return border