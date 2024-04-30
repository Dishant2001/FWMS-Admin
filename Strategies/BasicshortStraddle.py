from jproperties import Properties
import datetime as dt
import time
from Strategies.resources import *


# Importing config file
configs = Properties()
with open(r'.\app_config.properties', 'rb') as config_file:
    configs.load(config_file)

# repeat variables
def strategy1():
    qty = int(configs.get('ONE_LOT_QTY').data)
    End = False

    # Login check
    status = login(user_id=configs.get("NANA_ID").data,api_key=configs.get("NANA_API_KEY").data)
    if (status==True):
        # Checking trade for today
        Trade = True#check_trade()
        while(1):
            if End == True:
                print("Trade Executed")
                break
            elif (Trade == True):
                print(dt.datetime.now().time())
                if dt.datetime.now().time()>=dt.time(9,20,1):
                    alice = Aliceblue(user_id=configs.get("NANA_ID").data,api_key=configs.get("NANA_API_KEY").data)
                    banknifty = alice.get_instrument_by_symbol('INDICES','NIFTY BANK')
                    bnf_spot_ltp = float(alice.get_scrip_info(banknifty)['LTP'])
                    round_bnf_spot_ltp = round((bnf_spot_ltp/100),0)*100
                    bnf_expiry_date = get_curr_expiry(round_bnf_spot_ltp)
                    ce_instrument = alice.get_instrument_for_fno(exch="NFO",symbol='BANKNIFTY', expiry_date=str(bnf_expiry_date),
                                                                        is_fut=False,strike=round_bnf_spot_ltp, is_CE=True)
                    pe_instrument = alice.get_instrument_for_fno(exch="NFO",symbol='BANKNIFTY', expiry_date=str(bnf_expiry_date),
                                                                        is_fut=False,strike=round_bnf_spot_ltp, is_CE=False)
                    cesell = float(alice.get_scrip_info(ce_instrument)['LTP'])
                    pesell = float(alice.get_scrip_info(pe_instrument)['LTP'])
                    val_sum = cesell + pesell

                    if ((val_sum > 272)):
                        print(val_sum)
                        place_b_order("Sell",qty,ce_instrument,pe_instrument)
                        print(f"LTP is {bnf_spot_ltp} Sell PE and CE on {round_bnf_spot_ltp} Price at expiry {bnf_expiry_date}.")

                        # Calculating the Target and the StopLoss
                        target = val_sum * 0.9
                        stoploss = val_sum * 1.10
                        print("Target: ", target)
                        print("Stoploss: ",stoploss)
                        print("Value Sum: ",val_sum)

                        # Calculating Trade
                        while(1):
                            time.sleep(5)
                            celtp = float(alice.get_scrip_info(ce_instrument)['LTP'])
                            peltp = float(alice.get_scrip_info(pe_instrument)['LTP'])
                            val_ltp = celtp + peltp

                            if (val_ltp <= target):
                                print("Target Achive Square Off the Trade at: ",val_ltp)
                                place_b_order("Buy",qty,ce_instrument,pe_instrument)
                                End = True
                                break

                            elif (val_ltp >= stoploss):
                                print("StopLoss Hit Square Off the Trade at: ", val_ltp)
                                place_b_order("Buy",qty,ce_instrument,pe_instrument)
                                End = True
                                break

                            elif (dt.datetime.now().time()>=dt.time(15,15,0)):
                                print("Market Close Square Off the Trade at: ", val_ltp)
                                place_b_order("Buy",qty,ce_instrument,pe_instrument)
                                End = True
                                break

                            else:
                                try :
                                    print(f"Current Sum: {val_ltp} and Running Profit/Loss: {(val_sum)-(val_ltp)}")
                                except:
                                    print("Not get LTP")
                                    time.sleep(5)
                    else:
                        print(f"{val_sum} is less then 272 not trade today")
                        break
                else:
                    time.sleep(1)
            else:
                print("Not Trade today")
                break
    else:
        print("Please login with web or app.")

    return "strategy executed"