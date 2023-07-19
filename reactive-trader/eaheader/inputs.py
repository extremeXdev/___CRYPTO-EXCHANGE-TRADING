
###########################################
#        REACTIVE TRADER INPUTS           #
###########################################

# :::::::::
# LEVEL 3
# :::::::::

import eaheader.enums as eaenum
#   import eaheader.constants as Eacst

# :::::: MODE
EA_Mode_Debugger = True                                          # EA Debugger Mode
EA_Mode_TestViaVoyant = True                                     # EA Test Via Voyant
EA_Mode_ActivateTesterMode = False                               # Activate tester Mode

EA_Trade_Mode = eaenum.TradeMode.Margin                          # set To Margin Trading
# ::::::

# :::::: PAIR
EA_Trade_Pair: str = eaenum.TradePairMargin.BUSDUSDT.value       # EA Trade Pair
# EA_SelectedSymbol = eaenum.TradePairMargin.BUSDUSDT.value        # EA Selected Symbol

EA_Want_Change_leverage = True                                   # EA Want Change Leverage ?
EA_Leverage = 125                                                # EA Leverage
EA_Minor_Coin_Balance_inAlert_PCR = 20/100                       # Minor Coin Balance Alert PCR according to Major
# ::::::

# ::::: TIME
EA_Lifetime_Duration_Days = 365                                  # EA Lifetime Duration Days
EA_Timeframe = eaenum.TimeFrames.M1.value                        # EA TimeFrame
EA_Max_OrderRequestTime = 3000                                   # EA Max Order Request Time
EA_TimerSetup_ms = 3600*1000                                     # EA Timer Setup (ms)
EA_Prefer_Use_ServerTimeThanLocal = False                        # Prefer Use Fx Time Than Local
# :::::

# ::::: WALLET
EA_Wallets = ["adr1", "adr2"]
EA_Withdrawal_WalletSelected = 0                                 # withdrawal Wallet Selection
EA_Withdrawal_Time = 23                                          # EA Withdrawal Time (eg: 0-23)

EA_TP_TargetPips = 0                                             # EA TP Target Pips (don't need TP)
EA_SL_SecurityPips = 3                                           # EA SL Security Pips

EA_Use_Collateral = False                                        # EA Use Collateral ( Spot or Margin Mode )
EA_Future_Mode = eaenum.FutureMod.USDMod                         # EA Future Collateral Mode

EA_Trade_SideLeft = True                                         # EA Trade Side Left
EA_Trade_SideRight = True                                        # EA Trade Side Right
# :::::

# ::::: MMG
EA_MMG_Lot_Capital_PCT = 10                                      # EA MMG Lot Capital Percent
# ::::: MMG

EA_MagicNumber = 888

# ::::: ORDERS
EA_TimeInForce = eaenum.TimeInForce.GTC                          # EA Time In Force for Orders
EA_IsIsolated = True                                             # EA Margin Order Isolation Mode
# ::::: ORDERS

# :::: EXCHANGE CONFIG
EA_DEFAULT_EXCHANGE = eaenum.SupportedExchange.Binance
# EA_Use_CCXT = True                                               # EA Use CCXT          # No Longer Using that
EA_Use_Asinc = False                                             # EA Use Asinc         # Don't using yet
# :::: EXCHANGE CONFIG

# :::: EXCHANGE
EA_Exc_Enable_RateLimit = True                                   # EA Exchange Enable Rate Limit
EA_Exc_RateLimit = EA_Max_OrderRequestTime                       # EA Exchange Rate Limit
EA_Exc_Verbose = False                                           # EA Exchange Verbose
# :::: EXCHANGE

# ::::: API
EA_API_Key = ""
EA_API_Secret = ""
EA_API_PW = ""
# ::::: API
