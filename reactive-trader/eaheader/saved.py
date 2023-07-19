
###########################################
#          REACTIVE TRADER SAVED          #
###########################################

# :::::::::
# LEVEL 5
# :::::::::

from eazcore.lib import Candle
from eazcore.lib import Duration
import datetime as dt

EALastTickPrice_Saved: float = 0                                               # Last Tick Price Saved
EALastBar_Saved: Candle                                                        # Last Bar Saved
EALastDeviationBar_Saved: Candle                                               # Last Deviation Bar Saved

EARightPriceTo_OpenPos_BtnBuy_Saved: float = 0                                 # Right Price To Open Pos btn-BUY Saved
EARightPriceTo_OpenPos_BtnSell_Saved: float = 0                                # Right Price To Open Pos btn-Sell Saved

EALastTradeLot_Saved: float = 0                                                # Last Trade Lot Saved
EALastTradeLot_RightCoin_Saved: float = 0                                      # Right Coin Saved
EALastTradeLot_LeftCoin_Saved: float = 0                                       # Left Coin Saved

EALast_valideCapital_Saved: float = 0                                          # EA MMG Capital Calculated
EALast_valideCapital_Left_Saved: float = 0                                     # EA MMG Capital Calculated
EALast_valideCapital_Right_Saved: float = 0                                    # EA MMG Capital Calculated

EALast_SavedDay_date_Saved: dt.datetime = Duration.get_null_datetime()
EALast_SaveWeek_monday_date_Saved: dt.datetime = Duration.get_null_datetime()  # Last Saved Week's Monday Date
EALast_SaveMonth_Saved: int = 0                                                # Last Saved Month
EALast_SaveYear_Saved: int = 0                                                 # Last Saved Year
