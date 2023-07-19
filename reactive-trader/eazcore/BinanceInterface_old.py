
###########################################
#        BINANCE INTERFACE          #
###########################################



from eazcore.lib import *

from config import ConnectClient

import eaheader.inputs
import binance.client as bc


class BinanceInterface(object):

    client = ConnectClient().make_connection()

    _pair = Pair()

    _coinLeft = _pair.get_coinLeft()
    _coinRight = _pair.get_coinRight()

    max_amount = client.get_max_margin_loan(asset=_coinLeft, isolatedSymbol=EAinp.EA_Trade_Pair)['amount']
    # Change for how much money you allow for trade. Current one 35% from maximum allowed borrow limit
    max_amount_sell = format(float(max_amount) * 35 / 100, ".6f")

    max_amount = client.get_max_margin_loan(asset=_coinRight, isolatedSymbol=EAinp.EA_Trade_Pair)['amount']
    # Change for how much money you allow for trade. Current one 35% from maximum allowed borrow limit
    max_amount_buy = format(float(max_amount) * 35 / 100, ".6f")

    def __init__(cls):
       pass


    @classmethod
    def I_getCandle_currentTickPrice(cls, _pair: str, _trdMod: EAenum.TradeMode) -> float:
        rsl: float = 0

        # Process

        # must be normalised

        return rsl

    @classmethod
    def I_getCandleInfo_ByDatetime(cls, _dt: dt.datetime, _timeframe: EAenum.TimeFrames) -> list:
        rsl: list = []

        # Process

        return rsl

    @classmethod
    def I_getCandleInfo_ByPosition(cls, _pos: int, _timeframe: EAenum.TimeFrames) -> list:
        rsl: list = []

        # Process

        return rsl

    @classmethod
    def I_getCoinBalance(cls, _coin: str, _trdMod: EAenum.TradeMode) -> float:
        rsl: float = 0

        # Process

        return rsl

    @classmethod
    def I_replenishCoin(cls, _coin: str, _amount: float) -> bool:
        rsl: bool = False

        # process

        return rsl

    @classmethod
    def I_withdrawCoin(cls, _coin: str, _amount: float, _wallet_adr: str) -> bool:
        rsl: bool = False

        # process

        return rsl

    @classmethod
    def I_swapCoin(cls, _coinSrc: str, _coinDst: str, _amount: float) -> bool:
        rsl = False

        # process

        return rsl


    @classmethod
    def I_get_minLot(cls, _pair: str, _trdMode: EAenum.TradeMode) -> float:
        rsl = False

        # process

        return rsl


    @classmethod
    def I_get_maxLot(cls, _pair: str, _trdMode: EAenum.TradeMode) -> float:
        rsl = False

        # process

        return rsl



    @classmethod
    def I_closePositionOrOrder(cls, _ticket: str) -> bool:
        rsl: bool = False

        # process

        return rsl

    @classmethod
    def I_getPosition_Type(cls, _ticket: str) -> EAenum.PosType:
        rsl: EAenum.PosType = EAenum.PosType.OpNo

        # process

        return rsl


    @classmethod
    def I_getPosition_TpPrice(cls, _ticket: str) -> float:
        rsl: float = 0

        # process

        return rsl


    @classmethod
    def I_getPosition_SlPrice(cls, _ticket: str) -> float:
        rsl: float = 0

        # process

        return rsl


    @classmethod
    def I_getPosition_Comment(cls, _ticket: str) -> str:
        rsl: str = ""

        # process

        return rsl

    @classmethod
    def I_getPosition_DealProfit(cls, _ticket) -> float:
        rsl: float = 0

        # Process

        return rsl

    @classmethod
    def I_getPosition_NumberOfBuy(cls) -> int:
        rsl: int = 0

        # Process

        return rsl


    @classmethod
    def I_getPosition_NumberOfSell(cls) -> int:
        rsl: int = 0

        # Process

        return rsl


    @classmethod
    def I_getWaitingOrders_AllCount(cls, _tradeMod: EAenum.TradeMode) -> int:
        rsl: int = 0

        # Process

        return rsl


    @classmethod
    def I_isWaitingOrders_OnMarket(cls, _tradeMod: EAenum.TradeMode) -> bool:
        rsl: bool = False

        # Process

        return rsl

    @classmethod
    def I_getPosition_OpenPrice(cls, _ticket: str) -> float:
        rsl: float = 0

        # Process

        return rsl


    @classmethod
    def I_getPosition_OpenTime(cls, _ticket: str) -> dt.datetime:
        rsl: dt.datetime = Duration.get_null_datetime()

        # Process

        return rsl


    @classmethod
    def I_getPosition_Lot(cls, _ticket: str) -> float:
        rsl: float = 0

        # Process

        return rsl

    @classmethod
    def I_isPosition_FilledOnMarket(cls, _ticket: str) -> bool:
        rsl: bool = False

        # Process

        return rsl

    @classmethod
    def I_getPosition_veryLastFilledOnMarket_Ticket(cls) -> str:
        rsl: str = ""

        # Process

        return rsl

    @classmethod
    def I_getPosition_ClosedTime(cls, _ticket: str) -> dt.datetime:
        rsl: dt.datetime = Duration.get_null_datetime()

        # Process

        return rsl


    @classmethod
    def I_getPosition_ClosedPrice(cls, _ticket: str) -> float:
        rsl: float = 0

        # Process

        return rsl


    @classmethod
    def I_getPosition_ClosedProfit(cls, _ticket: str) -> float:
        rsl: float = 0

        # Process

        return rsl


    @classmethod        #  --TO RECODE--
    def I_placePosition(cls, _posTyp: EAenum.PosType, _tradMode: EAenum.TradeMode, _price: float, _lot: float,
                             _sl: float = 0, _tp: float = 0, is_isolated: bool = True) -> bool:
        rsl: bool = False


        if Util.isTradeMode_Margin(_tradMode):

            if Util.isPositionTypBuy(_posTyp):
                cls.I_openPosition_MarginBuy(_qty=_lot,
                                             _symbol=EAinp.EA_Trade_Pair,
                                             _openPrice=_price,
                                             _isIsolated=is_isolated,
                                             last_price=0,
                                            )

            elif Util.isPositionTypSell(_posTyp):
                cls.I_openPosition_MarginSell(_qty=_lot,
                                              _symbol=EAinp.EA_Trade_Pair,
                                              _openPrice=_price,
                                              _isIsolated=is_isolated,
                                              )


        elif Util.isTradeMode_Spot(_tradMode):

            if Util.isPositionTypBuy(_posTyp):
                pass

            elif Util.isPositionTypSell(_posTyp):
                pass


        elif Util.isTradeMode_Future(_tradMode):
            pass

        return rsl



    @classmethod        #  --TO RECODE--
    def I_closePosition(cls, _openPosTyp: EAenum.PosType, _tradMode: EAenum.TradeMode, _symbol: str, _price: float,
                        _lot: float, _sl: float = 0, _tp: float = 0, is_isolated: bool=True):
        rsl: bool = False

        if Util.isTradeMode_Margin(_tradMode):      # Tp Sl ?
             cls.I_closePosition_Margin(_openPosTyp=_openPosTyp,
                                        _qty=_lot,
                                        _symbol=_symbol,
                                        _closePrice=_price,
                                        _isIsolated=is_isolated,
                                        )

             # Tp sl for Margin

        elif Util.isTradeMode_Spot(_tradMode):      # Tp Sl ?
            cls.I_closePosition_Spot(_openPosTyp=_openPosTyp,
                                     _qty=_lot,
                                     _symbol=_symbol,
                                     _closePrice=_price,
                                     _isIsolated=is_isolated
                                     )
            # Tp Sl for Spot

        elif Util.isTradeMode_Future(_tradMode):
            cls.I_closePosition_Future(_openPosTyp=_openPosTyp,
                                       _qty=_lot,
                                       _symbol=_symbol,
                                       _closePrice=_price,
                                       _tp=_tp,
                                       _sl=_sl,
                                       _isIsolated=is_isolated
                                       )

        return rsl


    # MARGIN
    @classmethod
    def I_openPosition_MarginSell(cls, _qty: float, _symbol: str,_openPrice:float = 0, _isIsolated=True):

        order = cls.client.create_margin_order(
            sideEffectType='MARGIN_BUY',
            symbol=_symbol,                                      # Symbol
            side=cls.client.SIDE_SELL,                           # Sell Order
            type=cls.client.ORDER_TYPE_MARKET,                   # Market Execution
            price=str(_openPrice),                               # Price Open

            quantity=Util.NormalizeLot(_qty),                    # Lot
            isIsolated=From.FromBooleanTo_String(_isIsolated),   # Isolation
            timeInForce=EAinp.EA_TimeInForce,
            recvWindow=EAinp.EA_Max_OrderRequestTime
        )

        return (order)

    @classmethod
    def I_openPosition_MarginBuy(cls, last_price, _qty: float, _symbol: str,_openPrice:float = 0, _isIsolated=True):

        # when close price not defined use current Tick Price
        if _openPrice is 0:
            _openPrice = Candle.getCandle_currentTickPrice()     # Tick Price

        order = cls.client.create_margin_order(
            sideEffectType='MARGIN_BUY',
            symbol=_symbol,                                      # Symbol
            side=cls.client.SIDE_BUY,                            # Buy Order
            type=cls.client.ORDER_TYPE_MARKET,                   # Market Execution
            price=str(_openPrice),                               # Open Price

            # Converting USDT to BTC based on last price and trading 70% of that amount for the precision
            #quantity=format((float(cls.max_amount_buy) / last_price) / 100 * 70, ".5f"),

            quantity=Util.NormalizeLot(_qty),                    # Lot
            isIsolated=From.FromBooleanTo_String(_isIsolated),   # Isolation
            timeInForce=EAinp.EA_TimeInForce,
            recvWindow=EAinp.EA_Max_OrderRequestTime
        )

        return (order)


    # --TO CODE--
    @classmethod
    def I_openPosition_Margin_oco_order(cls, last_price, _qty: float, _symbol: str,_openPrice:float = 0, _isIsolated=True):

        # when close price not defined use current Tick Price
        if _openPrice is 0:
            _openPrice = Candle.getCandle_currentTickPrice()     # Tick Price

        order = cls.client.create_margin_oco_order(
            sideEffectType='MARGIN_BUY',
            symbol=_symbol,                                         # Symbol
            side=cls.client.SIDE_BUY,                               # Buy Order
            type=cls.client.ORDER_TYPE_MARKET,                      # Market Execution
            price=str(_openPrice),                                  # Open Price

            quantity=Util.NormalizeLot(_qty),                       # Lot
            isIsolated=From.FromBooleanTo_String(_isIsolated),      # Isolation
            timeInForce=EAinp.EA_TimeInForce,
            recvWindow=EAinp.EA_Max_OrderRequestTime
        )

        return (order)



    @classmethod
    def I_closePosition_Margin(cls, _qty: float, _openPosTyp: EAenum.PosType, _symbol: str, _closePrice:float = 0,_isIsolated=True):

        # when close price not defined use current Tick Price
        if _closePrice is 0:
           _closePrice = Candle.getCandle_currentTickPrice()        # Tick Price

        order = {}
        if Util.isPositionTypBuy(_openPosTyp):             # when Open position is BUY
            order = cls.client.create_margin_order(
                symbol=_symbol,                                     # Symbol
                side=cls.client.SIDE_SELL,                          # Sell Order
                type=cls.client.ORDER_TYPE_MARKET,                  # Market Execution
                price=str(_closePrice),                             # close Price

                quantity=Util.NormalizeLot(_qty),                   # Lot
                isIsolated=From.FromBooleanTo_String(_isIsolated),  # Isolation
                sideEffectType='AUTO_REPAY',                        # AUTO REPAY margin
                timeInForce=EAinp.EA_TimeInForce,                   # Time In Force
                recvWindow=EAinp.EA_Max_OrderRequestTime
            )

        elif Util.isPositionTypSell(_openPosTyp):          # when Open Position is SELL
            order = cls.client.create_margin_order(
                symbol=_symbol,                                     # Symbol
                side=cls.client.SIDE_BUY,                           # Buy Order
                type=cls.client.ORDER_TYPE_MARKET,                  # Market Execution
                price=str(_closePrice),                             # close Price

                quantity=Util.NormalizeLot(_qty),                   # Lot
                isIsolated=From.FromBooleanTo_String(_isIsolated),  # Isolation
                sideEffectType='AUTO_REPAY',                        # AUTO REPAY margin
                timeInForce=EAinp.EA_TimeInForce,                   # Time In Force
                recvWindow=EAinp.EA_Max_OrderRequestTime
            )

        return (order)



    # SPOT
    @classmethod
    def I_openPosition_SpotSell(cls, _qty: float, _symbol: str,_openPrice:float = 0, _isIsolated=True):

        order = cls.client.create_order(
            symbol=_symbol,                                         # Symbol
            side=cls.client.SIDE_SELL,                              # Sell Order
            type=cls.client.ORDER_TYPE_MARKET,                      # Market Execution
            price=str(_openPrice),                                  # Price Open

            quantity=Util.NormalizeLot(_qty),                       # Lot
            timeInForce=EAinp.EA_TimeInForce,                       # Time In Force
            recvWindow=EAinp.EA_Max_OrderRequestTime
        )

        return (order)


    @classmethod
    def I_openPosition_SpotBuy(cls, last_price, _qty: float, _symbol: str,_openPrice:float = 0, _isIsolated=True):

        # when close price not defined use current Tick Price
        if _openPrice is 0:
            _openPrice = Candle.getCandle_currentTickPrice()     # Tick Price

        order = cls.client.create_order(
            symbol=_symbol,                                      # Symbol
            side=cls.client.SIDE_BUY,                            # Buy Order
            type=cls.client.ORDER_TYPE_MARKET,                   # Market Execution
            price=str(_openPrice),                               # Open Price

            quantity=Util.NormalizeLot(_qty),                    # Lot
            timeInForce=EAinp.EA_TimeInForce,                    # Time In Force
            recvWindow=EAinp.EA_Max_OrderRequestTime
        )

        return (order)


    @classmethod
    def I_closePosition_Spot(cls, _qty: float, _openPosTyp: EAenum.PosType, _symbol: str, _closePrice: float = 0,
                               _isIsolated=True):

        # when close price not defined use current Tick Price
        if _closePrice is 0:
            _closePrice = Candle.getCandle_currentTickPrice()  # Tick Price

        order = {}
        if Util.isPositionTypBuy(_openPosTyp):          # when Open position is BUY
            order = cls.client.create_margin_order(
                symbol=_symbol,                                # Symbol
                side=cls.client.SIDE_SELL,                     # Sell Order
                type=cls.client.ORDER_TYPE_MARKET,             # Market Execution
                price=str(_closePrice),                        # close Price

                quantity=Util.NormalizeLot(_qty),              # Lot
                timeInForce=EAinp.EA_TimeInForce,              # Time In Force
                recvWindow=EAinp.EA_Max_OrderRequestTime
            )

        elif Util.isPositionTypSell(_openPosTyp):              # when Open Position is SELL
            order = cls.client.create_margin_order(
                symbol=_symbol,                                # Symbol
                side=cls.client.SIDE_BUY,                      # Buy Order
                type=cls.client.ORDER_TYPE_MARKET,             # Market Execution
                price=str(_closePrice),                        # close Price

                quantity=Util.NormalizeLot(_qty),              # Lot
                timeInForce=EAinp.EA_TimeInForce,              # Time In Force
                recvWindow=EAinp.EA_Max_OrderRequestTime
            )

        return (order)



    # FUTURE (don't Need Future Contract)
    @classmethod
    def I_openPosition_FutureSell(cls, _qty: float, _symbol: str,_openPrice:float = 0, _isIsolated=True):
        pass

    @classmethod
    def I_openPosition_FutureBuy(cls, last_price, _qty: float, _symbol: str,_openPrice:float = 0, _isIsolated=True):
        pass

    @classmethod
    def I_closePosition_Future(cls, _qty: float, _openPosTyp: EAenum.PosType, _symbol: str, _closePrice:float,
                               _tp: float = 0, _sl: float = 0, _isIsolated = True):
        pass

    @classmethod
    def I_placeFutureStopLoss(cls, _ticket, _SLprice_: float):
        pass

    @classmethod
    def I_placeFutureTakeprofit(cls, _ticket, _TPprice: float):
        pass

#  --- END CLASS BINANCE-INTERFACE ---  #
