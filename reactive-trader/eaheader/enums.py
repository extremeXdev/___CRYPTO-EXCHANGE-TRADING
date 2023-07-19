
###########################################
#      REACTIVE TRADER ENUMERATION        #
###########################################

# :::::::::
# LEVEL 1
# :::::::::

from enum import Enum   # , unique, auto
from binance.client import BaseClient as Bbc
from pytz import timezone


class PosType(Enum):
    OpBuy = "Buy"
    OpSell = "Sell"
    OpNo = "No"

# __
    def get_opposite_position_type(self):
        rsl = PosType.OpNo

        if self.value is PosType.OpBuy:  # when OpBuy
            rsl = PosType.OpSell  # set  OpSell

        elif self.value is PosType.OpSell:  # When OpSell
            rsl = PosType.OpBuy  # set OpBuy

        return rsl

# __
    @staticmethod
    def get_opposite_position_type_(ea_pos: type):     # --VERIFY--
        rsl = PosType.OpNo

        if ea_pos is PosType.OpBuy:      # when OpBuy
            rsl = PosType.OpSell         # set  OpSell

        elif ea_pos is PosType.OpSell:   # When OpSell
            rsl = PosType.OpBuy          # set OpBuy

        return rsl

# __
    @staticmethod
    def get_position_type_as_string(open_postyp: type, want_capitalize: bool = False) -> str:
        rsl: str = ""

        if open_postyp == PosType.OpBuy:
            rsl = "Buy"
        elif open_postyp == PosType.OpSell:
            rsl = "Sell"

        if want_capitalize:
            rsl.upper()

        return rsl
# End Enum  PosType #


class OrdType(Enum):
    OpTypLimit = Bbc.ORDER_TYPE_LIMIT
    OpTypMarket = Bbc.ORDER_TYPE_MARKET
    OpTypStopLoss = Bbc.ORDER_TYPE_STOP_LOSS
    OpTypStopLossLimit = Bbc.ORDER_TYPE_STOP_LOSS_LIMIT
    OpTypTakeProfit = Bbc.ORDER_TYPE_TAKE_PROFIT
    OpTypTakeProfitLimit = Bbc.ORDER_TYPE_TAKE_PROFIT_LIMIT
    OpTypLimitMaker = Bbc.ORDER_TYPE_LIMIT_MAKER
    OpNo = "OpNo"

    @staticmethod
    def get_ordtyp_as_string(open_ordtyp) -> str:
        rsl: str

        rsl = open_ordtyp

        return rsl
# End Enum PosType #


class FutureOrdType(Enum):
    FOpTypLimit = Bbc.FUTURE_ORDER_TYPE_LIMIT
    FOpTypMarket = Bbc.FUTURE_ORDER_TYPE_MARKET
    FOpTypStop = Bbc.FUTURE_ORDER_TYPE_STOP
    FOpTypStopMarket = Bbc.FUTURE_ORDER_TYPE_STOP_MARKET
    FOpTypTakeProfit = Bbc.FUTURE_ORDER_TYPE_TAKE_PROFIT
    FOpTypTakeProfitMarket = Bbc.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET
    FOpTypLimitMaker = Bbc.FUTURE_ORDER_TYPE_LIMIT_MAKER
    FOpNo = "OpNo"
# End Enum Future #


class TradeMode(Enum):
    Spot = "Spot"
    Margin = "Margin"
    Future = "Future"
    MNone = ""
# End Enum TradeTyp #


class CoinSideTyp(Enum):
    coinLeft = 1
    coinRight = 2
    coinSideNo = -1
# End Enum CoinSideTyp #


class TrdDirection(Enum):
    Upper = 1
    Downer = 2
    Unknown = -1
# End Enum Direction #


class CandleTyp(Enum):
    Bullish = "Bullish"
    Bearish = "Bearish"
    Anonymous = "Anonymous"
    CdlNone = "None"
# End Enum CandleTyp #


class CFDPosListSrc(Enum):
    OpenPosList = 1
    HistoryPosList = 2
    No = -1
# End Enum CFDPosListSrc #


