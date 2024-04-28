from pya3 import Aliceblue, OrderType, TransactionType, ProductType
import datetime as dt


def login(user_id,api_key):
    global alice
    alice = Aliceblue(user_id,api_key)
    sessionid = alice.get_session_id()
    if 'sessionID' in sessionid:
        return True
    else:
        return False
  
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
                #print("No Trade today")
                signal = False
                return False
        except:
            days = days + 1

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

# Basket Oreder function
def place_b_order(order_type,qty,ce_instrument,pe_instrument): # order_type : Buy, Sell
    order1 = {  "instrument"        : ce_instrument,
                    "order_type"        : OrderType.Market,
                    "quantity"          : qty,
                    "transaction_type"  : TransactionType.order_type,
                    "product_type"      : ProductType.Intraday,
                    "order_tag"         : "Order1"}
    order2 = {  "instrument"        : pe_instrument,
                    "order_type"        : OrderType.Market,
                    "quantity"          : qty,
                    "transaction_type"  : TransactionType.order_type,
                    "product_type"      : ProductType.Intraday,
                    "order_tag"         : "Order2"}
    orders = [order1, order2]
    border = alice.place_basket_order(orders)
    print("Order placed")
    print("\n\n")
    print(f"{order_type} Executed successfully.")
    return True

