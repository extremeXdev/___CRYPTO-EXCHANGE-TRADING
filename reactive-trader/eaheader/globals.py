
###########################################
#        REACTIVE TRADER GLOBALS          #
###########################################

# :::::::::
# LEVEL 4
# :::::::::

from eazcore.lib import CFDManager
from eazcore.lib import Pair
from eazcore.lib import Lifetime
from eazcore.lib import ExChangeInterface


EA_NbOf_PipsGained = 0                                       # EA Number of Pips Gained
EA_NbOf_SuccessFul_ProfitTrade = 0                           # EA Number of SuccessFul Profit Trade
EA_NbOf_NoLoss_Trades = 0                                    # EA Number Of SuccessFul

# EA_API_KEY = 0                                               # EA API KEY        #
# EA_API_SECRET = 0                                            # EA API SECRET


EA_MMG_Capital_Calc = 0                                      # EA MMG Capital Calculated
EA_MMG_Lot_Calc = 0                                          # EA MMG Volume Calculated
EA_MMG_Lot_Left_Calc = 0                                     # EA MMG Volume Left Calculated
EA_MMG_Lot_Right_Calc = 0                                    # EA MMG Volume Right Calculated
EA_MMG_Current_Lot = 0                                       # EA MMG Current Lot

EA_Bot_Interruption_Called = False                           # EA Bot Interruption Called
EA_Bot_Interrupted = False
EA_Bot_IsRunning = False                                     # EA Bot Running State

EA_Day_Withdrawal_Performed = False                          # EA Day Withdraw is Performed

# EA_position_very_last_filled_onmarket =                     # EA very last position filled on market


# ..... Program Objects

cfdManaja = CFDManager()     # CFDManager launching
EAPair = Pair()              # Pair
EA_lifetime = Lifetime()     # Setting Lifetime Countdown
EA_Exchange = ExChangeInterface.get_exchange()

# .....