class PosFillTyp(Enum):
    OpenPos = 1
    ClosePos = 2
    No = -1
# End Enum PosFillTyp #


class TimeInForce(Enum):
    GTC = Bbc.TIME_IN_FORCE_GTC           # Good til Canceled
    IOC = Bbc.TIME_IN_FORCE_IOC           # Immediate or Canceled
    FOK = Bbc.TIME_IN_FORCE_FOK           # Fill or Kill
# End Enum TimeInForce #


class Timezone(Enum):
    utc_moscow = timezone('Europe/Moscow')
    utc_abidjan = timezone('Africa/Abidjan')
    utc_paris = timezone('Europe/Paris')
    utc_newyork = timezone('America/New_York')
    utc_hongkong = timezone('Asia/Hong_Kong')
# End Enum timezone #


class TradePairSpot(Enum):
    BUSDUSDT = "BUSD/USDT"                # BUSD USDT
    USDCUSDT = "USDC/USDT"                # USDC USDT
    USDCBUSD = "USDC/BUSD"                # USDC BUSD
    TUSDUSDT = "TUSD/USDT"                # TUSD USDT
    EURBUSD = "EUR/BUSD"                  # EUR BUSD
    PNone = ""                            # NO
# End Enum TradePairSpot #


class TradePairMargin(Enum):
    BUSDUSDT = "BUSD/USDT"                # BUSD USDT
    USDCUSDT = "USDC/USDT"                # USDC USDT
    USDCBUSD = "USDC/BUSD"                # USDC BUSD
    PNone = ""                            # NO
# End Enum TradePairMargin #


class FutureMod(Enum):
    CoinAsCo = 1                           # Coin as Collateral
    USDAsCo = 2                            # USD as Collateral
# End Enum FutureMod #


class TimeFrames(Enum):
    M1 = Bbc.KLINE_INTERVAL_1MINUTE       # M1
    M3 = Bbc.KLINE_INTERVAL_3MINUTE       # M3
    M5 = Bbc.KLINE_INTERVAL_5MINUTE       # M5
    M15 = Bbc.KLINE_INTERVAL_15MINUTE     # M15
    M30 = Bbc.KLINE_INTERVAL_30MINUTE     # M30

    H1 = Bbc.KLINE_INTERVAL_1HOUR         # H1
    H2 = Bbc.KLINE_INTERVAL_2HOUR         # H2
    H4 = Bbc.KLINE_INTERVAL_4HOUR         # H4
    H6 = Bbc.KLINE_INTERVAL_6HOUR         # H6
    H8 = Bbc.KLINE_INTERVAL_8HOUR         # H8
    H12 = Bbc.KLINE_INTERVAL_12HOUR       # H12

    D1 = Bbc.KLINE_INTERVAL_1DAY          # D1
    D3 = Bbc.KLINE_INTERVAL_3DAY          # D3
    W1 = Bbc.KLINE_INTERVAL_1WEEK         # W1
    Mt = Bbc.KLINE_INTERVAL_1MONTH        # Mt
# End Enum TimeFrames #


class SupportedExchange(Enum):
    Binance = "Binance"
    CoinBase = "Coinbase"
    huobi = "Huobi"
# End Enum SupportedExchange #

# _______________________________________________________________


class MarginBalanceTyp(Enum):
    MBorrowed = "borrowed"
    MFree = "free"
    MInterest = "interest"
    MLocked = 'locked'
    MNetAsset = 'netAsset'
# End Enum MarginBalanceTyp #


class SpotBalanceTyp(Enum):
    SFree = "free"
    SLocked = 'locked'
# End Enum SpotBalanceTyp #


class FutureBalanceTyp(Enum):
    FWalletBalance = "walletBalance"
    FUnrealizedProfit = "unrealizedProfit"
    FMarginBalance = "marginBalance"
    FMaintMargin = "maintMargin"
    FInitialMargin = "initialMargin"
    FPositionInitialMargin = "positionInitialMargin"
    FOpenOrderInitialMargin = "openOrderInitialMargin"
    FMaxWithdrawAmount = "maxWithdrawAmount"
# End Enum FutureBalanceTyp #
