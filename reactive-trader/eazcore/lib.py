
###########################################
#        REACTIVE TRADER LIBRARY          #
###########################################

# LEVEL 6

# IMPORTS #

import datetime as dt
from pytz import timezone
# import numpy
# import talib
# import time
# import math

import eaheader.enums as Eaenum
import eaheader.constants as Eacst
import eaheader.globals as Eagbl
import eaheader.inputs as Eainp
import eaheader.saved as Easav

import binance.client as bc

from eazcore.core import EA
from eazcore.BinanceInterface import *
from eazcore.CoinbaseInterface import *

###########


class Candle(object):
    """
    Basic Candle Class
    """

    m_Candle_Open: float
    m_Candle_High: float
    m_Candle_Low: float
    m_Candle_Close: float
    m_Candle_Volume: float

    m_Candle_dt: dt.datetime
    m_Candle_Pos: int

    m_Candle_Typ: Eaenum.CandleTyp

# __
    def __init__(self, _pos: int = 0, _datetime: dt.datetime = None):

        _getNullCdl = False

        tmframe = Eainp.EA_Timeframe
        Pair.get_symbol()

        data = []
        if _datetime is None:
            data = Candle.get_cdl_info_by_position(_pos=_pos, _timeframe=tmframe,
                                                   _symbol=Pair.get_symbol())         # call to exchange
        elif _pos != -1:
            data = Candle.get_cdl_info_by_datetime(_dt=_datetime, _timeframe=tmframe,
                                                   _symbol=Pair.get_symbol())         # call to exchange
        else:   # when position equal -1
            _getNullCdl = True

        if not Util.is_true(_getNullCdl):
            self._populate(price_o=data[0],    # O
                           price_h=data[1],    # H
                           price_l=data[2],    # L
                           price_c=data[3],    # C
                           _vol=data[4],       # V
                           _dt=data[5],        # T
                           _pos=data[6])       # P
        else:
            self._populate(price_o=0, price_h=0, price_l=0, price_c=0,
                           _vol=0, _dt=None, _pos=-1)

# __
    def _populate(self, price_o: float, price_h: float, price_l: float, price_c: float,
                  _vol: float, _dt: dt.datetime = None, _pos: int = -1) -> None:
        """ Populate Function
        :param price_o:
        :param price_h:
        :param price_l:
        :param price_c:
        :param _vol:
        :param _dt:
        :param _pos
        """
        self.set_candle_open_price(price_o)
        self.set_candle_high_price(price_h)
        self.set_candle_low_price(price_l)
        self.set_candle_close_price(price_c)
        self.set_candle_volume(_vol)
        self.set_candle_datetime(_dt)
        self.set_candle_position(_pos)

        self.set_candle_typ(Candle.get_cdl_type(self.__class__))

# __
    @property
    def get_candle_upperprice(self) -> float:     # --To Recode--
        """ get Candle Info _Upper Price
        :return: float
        """
        rsl = self.get_candle_high_price()

        return rsl

# __
    @property
    def get_candle_bottomprice(self) -> float:    # --To Recode--
        """ get Candle Info _Bottom Price
        :return: float
        """
        rsl = self.get_candle_low_price()

        return rsl

# __
    @staticmethod
    def get_cdl_latest_candle() -> Candle:
        """get latest Candle Object
        :return Candle object
        """
        rsl: Candle

        rsl = Candle(_pos=0)

        return rsl

# __
    @staticmethod
    def get_cdl_previous_candle() -> Candle:
        """get previous Candle Object
        :return: Candle object
        """
        rsl: Candle

        rsl = Candle(_pos=1)

        return rsl

# __
    @staticmethod
    def get_cdl_latest_candle_ohlc() -> list:
        """ get Candle Info
        :return Open High Low Close: list
        """
        _cdl = Candle(_pos=0)

        rsl = _cdl.get_candle_ohlc()

        return rsl

# __
    @staticmethod
    def get_cdl_latest_candle_ohlcvdp() -> list:
        """ get Candle Info _Latest Candle OHLCVDP
        :return: list
        """
        _cdl = Candle(_pos=0)

        rsl = _cdl.get_candle_ohlcvdp()

        return rsl

# __
    @staticmethod
    def get_cdl_latest_candle_datetime() -> dt.datetime:
        """ get Candle Info _Latest Candle Datetime
        :return: datetime
        """
        _cdl = Candle(_pos=0)

        rsl = _cdl.get_candle_datetime()

        return rsl

# __
    @staticmethod
    def get_cdl_previous_candle_ohlc() -> list:
        """ get Candle Info _Previous Candle OHLC
        :return: list
        """
        _cdl = Candle(_pos=1)

        rsl = _cdl.get_candle_ohlc()

        return rsl

# __
    @staticmethod
    def get_cdl_previous_candle_ohlcvdp() -> list:
        """ get Candle Info _Previous Candle OHLCVDP
        :return: list
        """
        _cdl = Candle(_pos=1)

        rsl = _cdl.get_candle_ohlcvdp()

        return rsl

# __
    @staticmethod
    def get_cdl_previous_candle_datetime() -> dt.datetime:
        """ get Candle Info _Previous Candle Datetime
        :return: datetime
        """
        _cdl = Candle(_pos=1)

        rsl = _cdl.get_candle_datetime()

        return rsl

# __
    @staticmethod
    def get_cdl_ohlc_by_position(_pos: int) -> list:
        """ get Candle Info _OHLC by position
        :return: list
        """
        _cdl = Candle(_pos=_pos)

        rsl = _cdl.get_candle_ohlc()

        return rsl

# __
    @staticmethod
    def get_cdl_ohlc_by_datetime(_dt) -> list:
        """ get Candle Info _OHLC by position
        :return: list
        """
        _cdl = Candle(_datetime=_dt)

        rsl = _cdl.get_candle_ohlc()

        return rsl

# __
    @staticmethod
    def get_cdl_datetime_by_position(_pos: int) -> dt.datetime:
        """ get Candle datetime By position
        :return: datetime
        """
        _cdl = Candle(_pos=_pos)

        rsl = _cdl.get_candle_datetime()

        return rsl

# __
    @staticmethod
    def get_cdl_position_by_datetime(_dt: dt.datetime) -> int:
        """ get Candle position by Datetime
        :param _dt
        :return: int
        """
        rsl: int

        _cdl = Candle(_datetime=_dt)

        rsl = _cdl.get_candle_position()

        return rsl

# __
    def get_candle_ohlc(self) -> list:
        """ get Candle Info _OHLC
        :return: list
        """
        rsl = [self.get_candle_open_price(),
               self.get_candle_high_price(),
               self.get_candle_low_price(),
               self.get_candle_close_price()]

        return rsl

# __
    def get_candle_ohlcvdp(self) -> list:
        """ get Candle Info _OHLCVDP
        :return: list
        """
        rsl = [self.get_candle_open_price(),
               self.get_candle_high_price(),
               self.get_candle_low_price(),
               self.get_candle_close_price(),
               self.get_candle_volume(),
               self.get_candle_datetime(),
               self.get_candle_position()]

        return rsl

# getters
    def get_candle_open_price(self):
        return self.m_Candle_Open

    def get_candle_high_price(self):
        return self.m_Candle_High

    def get_candle_low_price(self):
        return self.m_Candle_Low

    def get_candle_close_price(self):
        return self.m_Candle_Close

    def get_candle_datetime(self):
        return self.m_Candle_dt

    def get_candle_volume(self):
        return self.m_Candle_Volume

    def get_candle_position(self):
        return self.m_Candle_Pos

    def get_candle_typ(self):
        return self.m_Candle_Typ
#

# setters
    def set_candle_open_price(self, _price: float):
        self.m_Candle_Open = _price

    def set_candle_high_price(self, _price: float):
        self.m_Candle_High = _price

    def set_candle_low_price(self, _price: float):
        self.m_Candle_Low = _price

    def set_candle_close_price(self, _price: float):
        self.m_Candle_Close = _price

    def set_candle_datetime(self, _dt: dt.datetime):
        self.m_Candle_dt = _dt

    def set_candle_volume(self, _vol: float):
        self.m_Candle_Volume = _vol

    def set_candle_position(self, _pos: int):
        self.m_Candle_Pos = _pos

    def set_candle_typ(self, _typ: Eaenum.CandleTyp):
        self.m_Candle_Typ = _typ
#

# __
    @staticmethod
    def get_candle_count_between_datetime(_dt1: dt.datetime, _dt2: dt.datetime) -> int:
        """ get Candle _Count Between Datetime
        :return: int
        """
        rsl: int

        _cdl = Candle(_datetime=_dt1)
        pos1 = _cdl.get_candle_position()

        _cdl2 = Candle(_datetime=_dt2)
        pos2 = _cdl2.get_candle_position()

        rsl = abs(pos1 - pos2)

        return rsl

# __
    @property
    def get_candle_body_size(self) -> int:
        """ get Candle Info _Body Size (pips)
        :return: int
        """
        rsl = From.from_prices_to_dist_between(self.get_candle_open_price(),
                                               self.get_candle_close_price())
        return rsl

# __
    @property
    def get_candle_full_size(self) -> int:
        """ get Candle Info _Body Size (pips)
        :return: int
        """
        rsl = From.from_prices_to_dist_between(self.get_candle_high_price(),
                                               self.get_candle_low_price())
        return rsl

# __
    @property
    def get_candle_upper_wisp_size(self) -> int:
        """ get Candle Info _Body Size (pips)
        :return: int
        """
        rsl = 0

        cdl_typ = self.get_candle_typ()

        if Util.is_candle_type_bullish(cdl_typ):
            rsl = From.from_prices_to_dist_between(self.get_candle_high_price(),
                                                   self.get_candle_close_price())
        elif Util.is_candle_type_bearish(cdl_typ):
            rsl = From.from_prices_to_dist_between(self.get_candle_high_price(),
                                                   self.get_candle_open_price())
        elif Util.is_candle_type_anonymous(cdl_typ):
            rsl = From.from_prices_to_dist_between(self.get_candle_open_price(),
                                                   self.get_candle_high_price())

        return rsl

# __
    @property
    def get_candle_bottom_wisp_size(self) -> int:
        """ get Candle Info _Bottom wisp Size (pips)
        :return: int
        """
        rsl = 0

        cdl_typ = self.get_candle_typ()

        if Util.is_candle_type_bullish(cdl_typ):
            rsl = From.from_prices_to_dist_between(self.get_candle_low_price(),
                                                   self.get_candle_open_price())
        elif Util.is_candle_type_bearish(cdl_typ):
            rsl = From.from_prices_to_dist_between(self.get_candle_low_price(),
                                                   self.get_candle_close_price())
        elif Util.is_candle_type_anonymous(cdl_typ):
            rsl = From.from_prices_to_dist_between(self.get_candle_open_price(),
                                                   self.get_candle_low_price())

        return rsl

# __
    @staticmethod
    def get_cdl_type(cdl: Candle) -> Eaenum.CandleTyp:
        """ get Candle type
        :param cdl:
        :return: CandleTyp
        """
        rsl: Eaenum.CandleTyp

        _open = cdl.get_candle_open_price()
        close = cdl.get_candle_close_price()

        if close > _open:
            rsl = Eaenum.CandleTyp.Bullish

        elif _open > close:
            rsl = Eaenum.CandleTyp.Bearish

        elif _open == close:
            rsl = Eaenum.CandleTyp.anonymous

        else:
            rsl = Eaenum.CandleTyp.CdlNone

        return rsl

# __
    @staticmethod
    def get_cdl_current_tickprice(_pair: str = None,
                                  trd_mod: Eaenum.TradeMode = None,
                                  trd_direction: Eaenum.TrdDirection = Eaenum.TrdDirection) -> float:
        """ get current Tick Price
        :return: float
        """
        rsl: float

        if Util.is_null_string(_pair):
            _pair = Pair.get_symbol()

        if Util.is_none_(trd_mod):
            trd_mod = Pair.get_trading_mode()

        # Call To Interface #
        rsl = MarketBridge.i_get_candle_current_tick_price(_pair, trd_mod, trd_direction)    # must be normalised

        return rsl

# __
    def is_null_candle(self) -> bool:
        """ is This Candle Null Candle ?
        :return: bool
        """
        rsl = False

        if self.get_candle_position() == -1:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_null_candle_(_cdl: Candle) -> bool:
        """ is Null Candle ?
        :param _cdl:
        :return: bool
        """
        rsl = False

        if _cdl == Candle.get_null_candle():
            rsl = True

        return rsl

# __
    @staticmethod
    def get_null_candle() -> __class__:
        """ get Null Candle _object
        :return: Candle object
        """
        rsl = Candle(_pos=-1)

        return rsl

# __
    @staticmethod
    def get_cdl_according_to_another_by_position(_cdl_pos: int, target_pos: int) -> __class__:                 # <---
        """ get Candle _According To Another by Position
        :return: Candle object
        """
        rsl: Candle

        target_pos = _cdl_pos + target_pos

        # get Candle Object by right position
        rsl = Candle(_pos=target_pos)

        return rsl

# __
    @staticmethod
    def get_cdl_according_to_another_by_position_forward(_cdl_pos: int, target_pos: int) -> __class__:          # --->
        """ get Candle _According To Another by position _Forward
        :param _cdl_pos:
        :param target_pos:
        :return: Candle object
        """
        rsl: Candle

        target_pos = _cdl_pos - target_pos
        if target_pos < 0:
            rsl = Candle.get_null_candle()
            return rsl

        # get Candle Object by right position
        rsl = Candle(_pos=target_pos)

        return rsl

# __
    @staticmethod
    def get_cdl_info_by_datetime(_dt: dt.datetime, _timeframe: Eaenum.TimeFrames, _symbol: str) -> list:
        """ get Candle Info _by Datetime
        :param _dt:
        :param _timeframe:
        :param _symbol:
        :return: []
        """
        rsl: list

        # Call To Interface #
        rsl = MarketBridge.i_get_candle_info_by_datetime(_dt=_dt,
                                                         _timeframe=_timeframe,
                                                         _symbol=_symbol)

        return rsl

# __
    @staticmethod
    def get_cdl_info_by_position(_pos: int, _timeframe: Eaenum.TimeFrames, _symbol: str) -> list:
        """ get Candle Info _by position
        :param _pos:
        :param _timeframe:
        :param _symbol:
        :return: []
        """
        rsl: list

        # Call To Interface #
        rsl = MarketBridge.i_get_candle_info_by_position(_pos=_pos,
                                                         _timeframe=_timeframe,
                                                         _symbol=_symbol)

        return rsl

# --- END CANDLE OBJECT ---#


class Bar(object):
    """
    Advanced Class for Candle
    """
    m_candle: Candle

    def __init__(self, cdl_: Candle):
        self.set_candle(cdl_)

# ........... getters-setters
    def get_candle(self):
        return self.m_candle

    def set_candle(self, cdl_: Candle):
        self.m_candle = cdl_
# ...........

# __
    def isbar_highprice_differentof_low(self) -> bool:
        """ is Bar High price _different Of Low ?
        :return: bool
        """
        rsl = False

        High = self.get_candle().get_candle_high_price()
        Low = self.get_candle().get_candle_low_price()

        if not(High == Low):
            rsl = True

        return rsl

# __
    def isbar_openprice_differentof_close(self) -> bool:
        """ is Bar Open price _different Of Close ?
        :return: bool
        """
        rsl = False

        Open = self.get_candle().get_candle_open_price()
        Close = self.get_candle().get_candle_close_price()

        if not(Open == Close):
            rsl = True

        return rsl

# __
    @staticmethod
    def isbar_normalbar_happearedafter_lastdeviation() -> bool:
        """ is Normal Bar _Happeared After Last Deviation Bar ?
        :return: bool
        """
        rsl: bool  # = False

        rsl = Bar.isbar_normalbar_happearedafter_deviation()

        return rsl

# __
    @staticmethod
    def isbar_normalbar_happearedafter_deviation(dv_bar: Candle = None) -> bool:
        """ is Normal Bar _Happeared After Deviation Bar ?
        :param dv_bar
        :return: bool
        """
        rsl = False

        if dv_bar is None:
            dv_bar = Saver.get_last_deviation_bar_saved()

        bar = Bar.getbar_next_normalbar_afterdeviation(dv_bar)

        if Candle.is_null_candle_(bar):
            rsl = True

        return rsl

# __
    @staticmethod
    def getbar_next_normalbar_afterdeviation(dv_cdl: Candle) -> Candle:
        """ get Next Normal Bar After Deviation
        :param dv_cdl
        :return: Candle
        """
        rsl: Candle = Candle.get_null_candle()

        # let's search inside the next 5 bars if normal bar occured
        for i in range(5):
            target_pos = i+1
            normalCdl = Candle.get_cdl_according_to_another_by_position_forward(dv_cdl.get_candle_position(),
                                                                                target_pos)

            # when we have a little Bar than deviation Bar
            if normalCdl.get_candle_full_size < dv_cdl.get_candle_full_size:
                rsl = normalCdl
                break

        return rsl

# __
    @staticmethod
    def get_last_deviation_bar_happeared() -> Candle:
        """ get last Deviation Bar Happeared
        :return: Candle
        """
        rsl: Candle

        if Bar.is_deviation_bar_happeared_now():
            rsl = Candle(_pos=0)
            Saver.save_last_deviation_bar(rsl)
        else:
            rsl = Saver.get_last_deviation_bar_saved()

        return rsl

# __
    @staticmethod
    def is_deviation_bar(bar_dt: dt.datetime) -> bool:
        """ is it Deviation Bar ?
        :param bar_dt
        :return: bool
        """
        # compare bar according to two previous similar
        rsl = Bar.is_deviation_bar_happeared_at_datetime(bar_dt)

        return rsl

# __
    @staticmethod
    def get_deviation_positive_higher_price(dv_bar_dt: dt.datetime) -> float:
        """ get Deviation Positive Higher Price
        :param dv_bar_dt
        :return: float
        """
        rsl: float

        _cdl = Candle(_datetime=dv_bar_dt)
        dv_bar = Bar(_cdl)

        #   in the unique sens of deviation get the higher-lower price
        if dv_bar.is_deviation_higher_or_bottom() is True:
            rsl = dv_bar.get_candle().get_candle_high_price()          # get High if deviation is upper side
        else:
            rsl = dv_bar.get_candle().get_candle_low_price()           # get Low if deviation is bottom side

        return rsl

# __
    def is_deviation_higher_or_bottom(self) -> bool:
        """ is Deviation _Higher Or Bottom ?
        :return: bool
        """
        rsl = False

        High = self.get_candle().get_candle_high_price()
        Low = self.get_candle().get_candle_low_price()

        pos = self.get_candle().get_candle_position()
        former_bar = Candle(_pos=pos+1)

        if High > former_bar.get_candle_high_price():
            rsl = True
        elif Low < former_bar.get_candle_low_price():
            rsl = False

        return rsl

# __
    @staticmethod
    def isbar_last_deviation_bar_direction_upper() -> bool:
        """ is Last Deviation Bar _direction Upper ?
        :return: bool
        """
        rsl = False

        # get last deviation bar happeared
        dv_bar = Saver.get_last_deviation_bar_saved()

        # when deviation higher
        if Bar(dv_bar).is_deviation_higher_or_bottom():
            rsl = True

        return rsl

# __
    @staticmethod
    def isbar_last_deviation_bar_direction_downer() -> bool:
        """ is Last Deviation Bar _direction Downer ?
        :return: bool
        """
        rsl = False

        # when deviation higher
        if not Bar.isbar_last_deviation_bar_direction_upper():
            rsl = True

        return rsl

# __
    @staticmethod
    def is_deviation_bar_happeared_at_position(_pos: int) -> bool:
        """ is Deviation Bar _ Happeared At Position ?
        :param _pos
        :return: bool
        """
        rsl = not Bar.isbar_two_former_bars_similar_to_current(pivot_bar_pos=_pos)

        return rsl

# __
    @staticmethod
    def is_deviation_bar_happeared_at_datetime(_dt: dt.datetime) -> bool:
        """ is Deviation Bar _Happeared At datetime ?
        :param: datetime
        :return: bool
        """
        _cdl = Candle(_datetime=_dt)

        rsl = not Bar.isbar_two_former_bars_similar_to_current(pivot_bar_pos=_cdl.get_candle_position())

        return rsl

# __
    @staticmethod
    def is_deviation_bar_happeared_now() -> bool:
        """ is Deviation Bar _Happeared Now ?
        :return: bool
        """
        rsl = not Bar.isbar_two_former_bars_similar_to_current(pivot_bar_pos=0)

        return rsl

# __
    @staticmethod
    def getbar_running_when_time_occured(time_occured: dt.datetime, _timeframe: str = "") -> Candle:
        """ get the Bar Running _when time Occurred
        :param time_occured:
        :param _timeframe:
        :return: Candle
        """
        rsl: Candle

        pos = 0         # current bar as default position
        while True:
            #   let's begin recovering Candle by datetime
            c_Cdl = Candle(_pos=pos)      # don't need timeframe

            c_pos_dt = c_Cdl.get_candle_datetime()

            #   compare both datetime
            if c_pos_dt < time_occured:   # once candle open datetime is under _time occurred one have the right candle
                rsl = c_Cdl
                break

            #   increment position
            pos += 1

        return rsl

# __
    def is_price_different_from_bar_entry(self) -> bool:
        """ is Price Different from _Bar Entry ?
        :return:
        """
        rsl: bool  # = False

        _cdl = self.get_candle()

        _barEntry = _cdl.get_candle_open_price()
        _tickPrice = Candle.get_cdl_current_tickprice()

        # when Price not equal
        rsl = not self.is_price_equal(_tickPrice, _barEntry)

        return rsl

# __
    def is_price_greaterthan_bar_entry(self) -> bool:
        """ is Price greater Than _Bar Entry ?
        :return:
        """
        rsl: bool  # = False

        _cdl = self.get_candle()

        _barEntry = _cdl.get_candle_open_price()
        _tickPrice = Candle.get_cdl_current_tickprice()

        # when Price equal
        rsl = Bar.is_price_greater_than(_tickPrice, _barEntry)

        return rsl

# __
    def is_price_lowerthan_bar_entry(self) -> bool:
        """ is Price Lower Than _Bar Entry ?
        :return:
        """
        rsl: bool  # = False

        _cdl = self.get_candle()

        _barEntry = _cdl.get_candle_open_price()
        _tickPrice = Candle.get_cdl_current_tickprice()

        rsl = Bar.is_price_lower_than(_tickPrice, _barEntry)

        return rsl

# __
    @staticmethod
    def isbar_same_high(bar1_pos: int, bar2_pos: int) -> bool:
        """ is Bars same _High ?
        :param bar1_pos:
        :param bar2_pos:
        :return:
        """
        rsl: bool = False

        # recover bar1 Candle
        _cdl1 = Candle(_pos=bar1_pos)
        High1 = _cdl1.get_candle_high_price()  # get the High

        # recover bar2 Candle
        _cdl2 = Candle(_pos=bar2_pos)
        High2 = _cdl2.get_candle_high_price()   # get the High

        if High1 == High2:
            rsl = True

        return rsl

# __
    @staticmethod
    def isbar_same_low(bar1_pos: int, bar2_pos: int) -> bool:
        """ is Bars same _Low ?
        :param bar1_pos:
        :param bar2_pos:
        :return:
        """
        rsl = False

        # recover bar1 Candle
        _cdl1 = Candle(_pos=bar1_pos)
        Low1 = _cdl1.get_candle_low_price()   # get the Low

        # recover bar2 Candle
        _cdl2 = Candle(_pos=bar2_pos)
        Low2 = _cdl2.get_candle_low_price()   # get the Low

        if Low1 == Low2:
            rsl = True

        return rsl

# __
    @staticmethod
    def isbar_same_open(bar1_pos: int, bar2_pos: int) -> bool:
        """ is Bars same _Open ?
        :param bar1_pos:
        :param bar2_pos:
        :return:
        """
        rsl = False

        # recover bar1 Candle
        _cdl1 = Candle(_pos=bar1_pos)
        Open1 = _cdl1.get_candle_open_price()   # get the Open

        # recover bar2 Candle
        _cdl2 = Candle(_pos=bar2_pos)
        Open2 = _cdl2.get_candle_open_price()   # get the Open

        if Open1 == Open2:
            rsl = True

        return rsl

# __
    @staticmethod
    def isbar_same_close(bar1_pos: int, bar2_pos: int) -> bool:
        """ is Bars same _Close?
        :param bar1_pos:
        :param bar2_pos:
        :return:
        """
        rsl = False

        # recover bar1 Candle
        _cdl1 = Candle(_pos=bar1_pos)
        Close1 = _cdl1.get_candle_close_price()   # get the Close

        # recover bar2 Candle
        _cdl2 = Candle(_pos=bar2_pos)
        Close2 = _cdl2.get_candle_close_price()   # get the Close

        if Close1 == Close2:
            rsl = True

        return rsl

# __
    @staticmethod
    def get_market_upper_price() -> float:
        """ get Market _upper Price
        :return:
        """
        rsl: float = 0

        if not Bar.isbar_two_former_bars_similar_to_current():
            return rsl

        rsl = Candle(_pos=0).get_candle_upperprice

        return rsl

# __
    @staticmethod
    def get_market_bottom_price() -> float:
        """ get Market _bottom Price
        :return:
        """
        rsl: float = 0

        if not Bar.isbar_two_former_bars_similar_to_current():
            return rsl

        rsl = Candle(_pos=0).get_candle_bottomprice

        return rsl

# __
    @staticmethod
    def isbar_datetime_greater_than(_cdl1: Candle, _cdl2: Candle) -> bool:
        """ is Bar datetime _greater Than
        :param _cdl1:
        :param _cdl2:
        :return:
        """
        rsl: bool = False

        _dt1 = _cdl1.get_candle_datetime()
        _dt2 = _cdl2.get_candle_datetime()

        if _dt1 > _dt2:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_price_equal(_price1: float, _price2: float) -> bool:
        """ is Prices Equal
        :param _price1:
        :param _price2:
        :return:
        """
        rsl = False

        if _price1 == _price2:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_price_greater_than(_price1: float, _price2: float) -> bool:
        """ is price greater than ?
        :param _price1:
        :param _price2:
        :return:
        """
        rsl = False

        if _price1 > _price2:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_price_lower_than(_price1: float, _price2: float) -> bool:
        """ is Price Lower Than ?
        :param _price1:
        :param _price2:
        :return:
        """
        rsl = False

        if _price1 < _price2:
            rsl = True

        return rsl

# __
    def isbar_profit_margin_between_high_and_low(self) -> bool:  # VERIFY
        """ is Bar Profit Margin Between High and Low ?
        :return:
        """
        rsl: bool

        cdl = self.get_candle()

        priceHigh = cdl.get_candle_high_price()       # recover High
        priceLow = cdl.get_candle_low_price()        # recover Low

        rsl = Bar.is_price_profit_margin_between(priceHigh, priceLow)

        return rsl

# __
    def getbar_potential_margin_profit_pips_between_high_low(self) -> int:
        """ get Bar Potential Margin Profit Pips _Between High And Low
        :return:
        """
        rsl: int

        cdl = self.m_candle

        priceHigh = cdl.get_candle_high_price()  # recover High
        priceLow = cdl.get_candle_low_price()    # recover Low

        rsl = Bar.getbar_potential_margin_profit_pips_between_price(priceHigh, priceLow)

        return rsl

# __
    @staticmethod
    def is_price_profit_margin_between(_price1: float, _price2: float) -> bool:
        """ is Price Profit Margin Between ?
        :param _price1:
        :param _price2:
        :return:
        """
        rsl: bool = False

        if abs(_price1 - _price2) > 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def getbar_potential_margin_profit_pips_between_price(_price1: float, _price2: float) -> int:
        """ get Bar Potential Margin Profit Pips _Between Price
        :param _price1:
        :param _price2:
        :return:
        """
        rsl: int

        rsl = From.from_prices_to_dist_between(_price1, _price2)

        return rsl

# __
    @staticmethod
    def isbars_same_body_size(_dt1: dt.datetime, _dt2: dt.datetime) -> bool:
        """ is Bars same _body Size ?
        :param _dt1:
        :param _dt2:
        :return:
        """
        rsl = False

        _cdl1 = Candle(_datetime=_dt1)       # candle
        Cdl1_sz = _cdl1.get_candle_body_size       # size

        _cdl2 = Candle(_datetime=_dt2)       # candle
        Cdl2_sz = _cdl2.get_candle_body_size       # size

        # Size Comparison
        if Cdl1_sz == Cdl2_sz:
            rsl = True

        return rsl

# __
    @staticmethod
    def isbars_same_full_size(_dt1: dt.datetime, _dt2: dt.datetime) -> bool:
        """ is Bar same _Full Size ?
        :param _dt1:
        :param _dt2:
        :return:
        """
        rsl = False

        _cdl1 = Candle(_datetime=_dt1)        # candle
        Cdl1_sz = _cdl1.get_candle_full_size  # size

        _cdl2 = Candle(_datetime=_dt2)        # candle
        Cdl2_sz = _cdl2.get_candle_full_size  # size

        # Size Comparison
        if Cdl1_sz == Cdl2_sz:
            rsl = True

        return rsl

# __
    @staticmethod
    def isbars_two_former_bars_same_fullsize_with_current(pivot_bar_pos: int = 0) -> bool:
        """ is Bar Two Former Bar Same _Full size with the Current
        :param pivot_bar_pos:
        :return:
        """
        rsl = False

        _pos = pivot_bar_pos

        Cdl0 = Candle(_pos=_pos)               # candle
        Cdl0_sz = Cdl0.get_candle_full_size       # size

        _cdl1 = Candle(_pos=_pos+1)             # candle
        Cdl1_sz = _cdl1.get_candle_full_size       # size

        _cdl2 = Candle(_pos=_pos+2)             # candle
        Cdl2_sz = _cdl2.get_candle_full_size       # size

        # Size Comparison
        if Cdl0_sz == Cdl1_sz == Cdl2_sz:
            rsl = True

        return rsl

# __
    @staticmethod
    def isbars_two_former_bars_same_full_size(pivot_bar_pos: int = 0) -> bool:
        """ is bars Two Former Bars same Full Size ?
        :param pivot_bar_pos:
        :return:
        """
        rsl = False

        _pos = pivot_bar_pos + 1

        _cdl1 = Candle(_pos=_pos)              # candle
        Cdl1_sz = _cdl1.get_candle_full_size      # size

        _cdl2 = Candle(_pos=_pos+1)            # candle
        Cdl2_sz = _cdl2.get_candle_full_size      # size

        # Size Comparison
        if Cdl1_sz is Cdl2_sz:
            rsl = True

        return rsl

# __
    @staticmethod
    def isbars_five_former_bars_similar_bar_included(pivot_bar_pos=0) -> bool:
        """ is Bars _Five Former Bars Similars _Pivot bar Included
        :param pivot_bar_pos:
        :return:
        """
        rsl = False

        _pos = pivot_bar_pos

        # compare the bar according to the 4 former bar at that position
        rslH0_1 = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos + 1)    # comparing High
        rslH0_2 = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos + 2)    # comparing High
        rslH0_3 = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos + 3)    # comparing High
        rslH0_4 = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos + 4)    # comparing High

        rslH = rslH0_1 and rslH0_2 and rslH0_3 and rslH0_4

        rslL0_1 = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos + 1)     # comparing Low
        rslL0_2 = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos + 2)     # comparing Low
        rslL0_3 = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos + 3)     # comparing Low
        rslL0_4 = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos + 4)     # comparing Low

        rslL = rslL0_1 and rslL0_2 and rslL0_3 and rslL0_4

        # when similar bar
        if rslH and rslL:
            rsl = True  # set true

        return rsl

# __
    @staticmethod
    def isbar_three_former_bars_similar(pivot_bar_pos=0) -> bool:
        """ is Bars _Three Former Bars Similar ?
        :param pivot_bar_pos:
        :return:
        """
        rsl: bool = False
        _pos = pivot_bar_pos + 1

        # compare the bar according to the two former bar at that position
        rsl1 = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos+1)           # comparing High
        rsl1_ = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos+2)          # comparing High

        rsl2 = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos+1)            # comparing Low
        rsl2_ = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos+2)           # comparing Low

        # when similar bar
        if (rsl1 and rsl1_ and rsl2 and rsl2_) is True:
            rsl = True      # set true

        return rsl

# __
    @staticmethod
    def isbar_two_former_bars_similar(pivot_bar_pos: int = 0) -> bool:
        """ is Bar _Two Former Bars Similar ?
        :param pivot_bar_pos:
        :return:
        """
        rsl: bool = False
        _pos = pivot_bar_pos + 1

        # compare the two former bars before bar (bar excluded)
        rslH = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos+1)           # comparing High
        rslL = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos+1)            # comparing Low

        # when similar bar
        if rslH and rslL:
            rsl = True      # set true

        return rsl

# __
    @staticmethod
    def isbar_two_former_bars_similar_to_current(pivot_bar_pos: int = 0) -> bool:
        """ is Bar Two Former Bar Similar To Current ?
        :param pivot_bar_pos:
        :return: true if 2 former bars similar to the current false instead
        """
        rsl: bool = False
        _pos = pivot_bar_pos

        #   compare the bar according to the two former bar at that position
        rsl1 = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos+1)          # comparing High
        rsl1_ = Bar.isbar_same_high(bar1_pos=_pos, bar2_pos=_pos+2)         # comparing High

        rsl2 = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos+1)           # comparing Low
        rsl2_ = Bar.isbar_same_low(bar1_pos=_pos, bar2_pos=_pos+2)          # comparing Low

        #   when similar bar
        if rsl1 and rsl1_ and rsl2 and rsl2_:
            rsl = True      # set true

        return rsl

# __
    @staticmethod
    def is_current_price_upper_price() -> bool:
        """ is Current Price Upper Price ?
        :return: bool
        """
        rsl: bool = False

        #   recover current candle
        last_Cdl = Candle(_pos=0)

        #   get tick Price
        tickPrice = Candle.get_cdl_current_tickprice()

        #   check if Price Upper
        if tickPrice == last_Cdl.get_candle_upperprice:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_current_price_bottom_price() -> bool:
        """ is Current Price Bottom Price ?
        :return: bool
        """
        rsl: bool = False

        # recover current candle
        last_Cdl = Candle(_pos=0)

        # get tick Price
        tickPrice = Candle.get_cdl_current_tickprice()

        # check if Price Bottom
        if tickPrice == last_Cdl.get_candle_bottomprice:
            rsl = True

        return rsl


# --- END CLASS BAR --- #


#
class Position(object):

    m_positionTicket: str
    m_positionTyp: Eaenum.PosType
    m_positionOpenPrice: float
    m_positionOpenTime: dt.datetime
    m_positionLot: float
    m_positionTpPrice: float
    m_positionSlPrice: float
    m_posComment: str                # verify
    m_posFillTyp: Eaenum.PosFillTyp

    def __init__(self, _ticket: str, pos_filltyp: Eaenum.PosFillTyp = Eaenum.PosFillTyp.OpenPos):

        pos_openprice = MarketPosition.get_position_openprice(_ticket=_ticket)
        pos_opentime = MarketPosition.get_position_opentime(_ticket=_ticket)
        pos_typ = MarketPosition.get_position_typ(_ticket=_ticket)
        pos_lot = MarketPosition.get_position_lot(_ticket=_ticket)

        pos_tp_price = 0
        pos_sl_price = 0

        # recover tp sl price online only when future mode
        if Util.is_trade_mode_future(Eainp.EA_Trade_Mode):
            pos_tp_price = MarketPosition.get_position_tp_price(_ticket=_ticket)
            pos_sl_price = MarketPosition.get_position_sl_price(_ticket=_ticket)

# __
        _posComment = MarketPosition.get_position_comment(_ticket=_ticket)

        self._populate(_ticket, pos_typ, pos_openprice, pos_opentime, pos_lot, pos_tp_price, pos_sl_price,
                       partial_comment=_posComment, pos_filltyp=pos_filltyp)
# ............

# ............
    def _populate(self, pos_ticket: str, pos_typ: Eaenum.PosType, pos_openprice: float,
                  pos_opentime: dt.datetime, pos_lot: float,
                  pos_tp_price: float, pos_sl_price: float,
                  pos_filltyp: Eaenum.PosFillTyp = Eaenum.PosFillTyp.OpenPos,
                  partial_comment: str = ""
                  ):

        self.set_position_ticket(pos_ticket)
        self.set_position_typ(pos_typ)
        self.set_position_open_price(pos_openprice)
        self.set_position_open_time(pos_opentime)
        self.set_position_lot(pos_lot)
        self.set_position_tp_price(pos_tp_price)
        self.set_position_sl_price(pos_sl_price)

        self.set_position_fill_typ(pos_filltyp)

        self.set_position_comment(partial_comment)
# .............

# ............. getters
    def get_position_ticket(self) -> str:
        return self.m_positionTicket

    def get_position_open_price(self) -> float:
        return self.m_positionOpenPrice

    def get_position_typ(self) -> Eaenum.PosType:
        return self.m_positionTyp

    def get_position_open_time(self) -> dt.datetime:
        return self.m_positionOpenTime

    def get_position_lot(self) -> float:
        return self.m_positionLot

    def get_position_tp_price(self) -> float:
        return self.m_positionTpPrice

    def get_position_sl_price(self) -> float:
        return self.m_positionSlPrice

    def get_position_fill_typ(self) -> Eaenum.PosFillTyp:
        return self.m_posFillTyp

#
    def get_position_comment(self) -> str:
        return self.m_posComment
# ............

# ............ setters
    def set_position_ticket(self, pos_ticket: str) -> None:
        self.m_positionTicket = pos_ticket

    def set_position_open_price(self, pos_openprice: float) -> None:
        self.m_positionOpenPrice = pos_openprice

    def set_position_typ(self, pos_typ: Eaenum.PosType) -> None:
        self.m_positionTyp = pos_typ

    def set_position_open_time(self, pos_opentime: dt.datetime) -> None:
        self.m_positionOpenTime = pos_opentime

    def set_position_lot(self, pos_lot: float) -> None:
        self.m_positionLot = pos_lot

    def set_position_tp_price(self, pos_tp_price: float) -> None:
        self.m_positionTpPrice = pos_tp_price

    def set_position_sl_price(self, pos_sl_price: float) -> None:
        self.m_positionSlPrice = pos_sl_price

    def set_position_fill_typ(self, pos_filltyp: Eaenum.PosFillTyp) -> None:
        self.m_posFillTyp = pos_filltyp

# __
    def set_position_comment(self, part_comment: str):
        self.m_posComment = part_comment
# .............

# methods       # VERIFY
    def is_position_onmarket(self) -> bool:
        return MarketPosition.is_position_filled_onmarket(_ticket=self.get_position_ticket())

    def get_position_closedprice(self):
        return MarketPosition.get_position_closed_price(_ticket=self.get_position_ticket())

    def get_position_closedtime(self):
        return MarketPosition.get_position_closedtime(_ticket=self.get_position_ticket())

    def get_position_closedprofit(self):
        return MarketPosition.get_position_closed_profit(_ticket=self.get_position_ticket())
#               # VERIFY

# __
    @staticmethod
    def get_null_position() -> __class__:
        """ get Null Position
        :return:
        """
        rsl: Position

        null_Pos = Position(_ticket="", pos_filltyp=Eaenum.PosFillTyp.No)   # ??? VERIFY NULL PROCESS

        rsl = null_Pos

        return rsl

# __
    @staticmethod
    def is_position_in_profit(_ticket: str) -> bool:
        """ is Position In Profit ?
        :param _ticket:
        :return:
        """
        rsl: bool = False

        # get position Object (All info Inside)
        _pos = Position(_ticket=_ticket)

        # currentTick Price
        tickPrice = Candle.get_cdl_current_tickprice()

        # when Position Buy
        if Util.is_position_type_buy(_pos.get_position_typ()):
            if tickPrice > _pos.get_position_open_price():
                rsl = True

        # When Position Sell
        elif Util.is_position_type_sell(_pos.get_position_typ()):
            if tickPrice < _pos.get_position_open_price():
                rsl = True

        return rsl

# __
    @staticmethod
    def is_position_in_loss(_ticket: str) -> bool:
        """ is Position In Loss ?
        :param _ticket:
        :return:
        """
        rsl = False

        # get position Object (All info Inside)
        _pos = Position(_ticket=_ticket)

        # currentTick Price
        tickPrice = Candle.get_cdl_current_tickprice()

        # when Position Buy
        if Util.is_position_type_buy(_pos.get_position_typ()):
            if tickPrice < _pos.get_position_open_price():
                rsl = True

        # When Position Sell
        elif Util.is_position_type_sell(_pos.get_position_typ()):
            if tickPrice > _pos.get_position_open_price():
                rsl = True

        return rsl

# __
    @staticmethod
    def is_deviation_bar_happeared_after_trade_place(_ticket: str) -> bool:
        """ is Deviation Bar Happeared After Trade Place ?
        :param _ticket:
        :return:
        """
        rsl: bool = False

        # verify if deviation bar happeared after trade place
        dv_bar = Bar.get_last_deviation_bar_happeared()
        dv_bar_dt = dv_bar.get_candle_datetime()

        # Position
        posOpen_dt = MarketPosition.get_position_opentime(_ticket)

        if dv_bar_dt > posOpen_dt:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_zero_position_on_upperside() -> bool:
        """ is Zero Position _On Upper Side ?
        :return:
        """
        rsl: bool = False

        # get Number of Position Upper
        posNbOnUpperSide = Position.get_position_on_upperside_count()

        if posNbOnUpperSide == 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def get_position_on_upperside_count() -> int:   # VERIFY
        """ get Position On Upper Side Count
        :return:
        """
        rsl: int = 0

        # must be used when neither deviation
        if Bar.is_deviation_bar_happeared_now():
            return rsl

        # check if position exist
        if not Eagbl.cfdManaja.isPositionOnMarket():
            return rsl

        # get Upper Price
        _upperPrice = Candle(_pos=0).get_candle_upperprice

        # get All Position count (position list)
        posTotal = Eagbl.cfdManaja.getCFDPosOpen_ListCount()

        # for each positions
        for iPos in range(posTotal):
            # recover Ticket
            _ticket = From.from_index_to_ticket(iPos)         # ?

            # recover Open Price
            posOpenPrice = MarketPosition.get_position_openprice(_ticket)

            if posOpenPrice == _upperPrice:
                rsl += 1

        return rsl

# __
    @staticmethod
    def is_zero_position_on_bottomside() -> bool:
        """ is Zero Position _On Bottom Side ?
        :return:
        """
        rsl: bool = False

        # get Number of Position Bottom
        posNbOnBottomSide = Position.get_position_on_bottomside_count()

        if posNbOnBottomSide == 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def get_position_on_bottomside_count() -> int:
        """ Get Position On Bottom Side Count
        :return:
        """
        rsl: int = 0

        # must be used when neither deviation
        if Bar.is_deviation_bar_happeared_now():
            return rsl

        # check if position exist
        if not Eagbl.cfdManaja.isPositionOnMarket():
            return rsl

        # get bottom Price
        bottomPrice = Candle(_pos=0).get_candle_bottomprice

        # getAllPositionTicket (position list)
        posTotal = MarketPosition.get_position_all_count()

        # for each positions
        for iPos in range(posTotal):
            # recover Ticket
            _ticket = From.from_index_to_ticket(iPos)

            # get Open Price
            posOpenPrice = MarketPosition.get_position_openprice(_ticket)

            if posOpenPrice == bottomPrice:
                rsl += 1

        return rsl

# __
    @staticmethod
    def is_position_open_well_positioned(_ticket: str) -> bool:
        """ is Position Open Well Positioned ?
        :param _ticket:
        :return:
        """
        rsl: bool = False
        
        trd_mod = Eainp.EA_Trade_Mode
        if Util.is_trade_mode_spot(trd_mod):
            rsl = Position.is_position_open_well_positioned_spot(_ticket)
        elif Util.is_trade_mode_margin(trd_mod):
            rsl = Position.is_position_open_well_positioned_margin(_ticket)
        elif Util.is_trade_mode_future(trd_mod):
            rsl = Position.is_position_open_well_positioned_future(_ticket)

        return rsl

# __
    @staticmethod
    def is_position_open_well_positioned_spot(_ticket: str) -> bool:        # --VERIFY--------
        """ is Position Open Well Positioned Spot ?
        :param _ticket:
        :return:
        """
        rsl: bool = False
        rightPlace = 0

        # get the Btn_orderType
        Btn_orderType = MarketPosition.get_position_typ(_ticket=_ticket)

        _pivotCoinSideTyp = From.from_open_ordertyp_to_coinsidetyp(Btn_orderType)
        pivot_coin = From.from_coinsidetyp_to_coin(_pivotCoinSideTyp)

        # recover the pair
        pair = Pair()

        # when the Coin at left Side
        if pair.is_coin_left(_coin=pivot_coin):

            # when for Buying the coin Left | one are Selling the Right one
            if Position.is_position_type_buy(_ticket=_ticket):
                # get buy right place
                rightPlace = Candle.get_candle_bottomprice      # one must buying it at bottom and close above

            elif Position.is_position_type_sell(_ticket=_ticket):
                # get Sell right place
                rightPlace = Candle.get_candle_upperprice       # one must Selling it Upper and close it bottom

        # when the Coin at Right Side
        elif pair.is_coin_right(_coin=pivot_coin):
            if Position.is_position_type_buy(_ticket=_ticket):
                # get buy right place
                rightPlace = Candle.get_candle_upperprice

            elif Position.is_position_type_sell(_ticket=_ticket):
                # get Sell right place
                rightPlace = Candle.get_candle_bottomprice

        # recover pos open Price
        pos_openprice = MarketPosition.get_position_openprice(_ticket=_ticket)

        if pos_openprice == rightPlace:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_position_open_well_positioned_margin(_ticket: str) -> bool:
        """ is Position Open Well Positioned Margin ?
        :param _ticket:
        :return:
        """
        rsl: bool = False
        rightPlace: float  # = 0

        # recover the pair
        _Pair = Pair()

        # get the Btn_orderType
        Btn_orderType = MarketPosition.get_position_typ(_ticket=_ticket)

        # get the profitable coin Side
        profitableCoinSide = From.from_open_ordertyp_to_coinsidetyp(open_pos_typ=Btn_orderType)

        rightPlace = Position.get_position_rightprice_to_open_position(profitableCoinSide, Btn_orderType)

        # recover pos open Price
        pos_openprice = MarketPosition.get_position_openprice(_ticket=_ticket)

        if pos_openprice == rightPlace:
            rsl = True

        return rsl

# __
    @staticmethod
    def get_position_rightprice_to_open_position(profitableforcoin_coinside: Eaenum.CoinSideTyp,
                                                 _btn_postyp: Eaenum.PosType = Eaenum.PosType.OpBuy) -> float:
        """ get Position Right Price To Open Position
        :param profitableforcoin_coinside:
        :param _btn_postyp:
        :return:
        """
        rsl: float  # = 0
        rightPlace: float = 0
        coin_side = profitableforcoin_coinside
        pos_typ = _btn_postyp

        # ___MONEY MOVE LEFT  <---
        # OPEN FOR RIGHT SIDE or PROFITABLE FOR COIN RIGHT (BASE OF 'CAPITAL FLOW')
        if coin_side == Eaenum.CoinSideTyp.coinRight:
            if pos_typ == Eaenum.PosType.OpBuy:   # [BTN BUY]:  --> Buy first coin (ex: BUSD)
                # the right place to trade must be (BOTTOM)
                rightPlace = Candle(_pos=1).get_candle_bottomprice  # one might bought it at bottom and close above

        # ___MONEY MOVE RIGHT  --->
        elif coin_side == Eaenum.CoinSideTyp.coinLeft:  # OPEN RIGHT SIDE
            if pos_typ == Eaenum.PosType.OpSell:  # [BTN SELL]: --> Buy second coin (ex: USDT)
                # the right place to trade must be (UPPER)
                rightPlace = Candle(_pos=1).get_candle_upperprice  # one must Selling it Upper and close it bottom

        rsl = rightPlace

        return rsl

# __
    @staticmethod
    def get_position_rightprice_to_close_position(profitableforcoin_coinside: Eaenum.CoinSideTyp,
                                                  _btn_postyp: Eaenum.PosType) -> float:
        """ get Position Right Price To Close Position
        :param profitableforcoin_coinside:
        :param _btn_postyp:
        :return:
        """
        rsl: float  # = 0
        rightPlace: float = 0
        coin_side = profitableforcoin_coinside
        pos_typ = _btn_postyp

        # ___MONEY COMEBACK RIGHT  --->
        # CLOSE FOR RIGHT SIDE or PROFITABLE FOR COIN RIGHT (BASE OF 'CAPITAL FLOW'
        if coin_side == Eaenum.CoinSideTyp.coinRight:
            if pos_typ == Eaenum.PosType.OpSell:    # [BTN SELL]: buy second coin (ex: USDT)
                # the right place to close must be (UPPER)
                rightPlace = Candle(_pos=1).get_candle_upperprice  # one must Selling it Upper and close it bottom

        # ___MONEY COMEBACK LEFT  <---
        elif coin_side == Eaenum.CoinSideTyp.coinLeft:
            if pos_typ == Eaenum.PosType.OpBuy:     # [BTN BUY]:  buy first coin (ex: BUSD)
                # the right place to close must be (BOTTOM)
                rightPlace = Candle(_pos=1).get_candle_bottomprice  # one must Selling it Upper and close it bottom

        rsl = rightPlace

        return rsl

# __
    @staticmethod
    def is_position_open_well_positioned_future(_ticket: str) -> bool:  # --TO VERIFY--
        """ is Position Open Well Positioned _future
        :param _ticket:
        :return:
        """
        rsl: bool = False
        rightPlace = 0

        if Position.is_position_type_buy(_ticket=_ticket):
            # get Buy right place
            rightPlace = Candle.get_candle_bottomprice

        elif Position.is_position_type_sell(_ticket=_ticket):
            # get Sell right place
            rightPlace = Candle.get_candle_upperprice

        # recover pos open Price
        pos_openprice = MarketPosition.get_position_openprice(_ticket=_ticket)

        if pos_openprice == rightPlace:
            rsl = True

        return rsl

# __
    @staticmethod
    def get_position_bar_ongoing_when_placed(_ticket: str) -> Candle:
        """ get Position Bar On going _when Placed
        :param _ticket:
        :return:
        """
        rsl: Candle  # = Candle.get_null_candle()

        # get position Open Time
        pos_dt = MarketPosition.get_position_opentime(_ticket=_ticket)

        _tmframe = Eainp.EA_Timeframe
        # get Bar Running when time occured
        rsl = Bar.getbar_running_when_time_occured(time_occured=pos_dt, _timeframe=_tmframe)

        return rsl

# __
    @staticmethod
    def is_position_type_buy(_ticket: str) -> bool:
        """ is Position Type Buy ?
        :param _ticket:
        :return:
        """
        rsl: bool = False

        if MarketPosition.get_position_typ(_ticket=_ticket) is Eaenum.PosType.OpBuy:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_position_type_sell(_ticket: str) -> bool:
        """ is Position Type Sell ?
        :param _ticket:
        :return:
        """
        rsl: bool = False

        if MarketPosition.get_position_typ(_ticket=_ticket) == Eaenum.PosType.OpSell:
            rsl = True

        return rsl

# __
    @staticmethod
    def get_position_opposite_position(pos_typ: Eaenum.PosType) -> Eaenum.PosType:
        """ Get a Position _Opposite Position
         same as Postyp.getOpposite_PositionType()
        :param pos_typ:
        :return:
        """
        rsl: Eaenum.PosType = Eaenum.PosType.OpNo

        if pos_typ is Eaenum.PosType.OpBuy:      # when OpBuy
            rsl = Eaenum.PosType.OpSell             # set  OpSell

        elif pos_typ is Eaenum.PosType.OpSell:   # When OpSell
            rsl = Eaenum.PosType.OpBuy              # set OpBuy

        return rsl

# __
    @staticmethod
    def buy_bottom(_amount: float, _sl: float = 0, _tp: float = 0, is_isolated=True) -> bool:
        """ Buy Bottom
        :param _amount:
        :param _sl:
        :param _tp:
        :param is_isolated:
        :return:
        """
        rsl: bool = False

        # get Tick Price
        _tickPrice = Candle.get_cdl_current_tickprice()

        # get bottom Price
        _bottomPrice = Bar.get_market_bottom_price()

        if _tickPrice is _bottomPrice:
            rsl = MarketPosition.place_position(pos_typ=Eaenum.PosType.OpBuy,
                                                trd_mod=Pair.get_trading_mode(),
                                                _price=_tickPrice, _lot=_amount, _sl=_sl, _tp=_tp,
                                                is_isolated=is_isolated)

        return rsl

# __
    @staticmethod
    def buy_upper(_amount: float, _sl: float = 0, _tp: float = 0, is_isolated=True) -> bool:
        """ Buy Upper
        :param _amount:
        :param _sl:
        :param _tp:
        :param is_isolated:
        :return:
        """
        rsl: bool = False

        # get Tick Price
        _tickPrice = Candle.get_cdl_current_tickprice()

        # get Upper Price
        _upperPrice = Bar.get_market_upper_price()

        if _tickPrice is _upperPrice:
            rsl = MarketPosition.place_position(pos_typ=Eaenum.PosType.OpBuy,
                                                trd_mod=Pair.get_trading_mode(),
                                                _price=_tickPrice, _lot=_amount, _sl=_sl, _tp=_tp,
                                                is_isolated=is_isolated)

        return rsl

# __
    @staticmethod
    def sell_bottom(_amount: float, _sl: float = 0, _tp: float = 0, is_isolated=True) -> bool:
        """ Sell Bottom
        :param _amount:
        :param _sl:
        :param _tp:
        :param is_isolated:
        :return: bool
        """
        rsl: bool = False

        # get Tick Price
        _tickPrice = Candle.get_cdl_current_tickprice()

        # get bottom Price
        _bottomPrice = Bar.get_market_bottom_price()

        if _tickPrice is _bottomPrice:
            rsl = MarketPosition.place_position(pos_typ=Eaenum.PosType.OpSell,
                                                trd_mod=Pair.get_trading_mode(),
                                                _price=_tickPrice, _lot=_amount, _sl=_sl, _tp=_tp,
                                                is_isolated=is_isolated)

        return rsl

# __
    @staticmethod
    def sell_upper(_amount: float, _sl: float = 0, _tp: float = 0, is_isolated=True) -> bool:
        """ Sell Upper
        :param _amount:
        :param _sl:
        :param _tp:
        :param is_isolated:
        :return:
        """
        rsl: bool = False

        # get Tick Price
        _tickPrice = Candle.get_cdl_current_tickprice()

        # get Upper Price
        _upperPrice = Bar.get_market_upper_price()

        if _tickPrice is _upperPrice:
            rsl = MarketPosition.place_position(pos_typ=Eaenum.PosType.OpSell,
                                                trd_mod=Pair.get_trading_mode(),
                                                _price=_tickPrice, _lot=_amount, _sl=_sl, _tp=_tp,
                                                is_isolated=is_isolated)

        return rsl

# __
    @staticmethod
    def is_position_placed_at_deviation(_ticket: str) -> bool:
        """ is Position Placed At Deviation ?
        :param _ticket:
        :return:
        """
        rsl: bool = False

        the_bar = Position.get_position_bar_ongoing_when_placed(_ticket)
        bar_dt = the_bar.get_candle_datetime()

        # when it's in no case a deviation bar
        if not Bar.is_deviation_bar(bar_dt):
            return rsl      # return

        dv_topPrice = Bar.get_deviation_positive_higher_price(dv_bar_dt=bar_dt)
        pos_openprice = MarketPosition.get_position_openprice(_ticket)

        # when pos open price is the same with deviation bar positive top
        if pos_openprice == dv_topPrice:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_position_placed_before_deviation(_ticket: str) -> bool:
        """ is Position Placed Before Deviation ?
        :param _ticket:
        :return:
        """
        rsl: bool = False

        # when in no case a deviation bar happeraed after

        # when it's true that the position placed before
        if not Position.is_deviation_bar_happeared_after_trade_place(_ticket):
            rsl = True  # confirm True

        return rsl

# __
    @staticmethod
    def is_position_waiting_to_be_closed_at_profit(_ticket: str) -> bool:
        """ is Position Waiting To Be Closed At Profit ?
        :param _ticket:
        :return:
        """
        rsl: bool = False

        if Position.is_position_open_well_positioned(_ticket=_ticket) and\
                not Position.is_deviation_bar_happeared_after_trade_place(_ticket=_ticket):
            rsl = True

        return rsl

# __
    @staticmethod
    def is_position_waiting_to_be_closed_avoiding_loss_or_at_entry(_ticket: str) -> bool:
        """ is Position Waiting To Be Closed Avoiding Loss Or At Entry ?
        :param _ticket:
        :return:
        """
        rsl: bool = False

        # verify if deviation bar neither happeared after trade place
        if Position.is_deviation_bar_happeared_after_trade_place(_ticket=_ticket):
            return rsl

        # verify if entry is right according to type
        _entryRight = Position.is_position_open_well_positioned(_ticket)

        if Util.is_true(_entryRight):
            rsl = True

        return rsl

# __
    @staticmethod
    def is_position_waiting_to_be_closed_at_less_loss_when_negative_deviation(_ticket: str) -> bool:
        """ is Position Waiting To Be Closed At Less Loss _when negative Deviation
        Function used when deviation bar occured

        :param _ticket:
        :return:

        """
        rsl = False

        # require position Well placed
        if not Position.is_position_open_well_positioned(_ticket):
            return rsl

        # require deviation bar happearance -after trade place
        if not Position.is_deviation_bar_happeared_after_trade_place(_ticket=_ticket):
            return rsl

        # if normal Bar Happeared -after Deviation
        if Util.is_true(Bar.isbar_normalbar_happearedafter_deviation()):    # one need normal bar after Deviation
            rsl = True   # when all is correct

        return rsl

# __
    @staticmethod
    def is_position_waiting_to_be_closed_at_greatprofit_when_positive_deviation(_ticket: str) -> bool:    # VERIFY_____
        """ is Position Waiting To Be Closed At Great Profit When Positive Deviation ?
        Function used when deviation bar occured
        :param _ticket:
        :return:

        """
        rsl: bool = False

        # require position Well placed
        if not Position.is_position_open_well_positioned(_ticket):
            return rsl

        # require deviation bar happearance -after trade place
        if not Position.is_deviation_bar_happeared_after_trade_place(_ticket=_ticket):
            return rsl

        # recover trade favorable direction
        trd_direction = Position.get_position_trade_favorable_direction(_ticket)

        # when deviation higher
        if not (Bar.isbar_last_deviation_bar_direction_upper() and
                Util.is_trade_direction_upper(trd_direction)):
            return rsl

        # when Deviation Downer
        elif not (Bar.isbar_last_deviation_bar_direction_downer() and
                  Util.is_trade_direction_downer(trd_direction)):
            return rsl

        # must be Closed during normal Bar Happeared -after Deviation
        # if not Bar.isbar_normalbar_happearedafter_deviation():  # one do nothing while deviation bar is still present
        #    rsl = True

        return rsl

# __
    @staticmethod
    def is_position_filled(_ticket: str) -> bool:
        """ is Position Filled ?
        :param _ticket:
        :return:
        """
        rsl: bool  # = False

        rsl = MarketPosition.is_position_filled_onmarket(_ticket)

        return rsl

# __
    @staticmethod
    def is_position_waiting_to_be_closed_at_profit_when_positive_deviation(_ticket: str) -> bool:
        """ is Position Waiting To Be Closed At Profit _When Positive Deviation
        Function used when deviation bar occured

        :param _ticket:
        :return:
        """
        rsl: bool = False

        # position Well placed Doesn't matter

        # require deviation bar happearance -after trade place
        if not Position.is_deviation_bar_happeared_after_trade_place(_ticket=_ticket):
            return rsl

        # recover trade favorable direction
        trd_direction = Position.get_position_trade_favorable_direction(_ticket)

        # when deviation higher
        if not (Bar.isbar_last_deviation_bar_direction_upper() and
                Util.is_trade_direction_upper(trd_direction)):
            return rsl

        # when Deviation Downer
        elif not (Bar.isbar_last_deviation_bar_direction_downer() and
                  Util.is_trade_direction_downer(trd_direction)):
            return rsl

        # require normal Bar Happeared -after Deviation
        if not Bar.isbar_normalbar_happearedafter_deviation():  # one do nothing while deviation bar is still present
            rsl = True

        return rsl

# __
    @staticmethod
    def get_position_trade_favorable_direction(_ticket: str) -> Eaenum.TrdDirection:
        """ get Position Trade Favorable Direction
        :param _ticket:
        :return:
        """
        rsl: Eaenum.TrdDirection

        # get Position Type
        open_pos_typ = MarketPosition.get_position_typ(_ticket)

        # trade Direction
        _trdDirect = From.from_open_btntyp_to_profitable_direction(open_pos_typ)

        rsl = _trdDirect

        return rsl

# __
    @staticmethod
    def close_position_opened(_ticket: str) -> bool:
        """ Close Position Opened
        :param _ticket:
        :return:
        """
        rsl: bool = False

        # close Merely At Profit
        if Position.is_position_waiting_to_be_closed_at_profit(_ticket):
            rsl = Position.close_at_profit(_ticket=_ticket)

        # close At Entry
        elif Position.is_position_waiting_to_be_closed_avoiding_loss_or_at_entry(_ticket):
            rsl = Position.close_at_entry(_ticket=_ticket)

        # Close At Less Loss when Negative deviation
        elif Position.is_position_waiting_to_be_closed_at_less_loss_when_negative_deviation(_ticket):
            rsl = Position.close_at_less_loss(_ticket=_ticket)

        # close At Profit when Positive deviation
        elif Position.is_position_waiting_to_be_closed_at_profit_when_positive_deviation(_ticket):
            rsl = Position.close_at_profit_when_positive_deviation(_ticket=_ticket)

        # close At Great Profit When Positive deviation
        elif Position.is_position_waiting_to_be_closed_at_greatprofit_when_positive_deviation(_ticket):
            rsl = Position.close_at_great_profit_when_positive_deviation(_ticket=_ticket)

        # close At Deviation
        elif Position.is_position_placed_at_deviation(_ticket):
            rsl = Position.close_at_deviation(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def close_at_less_loss(_ticket: str) -> bool:
        """ Close At Less Loss
        :param _ticket:
        :return:
        """
        rsl: bool = False

        if not Position.is_deviation_bar_happeared_after_trade_place(_ticket=_ticket):
            return rsl

        # last deviation bar
        dvbar = Bar.get_last_deviation_bar_happeared()

        # get Normal Candle After Deviation
        normalCdl_after = Bar.getbar_next_normalbar_afterdeviation(dv_cdl=dvbar)

        # return when null Candle
        if normalCdl_after.is_null_candle():
            return rsl

        # normal High&Low
        nHigh = normalCdl_after.get_candle_upperprice
        nLow = normalCdl_after.get_candle_bottomprice

        # get Entry Price
        _posEntry = MarketPosition.get_position_openprice(_ticket=_ticket)

        # dist entry to high | dist entry to low
        _dist_entryToH = From.from_prices_to_dist_between(_posEntry, nHigh)
        _dist_entryToL = From.from_prices_to_dist_between(_posEntry, nLow)

        # get less Loss Price
        _lessLossPrice: float = 0

        if _dist_entryToH < _dist_entryToL:
            _lessLossPrice = _dist_entryToH
        elif _dist_entryToL < _dist_entryToH:
            _lessLossPrice = _dist_entryToL

        # deviation positive higher Price
        dv_posHigherPrice = Bar.get_deviation_positive_higher_price(dv_bar_dt=dvbar.get_candle_datetime())

        # tick Price
        _tickPrice = Candle.get_cdl_current_tickprice()

        # _tickPrice must be != of positive higer Price
        if _tickPrice == dv_posHigherPrice:
            return rsl

        # if all is right, let's go to last confirmation and Close Order
        if _tickPrice == _lessLossPrice:
            MarketPosition.close_position_or_order(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def close_at_entry(_ticket: str) -> bool:
        """ Close At Entry
        :param _ticket:
        :return:
        """
        rsl: bool = False

        # get Entry Price
        _posEntry = MarketPosition.get_position_openprice(_ticket=_ticket)

        _tickPrice = Candle.get_cdl_current_tickprice()

        if _tickPrice == _posEntry:
            rsl = MarketPosition.close_position_or_order(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def close_at_profit(_ticket: str) -> bool:
        """ Close At Profit
        :param _ticket:
        :return:
        """
        rsl: bool  # = False

        rsl = MarketPosition.close_at_profit(_ticket)

        return rsl

# __
    @staticmethod
    def close_at_profit_when_positive_deviation(_ticket: str) -> bool:
        """ Close At Profit _When Positive Deviation
        :param _ticket:
        :return:
        """
        rsl: bool = False

        # get last deviation Bar
        last_dv_bar = Bar.get_last_deviation_bar_happeared()

        # get dev Pos Top Price
        pos_devPosTopPrice = Bar.get_deviation_positive_higher_price(dv_bar_dt=last_dv_bar.get_candle_datetime())

        # get Tick Price
        _tickPrice = Candle.get_cdl_current_tickprice()

        if _tickPrice == pos_devPosTopPrice:
            rsl = MarketPosition.close_position_or_order(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def close_at_great_profit_when_positive_deviation(_ticket: str) -> bool:
        """ Close At Great Profit _When Positive Deviation
        :param _ticket:
        :return:
        """
        rsl: bool = False

        # get last deviation Bar
        last_dv_bar = Bar.get_last_deviation_bar_happeared()

        # get dev Top greater Price
        pos_devPosTopPrice = Bar.get_deviation_positive_higher_price(dv_bar_dt=last_dv_bar.get_candle_datetime())

        # get Tick Price
        _tickPrice = Candle.get_cdl_current_tickprice()

        if _tickPrice == pos_devPosTopPrice:
            rsl = MarketPosition.close_position_or_order(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def close_at_deviation(_ticket: str) -> bool:
        """ Close At Deviation
        :param _ticket:
        :return:
        """
        rsl: bool  # = False

        rsl = Position.close_at_entry(_ticket=_ticket)

        return rsl

#  --- END CLASS POSITION ---  #


class CFDPosition(object):

    # mode type
    m_posTrdMod: Eaenum.TradeMode
    m_posSymbol: str
    m_posBtnOrdTyp: Eaenum.PosType
    m_posProfitCoinSide: Eaenum.CoinSideTyp
    m_posTrdDirection: Eaenum.TrdDirection

    # opening
    m_posTicket_Opening: str
    m_posOpenLot: float
    m_posInvestedLot: float
    m_posOpenPrice: float
    m_posOpen_dt: dt.datetime
    m_posStopLoss: float
    m_posTakeProfit: float
    m_posComment: str
    m_posMagic: int

    # closing
    m_posTicket_Closing: str
    m_posClose_dt: dt.datetime
    m_posClosePrice: float
    m_posClosedProfitLoss: float

# getters
    def get_pos_trade_mode(self):
        return self.m_posTrdMod

    def get_pos_symbol(self):
        return self.m_posSymbol

    def get_pos_btnorder_type(self):
        return self.m_posBtnOrdTyp

    def get_pos_profit_coinside(self):
        return self.m_posProfitCoinSide

    def get_pos_trade_direction(self):
        return self.m_posTrdDirection

# __
    def get_pos_ticket_opening(self):
        return self.m_posTicket_Opening

    def get_pos_openlot(self):
        return self.m_posOpenLot

    def get_pos_invested_lot(self):
        return self.m_posInvestedLot

    def get_pos_openprice(self):
        return self.m_posOpenPrice

    def get_pos_open_datetime(self):
        return self.m_posOpen_dt

    def get_pos_stoploss(self):
        return self.m_posStopLoss

    def get_pos_takeprofit(self):
        return self.m_posTakeProfit

    def get_pos_comment(self):
        return self.m_posComment

    def get_pos_magic(self):
        return self.m_posMagic

# __
    def get_pos_ticket_closing(self):
        return self.m_posTicket_Closing

    def get_pos_close_datetime(self):
        return self.m_posClose_dt

    def get_pos_closeprice(self):
        return self.m_posClosePrice

    def get_pos_closed_profitloss(self):
        return self.m_posClosedProfitLoss

# __
    def get_position_opening(self) -> Position:    # --TO CODE--
        rsl: Position

        # get null position
        _pos = Position.get_null_position()

        # fill infos inside
        _pos.set_position_ticket(pos_ticket=self.get_pos_ticket_opening())
        _pos.set_position_open_price(pos_openprice=self.get_pos_openprice())
        _pos.set_position_open_time(pos_opentime=self.get_pos_open_datetime())
        _pos.set_position_typ(pos_typ=self.get_pos_btnorder_type())
        _pos.set_position_lot(pos_lot=self.get_pos_openlot())
        _pos.set_position_comment(part_comment=self.get_pos_comment())

        _pos.set_position_sl_price(pos_sl_price=self.get_pos_stoploss())
        _pos.set_position_tp_price(pos_tp_price=self.get_pos_takeprofit())

        _pos.set_position_fill_typ(pos_filltyp=Eaenum.PosFillTyp.OpenPos)

        rsl = _pos

        return rsl

# __
    def get_position_closing(self) -> Position:    # --TO CODE--
        rsl: Position

        # get null position
        _pos = Position.get_null_position()

        # fill infos inside
        _pos.set_position_ticket(pos_ticket=self.get_pos_ticket_closing())
        _pos.set_position_open_price(pos_openprice=self.get_pos_closeprice())
        _pos.set_position_open_time(pos_opentime=self.get_pos_open_datetime())
        _pos.set_position_typ(pos_typ=self.get_pos_btnorder_type().getOpposite_PositionType())
        _pos.set_position_lot(pos_lot=self.get_pos_invested_lot())
        _pos.set_position_fill_typ(pos_filltyp=Eaenum.PosFillTyp.ClosePos)

        rsl = _pos

        return rsl
#

# setters
    def set_pos_trade_mode(self, trd_mod: Eaenum.TradeMode):
        self.m_posTrdMod = trd_mod

    def set_pos_symbol(self, _symbol: str):
        self.m_posSymbol = _symbol

    def set_pos_btnorder_type(self, btn_ord_typ: Eaenum.PosType):
        self.m_posBtnOrdTyp = btn_ord_typ

    def set_pos_profit_coinside(self, profit_coinside: Eaenum.CoinSideTyp):
        self.m_posProfitCoinSide = profit_coinside

    def set_pos_trade_direction(self, trd_direction: Eaenum.TrdDirection):
        self.m_posTrdDirection = trd_direction

# __
    def set_pos_ticket_opening(self, _ticket: str):
        self.m_posTicket_Opening = _ticket

    def set_pos_openlot(self, _lot: float):
        self.m_posOpenLot = _lot

    def set_pos_invested_lot(self, _lot: float):
        self.m_posInvestedLot = _lot

    def set_pos_openprice(self, _price: float):
        self.m_posOpenPrice = _price

    def set_pos_open_datetime(self, dt_: dt.datetime):
        self.m_posOpen_dt = dt_

    def set_pos_stoploss(self, _sl_price: float):
        self.m_posStopLoss = _sl_price

    def set_pos_takeprofit(self, _tp_price: float):
        self.m_posTakeProfit = _tp_price

    def set_pos_comment(self, _comment: str):
        self.m_posComment = _comment

    def set_pos_magic(self, _magic: int):
        self.m_posMagic = _magic

# __
    def set_pos_ticket_closing(self, _ticket: str):
        self.m_posTicket_Closing = _ticket

    def set_pos_close_datetime(self, _dt: dt.datetime):
        self.m_posClose_dt = _dt

    def set_pos_closeprice(self, _price: float):
        self.m_posClosePrice = _price

    def set_pos_closed_profitloss(self, _value: float):
        self.m_posClosedProfitLoss = _value

# __
    def set_position_closing(self, _pos: Position):

        posCloseTicket = _pos.get_position_ticket()
        posClose_dt = _pos.get_position_closedtime()
        posClosePrice = _pos.get_position_open_price()
        posClosePnL = From.from_coinbuy_to_coin_amount_comeback_with_profitloss(
            close_price=posClosePrice,
            open_pos_lot=self.get_pos_openprice(),
            coin_origin_side=self.get_pos_profit_coinside())

        self.set_pos_ticket_closing(_ticket=posCloseTicket)
        self.set_pos_close_datetime(_dt=posClose_dt)
        self.set_pos_closeprice(_price=posClosePrice)
        self.set_pos_closed_profitloss(_value=posClosePnL)

# __
    def set_position_opening(self, _pos: Position):

        _posBtn_ordtyp = _pos.get_position_typ()
        _posTicket = _pos.get_position_ticket()
        _posOpenPrice = _pos.get_position_open_price()
        _posOpenTime = _pos.get_position_open_time()
        _posLot = _pos.get_position_lot()

        _posComment = _pos.get_position_comment()

        _symbol = Pair.get_symbol()
        trd_mod = Pair.get_trading_mode()

        _coinSideTyp = From.from_open_ordertyp_to_coinsidetyp(open_pos_typ=_posBtn_ordtyp)
        trd_direction = From.from_open_btntyp_to_profitable_direction(open_pos_typ=_posBtn_ordtyp)

        _pos_invLot = From.from_coinbuy_to_coin_amount_invested(open_price=_posOpenPrice,
                                                                _lot=_posLot,
                                                                coin_origin_side=_coinSideTyp)
        _posMagic = Eainp.EA_MagicNumber

        self.set_pos_trade_mode(trd_mod=trd_mod)
        self.set_pos_symbol(_symbol=_symbol)
        self.set_pos_btnorder_type(btn_ord_typ=_posBtn_ordtyp)
        self.set_pos_profit_coinside(profit_coinside=_coinSideTyp)
        self.set_pos_trade_direction(trd_direction=trd_direction)

        self.set_pos_ticket_opening(_ticket=_posTicket)
        self.set_pos_openlot(_lot=_pos.get_position_lot())
        self.set_pos_invested_lot(_lot=_pos_invLot)
        self.set_pos_openprice(_price=_posOpenPrice)
        self.set_pos_open_datetime(dt_=_posOpenTime)

        self.set_pos_stoploss(_sl_price=_pos.get_position_sl_price())   # recover sl and tp of Pos: must be updated
        self.set_pos_takeprofit(_tp_price=_pos.get_position_tp_price())  # before sent to object (not required if futur)

        self.set_pos_comment(_comment=_posComment)
        self.set_pos_magic(_magic=_posMagic)
# ..............

# __
    def __init__(self, o_pos: Position, c_pos: Position = None) -> None:
        self.set_position_opening(o_pos)

        if not Util.is_none_(c_pos):
            self.set_position_closing(c_pos)
        else:
            null_pos = Position.get_null_position()
            self.set_position_closing(null_pos)

# __
    def __init__(self, btn_ordtyp: Eaenum.PosType, _ticket: str, _lot: float, open_price: float = 0,
                 open_dt: dt.datetime = None, sl_price: float = 0, tp_price: float = 0, _comment: str = "",
                 _magic: int = 0, close_ticket: str = "", close_dt: dt.datetime = None, close_price: float = 0):

        _symbol = Pair.get_symbol()
        trd_mod = Pair.get_trading_mode()
        _coinSideTyp = From.from_open_ordertyp_to_coinsidetyp(open_pos_typ=btn_ordtyp)
        trd_direction = From.from_open_btntyp_to_profitable_direction(open_pos_typ=btn_ordtyp)

        _invLot = From.from_coinbuy_to_coin_amount_invested(open_price=open_price, _lot=_lot,
                                                            coin_origin_side=_coinSideTyp)

        close_pnl = From.from_coinbuy_to_coin_amount_comeback_with_profitloss(close_price=close_price,
                                                                              open_pos_lot=open_price,
                                                                              coin_origin_side=_coinSideTyp)

        self._populate(trd_mod=trd_mod, profit_coinside=_coinSideTyp, btn_ord_typ=btn_ordtyp,
                       _symbol=_symbol, trd_direction=trd_direction,
                       _ticket=_ticket, _lot=_lot, open_price=open_price, open_dt=open_dt,
                       sl_price=sl_price, tp_price=tp_price, _comment=_comment, _magic=_magic,
                       close_ticket=close_ticket, close_dt=close_dt, close_price=close_price,
                       close_pnl=close_pnl, invested_lot=_invLot)

# __
    def _populate(self, trd_mod: Eaenum.TradeMode, profit_coinside: Eaenum.CoinSideTyp,
                  _symbol: str, btn_ord_typ: Eaenum.PosType, trd_direction: Eaenum.TrdDirection,
                  _ticket: str, _lot: float, invested_lot: float, open_price: float,
                  open_dt: dt.datetime, sl_price: float, tp_price: float, _comment: str,
                  _magic: int, close_ticket: str, close_dt: dt.datetime, close_price: float,
                  close_pnl: float):

        self.set_pos_trade_mode(trd_mod=trd_mod)
        self.set_pos_symbol(_symbol=_symbol)
        self.set_pos_btnorder_type(btn_ord_typ=btn_ord_typ)
        self.set_pos_profit_coinside(profit_coinside=profit_coinside)
        self.set_pos_trade_direction(trd_direction=trd_direction)

        self.set_pos_ticket_opening(_ticket=_ticket)
        self.set_pos_openlot(_lot=_lot)
        self.set_pos_invested_lot(_lot=invested_lot)
        self.set_pos_openprice(_price=open_price)
        self.set_pos_open_datetime(dt_=open_dt)
        self.set_pos_stoploss(_sl_price=sl_price)
        self.set_pos_takeprofit(_tp_price=tp_price)
        self.set_pos_comment(_comment=_comment)
        self.set_pos_magic(_magic=_magic)

        self.set_pos_ticket_closing(_ticket=close_ticket)
        self.set_pos_close_datetime(_dt=close_dt)
        self.set_pos_closeprice(_price=close_price)
        self.set_pos_closed_profitloss(_value=close_pnl)

# __
    @staticmethod
    def get_null_cfdposition() -> __class__:
        """ return a Null Cfd Position
        :return:
        """
        rsl: CFDPosition
        _cfdPos = CFDPosition(btn_ordtyp=Eaenum.PosType.OpNo, _ticket="", _lot=0, open_price=0, open_dt=None)

        rsl = _cfdPos

        return rsl

# __
    def is_null_cfdposition(self) -> bool:
        """ know if position is null
        :return bool:
        """
        rsl: bool = False

        if self.get_pos_ticket_opening() is "":
            rsl = True

        return rsl

# __
    def is_pos_opened(self) -> bool:
        """ is Position Opened ?
        know if position is currently Opened
        :return bool:
        """
        rsl: bool = False

        if self.get_pos_ticket_opening() is not "":
            rsl = True

        return rsl

# __
    def is_pos_closed(self) -> bool:
        """ is Position Closed ?
        know if position is currently Closed
        :return bool:
        """
        rsl: bool = False

        if self.get_pos_ticket_closing() is not "":
            rsl = True

        return rsl

# __
    def pos_current_market_tickprice(self) -> float:
        """ know current Market Tick Price of the Position Symbol
        :return float:
        """
        rsl: float

        rsl = Candle.get_cdl_current_tickprice(_pair=self.m_posSymbol)

        return rsl

# __
    def pos_current_profit(self) -> float:
        """ know current Position Profit Situation on Market  -- Tailored for Opened CFD Position
        :return float:
        """

        # get Tick Price
        _tickPrice = self.pos_current_market_tickprice()
        _openLot = self.get_pos_openlot()
        _originSide = self.get_pos_profit_coinside()

        rsl = From.from_coinbuy_to_coin_amount_comeback_with_profitloss(close_price=_tickPrice,
                                                                        open_pos_lot=_openLot,
                                                                        coin_origin_side=_originSide)
        return rsl

# __  # VERIFY   or  cfdPos.getPosClosedProfitLoss() ?
    def pos_deal_profit(self) -> float:
        """ CFD Position Deal Profit  -- Tailored for Closed CFD Position
        :return: float
        """
        rsl: float = 0

        if not self.is_pos_closed():
            return rsl

        # get closed Price
        _closedPrice = self.m_posClosePrice       # ?
        _openLot = self.get_pos_openlot()
        _originSide = self.get_pos_profit_coinside()

        rsl = From.from_coinbuy_to_coin_amount_comeback_with_profitloss(close_price=_closedPrice,
                                                                        open_pos_lot=_openLot,
                                                                        coin_origin_side=_originSide)
        return rsl

# __
    @staticmethod
    def is_pos_deal_winner(_pos: CFDPosition) -> bool:   # VERIFY
        """ know if a Opened Position is winner or loser (In Profit or Loss)
        :param _pos:
        :return bool:
                """
        rsl: bool = False

        # return if Position closed
        if _pos.is_pos_closed():
            return rsl

        if _pos.posCurrentProfit() > 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_pos_his_deal_winner(_pos: CFDPosition) -> bool:
        """ know if a History Deal was winner or loser (In Profit or Loss)
        :param _pos:
        :return bool:
        """
        rsl: bool = False

        # return if Position not yet closed
        if not _pos.is_pos_closed():
            return rsl

        # when Position Buy
        if Util.is_position_type_buy(_pos.get_pos_btnorder_type()):
            if _pos.get_pos_closeprice() > _pos.get_pos_openprice():
                rsl = True

        # When Position Sell
        elif Util.is_position_type_sell(_pos.get_pos_btnorder_type()):
            if _pos.get_pos_closeprice() < _pos.get_pos_openprice():
                rsl = True

        return rsl

#  --- END CLASS CFD POSITION ---  #


class CFDManager(object):

    m_openPositionList: list        # list of CFDPosition
    m_historyPositionList: list     # History list of Filled CFDPosition

    def __init__(self):

        # let's init content
        self.clear_cfdpos_list(list_src=Eaenum.CFDPosListSrc.OpenPosList)
        self.clear_cfdpos_list(list_src=Eaenum.CFDPosListSrc.HistoryPosList)

# __
    @classmethod
    def get_cfdpos_list_count(cls, list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> int:
        """ get CFD Position List count according to Specified List source
        :param list_src:
        :return: int
        """
        rsl: int = 0

        if Util.is_cfdpos_list_src_from_open_poslist(list_src):
            rsl = len(cls.m_openPositionList)
        elif Util.is_cfdpos_list_src_from_history_list(list_src):
            rsl = len(cls.m_historyPositionList)

        return rsl

# __
    @classmethod
    def get_cfdpos_list(cls, list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> list:
        """ get CFD Position according to Specified List source
        :param list_src:
        :return: []
        """
        rsl: list = []

        if Util.is_cfdpos_list_src_from_open_poslist(list_src):
            rsl = cls.m_openPositionList
        elif Util.is_cfdpos_list_src_from_history_list(list_src):
            rsl = cls.m_historyPositionList

        return rsl

# __
    @classmethod
    def clear_cfdpos_list(cls, list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> None:
        """ clear a CFD Position to Specified List source
        :param list_src
        :return: None
        """
        if Util.is_cfdpos_list_src_from_open_poslist(list_src):
            cls.m_openPositionList.clear()
        elif Util.is_cfdpos_list_src_from_history_list(list_src):
            cls.m_historyPositionList.clear()

# __
    @classmethod
    def add_cfdpos_to_list(cls, cfd_pos: CFDPosition,
                           list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> None:
        """ add CFD Position to Specified List source
        :param cfd_pos:
        :param list_src:
        :return: None
        """
        if Util.is_cfdpos_list_src_from_open_poslist(list_src):
            cls.m_openPositionList.append(cfd_pos)
        elif Util.is_cfdpos_list_src_from_history_list(list_src):
            cls.m_historyPositionList.append(cfd_pos)

# __
    @classmethod     # VERIFY
    def remove_cfdpos_to_list(cls, _ticket: str,
                              list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> bool:
        """ remove CFD Position To List
            return true if found and removed, false if not
        :return: bool
        """
        rsl: bool

        _pos = cls.get_cfdpos_inside_list(_ticket, list_src)
        rsl = Util.remove_position_to_list(_pos, cls.get_cfdpos_list(list_src))

        return rsl

# __
    @classmethod
    def get_cfdpos_inside_list_index(cls, _ticket: str,
                                     list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> int:
        """ get CFD Position inside List _Index according to Specified List source
        :param _ticket:
        :param list_src:
        :return: int
        """
        rsl: int

        _cfdPos = cls.get_cfdpos_inside_list(_ticket, list_src)                      # First get cfdPos
        rsl = Util.get_position_inside_list_index(_cfdPos, cls.get_cfdpos_list(list_src))     # seek in inside list

        return rsl

# __
    @classmethod
    def get_cfdpos_inside_list(cls, _ticket: str,
                               list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> CFDPosition:
        """ get CFD Position inside the list according to Specified List source
        :param _ticket:
        :param list_src:
        :return: CFDPosition
        """
        rsl: CFDPosition = CFDPosition.get_null_cfdposition()

        PosList = cls.get_cfdpos_list(list_src)

        for _pos in PosList:
            if _pos.get_pos_ticket_opening() == _ticket:
                rsl = _pos
                break

        return rsl

# __
    @classmethod
    def get_cfdpos_list_size(cls, list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> int:
        """ __same as list count__
            get CFD Position List size according to Specified List source
        :param list_src:
        :return: int
        """
        return cls.get_cfdpos_list_count(list_src)

# __
    @classmethod
    def is_cfdpos_list_empty(cls, list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> bool:
        """ is CFD Position List Empty ?
        :param list_src:
        :return: bool
        """
        rsl: bool = False

        if cls.get_cfdpos_list_size(list_src) == 0:
            rsl = True

        return rsl

# __
    @classmethod
    def get_cfdpos_list_latest_index(cls, list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> int:
        """ get CFD Position List Latest Index according to Specified List source
        :return: int
        """
        rsl: int

        rsl = cls.get_cfdpos_list_size(list_src) - 1

        return rsl

# __
    @classmethod
    def get_cfdpos_inside_list_by_index(cls, _index: int,
                                        list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList
                                        ) -> CFDPosition:
        """ get CFD Position Inside List by Index according to Specified List source
        :param _index:
        :param list_src:
        :return: CFDPosition
        """
        pos_list = cls.get_cfdpos_list(list_src)

        return pos_list[_index]

# __
    @classmethod
    def is_cfdpos_still_onmarket_execution(cls, open_ticket: str) -> bool:
        """ is CFD Position Still On Market Execution ?
        :param open_ticket:
        :return: bool
        """
        rsl: bool = False

        _cfdPos = cls.get_cfdpos_inside_list(open_ticket, Eaenum.CFDPosListSrc.OpenPosList)

        if _cfdPos.is_pos_opened() and not _cfdPos.is_pos_closed():
            rsl = True

        return rsl

# __
    @classmethod
    def is_cfdpositions_onmarket(cls) -> bool:
        """ is CFD Position _On Market ?
            check any Position existence or opening availability
        :return: bool
        """
        rsl: bool = False

        if cls.get_cfdpos_list_count(Eaenum.CFDPosListSrc.OpenPosList) == 0:
            rsl = True

        else:
            PosList = cls.get_cfdpos_list(Eaenum.CFDPosListSrc.OpenPosList)

            for _pos in PosList:
                if _pos.getPosTrdMod() is not Eainp.EA_Trade_Mode:
                    continue                                         # nothing to signal
                else:                                                # position is on market
                    rsl = True
                    break

        return rsl

# __
    @classmethod
    def toggle_closed_cfdpos_to_history(cls, pos_index_in: int) -> bool:    # VERIFY
        """ toggle Closed CFD Position To History
        :param pos_index_in:
        :return: bool
        """
        rsl: bool = False

        # find cfdPosition inside list
        cfd_Pos = cls.get_cfdpos_list(Eaenum.CFDPosListSrc.OpenPosList)[pos_index_in]

        if cfd_Pos.isNull_CFDPosition():    # CFD Position cannot be negative
            return rsl

        rsl = True

        # save position to History List
        cls.add_cfdpos_to_list(cfd_Pos, Eaenum.CFDPosListSrc.HistoryPosList)

        # remove from open pos list
        cls.remove_cfdpos_to_list(_ticket=cfd_Pos.get_pos_ticket_opening(), list_src=Eaenum.CFDPosListSrc.OpenPosList)

        return rsl

# __
    @classmethod
    def save_filled_openpos_onmarket_to_cfdposition(cls, _ticket: str, tp_price=0, sl_price=0) -> None:       # VERIFY
        """ save Filled Open Position On Market To CFD Position
        :param _ticket:
        :param tp_price:
        :param sl_price:
        :return: None
        """
        sv_Pos: CFDPosition  # = CFDPosition.get_null_cfdposition()

        #   recover infos
        _pos = Position(_ticket=_ticket)

        _pos.set_position_tp_price(tp_price)           # define right tp target
        _pos.set_position_sl_price(sl_price)           # define right sl target

        #   get CFDPosition by Opened Position
        sv_Pos = CFDPosition(o_pos=_pos)

        #   add it To List
        cls.m_openPositionList.append(sv_Pos)

# __
    @classmethod
    def get_cfdpos_all_of_listsrc(cls, list_src: Eaenum.CFDPosListSrc) -> list:
        """ get CFD Position All of Specified List source
        :param list_src:
        :return: []
        """
        rsl: list

        rsl = cls.get_cfdpos_list(list_src)  # using history list

        return rsl

# __
    @classmethod
    def get_cfdpos_all_by_magic(cls, magic_number: int,
                                list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> list:
        """ get CFD Positions All by Magic according to Specified List source
        :param magic_number:
        :param list_src:
        :return: []
        """
        rsl: list

        pos_list: list
        wantedPosList: list = []

        pos_list = cls.get_cfdpos_all_of_listsrc(list_src)

        for _pos in pos_list:
            if _pos.getPosMagic() == magic_number:
                Util.add_position_to_list(_pos, wantedPosList)

        rsl = wantedPosList

        return rsl

# __
    @classmethod
    def get_cfdpos_all_by_position(cls, pos_typ: Eaenum.PosType,
                                   list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> list:
        """ get CFD Positions All By _PositionType according to Specified List source
        :param pos_typ:
        :param list_src:
        :return: []
        """
        rsl: list

        pos_list: list
        wantedPosList: list = []

        pos_list = cls.get_cfdpos_all_of_listsrc(list_src)

        if not Util.is_position_type_opno(pos_typ):      # when posTyp Specified

            #   let's seek when Inside
            for _pos in pos_list:
                if _pos.get_pos_btnorder_type() == pos_typ:
                    Util.add_position_to_list(_pos, wantedPosList)

        else:                                        # when not
            wantedPosList = pos_list     # use and return default list

        rsl = wantedPosList

        return rsl

# __
    @classmethod
    def get_cfdpos_all_by_daterange(cls, from_dt: dt.datetime, to_dt: dt.datetime,
                                    open_pos_typ: Eaenum.PosType = Eaenum.PosType.OpNo,
                                    list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> list:
        """ get CFD Positions All By _DateRange according to Specified List source
        :param from_dt:
        :param to_dt:
        :param open_pos_typ:
        :param list_src:
        :return: []
        """
        rsl: list

        pos_list: list
        _wantedPosList: list = []

        pos_list = cls.get_cfdpos_all_by_position(open_pos_typ, list_src)   # get All By Position Type

        #   control null datetime values
        if Duration.is_null_datetime(from_dt) and not Duration.is_null_datetime(to_dt):
            if Util.is_none_(from_dt):
                from_dt = Duration.get_null_datetime()

        elif not Duration.is_null_datetime(from_dt) and Duration.is_null_datetime(to_dt):
            to_dt = Duration.get_current_time()

        #   check and get inside list by date
        for _pos in pos_list:
            if (_pos.get_pos_open_datetime() >= from_dt) and (_pos.get_pos_open_datetime() <= to_dt):
                Util.add_position_to_list(_pos, _wantedPosList)

        rsl = _wantedPosList

        return rsl

# __
    @classmethod
    def get_cfdpos_all_of_specific_day(cls, the_day_date: dt.date, open_pos_typ: Eaenum.PosType = Eaenum.PosType.OpNo,
                                       list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> list:
        """ get CFD Positions All Of Specific day according to Specified List source
        :param the_day_date:
        :param open_pos_typ:
        :param list_src:
        :return: []
        """
        rsl: list

        pos_list: list
        _wantedPosList: list = []

        pos_list = cls.get_cfdpos_all_by_position(open_pos_typ, list_src)

        for _pos in pos_list:
            if _pos.get_pos_open_datetime().date == the_day_date:
                Util.add_position_to_list(_pos, _wantedPosList)

        rsl = _wantedPosList

        return rsl

# __
    @classmethod
    def get_cfdpos_all_of_today(cls, open_pos_typ: Eaenum.PosType = Eaenum.PosType.OpNo,
                                list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList
                                ) -> list:
        """ get CFD Positions All Of Today according to Specified List source
        :param open_pos_typ:
        :param list_src:
        :return: []
        """
        rsl: list
        _wantedPosList: list = []

        today_dt = Duration.get_current_time()       # get today datetime

        _wantedPosList = cls.get_cfdpos_all_of_specific_day(today_dt.date(), open_pos_typ, list_src)

        rsl = _wantedPosList

        return rsl

# __
    @classmethod
    def get_cfdpos_all_winning(cls, from_dt: dt.datetime = None, to_dt: dt.datetime = None,
                               open_pos_typ: Eaenum.PosType = Eaenum.PosType.OpNo,
                               list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> list:
        """ get CFD Positions All Winning according to Specified List source
        :param from_dt:
        :param to_dt:
        :param open_pos_typ:
        :param list_src:
        :return: []
        """

        rsl: list

        pos_list: list
        _wantedPosList: list = []

        pos_list = cls.get_cfdpos_all_by_daterange(from_dt, to_dt, open_pos_typ, list_src)

        #   when open List proceed
        if Util.is_cfdpos_list_src_from_open_poslist(list_src):

            for _pos in pos_list:
                if CFDPosition.is_pos_deal_winner(_pos):
                    Util.add_position_to_list(_pos, _wantedPosList)

        #   when History List proceed
        elif Util.is_cfdpos_list_src_from_history_list(list_src):

            for _pos in pos_list:
                if CFDPosition.is_pos_his_deal_winner(_pos):
                    Util.add_position_to_list(_pos, _wantedPosList)

        rsl = _wantedPosList

        return rsl

# __
    @classmethod
    def get_cfdpos_all_losing(cls, from_dt: dt.datetime = None, to_dt: dt.datetime = None,
                              open_pos_typ: Eaenum.PosType = Eaenum.PosType.OpNo,
                              list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> list:
        """ get CFD Positions All Losing according to Specified List source
        :param from_dt:
        :param to_dt:
        :param open_pos_typ:
        :param list_src:
        :return: []
        """
        rsl: list

        pos_list: list
        _wantedPosList: list = []

        pos_list = cls.get_cfdpos_all_by_daterange(from_dt, to_dt, open_pos_typ, list_src)

        #   when open position List
        if Util.is_cfdpos_list_src_from_open_poslist(list_src):

            for _pos in pos_list:
                if not CFDPosition.is_pos_deal_winner(_pos):
                    Util.add_position_to_list(_pos, _wantedPosList)

        #   when History position List
        elif Util.is_cfdpos_list_src_from_history_list(list_src):

            for _pos in pos_list:
                if not CFDPosition.is_pos_his_deal_winner(_pos):
                    Util.add_position_to_list(_pos, _wantedPosList)

        rsl = _wantedPosList

        return rsl

# __
    @classmethod
    def get_cfdpos_last_closed(cls) -> CFDPosition:
        """ get CFD Position last Closed
        :return: CFDPosition
        """
        rsl: CFDPosition  # = CFDPosition.get_null_cfdposition()

        idx_ = Util.get_position_list_latest_index(cls.get_cfdpos_list(Eaenum.CFDPosListSrc.OpenPosList))

        rsl = cls.get_cfdpos_list(Eaenum.CFDPosListSrc.HistoryPosList)[idx_]

        return rsl

# __
    @classmethod
    def get_cfdpos_last_opened_onmarket(cls) -> CFDPosition:
        """ get CFD Position _Last Opened On Market
            Recover the last element inside Opened cfd position List
        :return: CFDPosition
        """
        rsl: CFDPosition  # = CFDPosition.get_null_cfdposition()

        idx_ = Util.get_position_list_latest_index(cls.get_cfdpos_list(Eaenum.CFDPosListSrc.OpenPosList))

        rsl = cls.get_cfdpos_list(Eaenum.CFDPosListSrc.OpenPosList)[idx_]

        return rsl

# __
    @classmethod
    def get_cfdpos_number_opened(cls) -> int:
        """ get CFD Position _Number Opened On Market
            Recover the Opened cfd positions inside Opened one List
        :return: int
        """
        return Util.get_positions_count(cls.get_cfdpos_list(Eaenum.CFDPosListSrc.OpenPosList))

# __
    @classmethod
    def get_cfdpos_overall_profit_loss(cls, from_dt: dt.datetime = None, to_dt: dt.datetime = None,
                                       open_pos_typ: Eaenum.PosType = Eaenum.PosType.OpNo,
                                       list_src: Eaenum.CFDPosListSrc = Eaenum.CFDPosListSrc.OpenPosList) -> float:
        """ get CFD Positions Overall Profit Loss according to Specified List source
        :param from_dt:
        :param to_dt:
        :param open_pos_typ:
        :param list_src:
        :return: float
        """
        rsl: float

        Pnl: float = 0
        pos_list: list

        pos_list = cls.get_cfdpos_all_by_daterange(from_dt, to_dt, open_pos_typ, list_src)

        #   when open position List
        if Util.is_cfdpos_list_src_from_open_poslist(list_src):
            for _pos in pos_list:
                Pnl += _pos.posCurrentProfit()

        #   when history position List
        elif Util.is_cfdpos_list_src_from_history_list(list_src):
            for _pos in pos_list:
                Pnl += _pos.pos_deal_profit()

        rsl = Pnl

        return rsl

#  --- END CLASS CFD POSITION ---  #


class CFDTradeExecutor(object):  # Needed ???

    def __init__(self):
        pass

#  --- END CLASS CFD TRADE EXECUTOR ---  #


class MarketPosition(object):       # --TO OPTIMISE--

    def __init__(self):
        pass  # Not need init for total static class

# __
    @staticmethod
    def get_position_openprice(_ticket: str) -> float:
        """ get Position Open Price
        :param _ticket:
        :return: float
        """
        rsl: float = 0

        if Util.is_null_ticket(_ticket):
            return rsl

        trd_mod = Pair.get_trading_mode()
        
        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_openprice(_ticket=_ticket, trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def get_position_opentime(_ticket: str) -> dt.datetime:
        """ get Position Open Time
        :param _ticket:
        :return: datetime
        """
        rsl: dt.datetime = Duration.get_null_datetime()

        if Util.is_null_ticket(_ticket):
            return rsl

        trd_mod = Pair.get_trading_mode()
        
        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_opentime(_ticket=_ticket, trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def get_position_lot(_ticket: str) -> float:
        """ get Position _lot
        :param _ticket:
        :return: float
        """
        rsl: float = 0

        if Util.is_null_ticket(_ticket):
            return rsl

        trd_mod = Pair.get_trading_mode()
        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_lot(_ticket=_ticket, trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def get_position_typ(_ticket: str) -> Eaenum.PosType:
        """ get Position _Type
        :param _ticket:
        :return: PosTyp
        """
        rsl: Eaenum.PosType = Eaenum.PosType.OpNo

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        trd_mod = Pair.get_trading_mode()
        rsl = Eagbl.EA_Exchange.i_get_position_type(_ticket=_ticket, trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def get_position_tp_price(_ticket: str) -> float:
        """ get Position _Take Profit Price
        :param _ticket:
        :return: float
        """
        rsl: float = 0

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_tp_price(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def get_position_sl_price(_ticket: str) -> float:
        """ get Position _Stop Loss Price
        :param _ticket:
        :return: float
        """
        rsl: float = 0

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_sl_price(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def get_position_comment(_ticket: str) -> str:
        """ get Position _Comment
        :param _ticket:
        :return: str
        """
        rsl: str = ""

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_comment(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def get_position_deal_profit(_ticket: str) -> float:
        """ get Position _Deal Profit
        :param _ticket:
        :return: float
        """
        rsl: float = 0

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_dealprofit_future(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def is_position_filled_onmarket(_ticket: str) -> bool:
        """ is Position _Filled On Market ?
        :param _ticket:
        :return: bool
        """
        rsl: bool = False

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_is_position_filled_on_market(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def get_position_verylast_filled_onmarket_ticket() -> str:
        """ get Position _very Last Filled On Market _ticket
        :return: str
        """
        rsl: str  # = ""

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_very_last_filled_onmarket_ticket()

        return rsl

# __
    @staticmethod
    def get_position_verylast_filled_onmarket_infos() -> dict:
        """ get Position _very Last Filled On Market _Infos
        :return: {}
        """
        rsl: dict

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_very_last_filled_onmarket_infos()

        return rsl

# __
    @staticmethod
    def get_position_closed_price(_ticket: str) -> float:
        """ get Position _Closed Price
        :param _ticket:
        :return: float
        """
        rsl: float = 0

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_closedprice_future(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def get_position_closedtime(_ticket: str) -> dt.datetime:
        """ get Position _Closed Time
        :param _ticket:
        :return: datetime
        """
        rsl: dt.datetime = Duration.get_null_datetime()

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_closedtime_future(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def get_position_closed_profit(_ticket: str) -> float:
        """ get Position _Closed Profit
        :param _ticket:
        :return: float
        """
        rsl: float = 0

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_position_closed_profit_future(_ticket=_ticket)

        return rsl

# __
    @staticmethod
    def is_position_older_yet_opened_on_market() -> bool:   # VERIFY - not the good implementation
        """ is Position Older _yet Opened On Market ?
        :return: bool
        """
        rsl: bool = False

        pos_count = MarketPosition.get_position_all_count()

        if pos_count is not 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def get_position_number_of_buy() -> int:
        """ get Position _Number Of Buy
        :return: int
        """
        rsl: int = 0

        symbol = Pair.get_symbol()

        trd_mod = Pair.get_trading_mode()

        if Util.is_trade_mode_future(trd_mod):
            # Call to Interface #
            rsl = Eagbl.EA_Exchange.i_get_position_onmarket_numberof_buy_future(_symbol=symbol)

        elif Util.is_trade_mode_spot_or_margin(trd_mod):
            rsl = Eagbl.cfdManaja.get_cfdpos_all_by_position(pos_typ=Eaenum.PosType.OpBuy)

        return rsl

# __
    @staticmethod
    def get_position_number_of_sell() -> int:
        """ get Position _Number Of Sell
        :return: int
        """
        rsl: int = 0

        symbol = Pair.get_symbol()

        trd_mod = Pair.get_trading_mode()

        if Util.is_trade_mode_future(trd_mod):
            # __ Call to Interface #
            rsl = Eagbl.EA_Exchange.i_get_position_onmarket_numberof_sell_future(_symbol=symbol)

        elif Util.is_trade_mode_spot_or_margin(trd_mod):
            rsl = Eagbl.cfdManaja.get_cfdpos_all_by_position(pos_typ=Eaenum.PosType.OpSell)

        return rsl

# __
    @staticmethod
    def get_position_all_count() -> int:   # this function work for CFD Manager as well as Market Position
        """ get Position _All Count
        this function work for CFD Manager as well as Market Position
        :return: int
        """
        rsl: int = 0

        trd_mod = Pair.get_trading_mode()

        if Util.is_trade_mode_future(trd_mod):
            rsl = MarketPosition.get_position_number_of_buy() +\
                  MarketPosition.get_position_number_of_sell()

        elif Util.is_trade_mode_spot_or_margin(trd_mod):
            rsl = Eagbl.cfdManaja.get_cfdpos_number_opened()

        return rsl

# __
    @staticmethod
    def get_waiting_orders_all_count(trd_mod: Eaenum.TradeMode) -> int:
        """ get Waiting Orders _All Count
        :param trd_mod:
        :return: int
        """
        symbol = Pair.get_symbol()

        # Call to Interface #
        rsl = Eagbl.EA_Exchange.i_get_waiting_orders_onmarket_all_count(_symbol=symbol,
                                                                        trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def is_waiting_orders_onmarket(trd_mod: Eaenum.TradeMode) -> bool:
        """ is Waiting Orders _On Market ?
        :return: int
        """
        rsl: bool  # = False

        # symbol
        symbol = Pair.get_symbol()      # Useful ???

        # Call to Interface #
        rsp = Eagbl.EA_Exchange.i_is_waiting_orders_onmarket(_symbol=symbol, trd_mod=trd_mod)

        rsl = rsp

        return rsl

# __
    @staticmethod
    def close_position_or_order(_ticket: str) -> bool:
        """ close Position Or Orders
        :param _ticket:
        :return: bool
        """
        rsl: bool = False

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call To Interface #
        rsp = Eagbl.EA_Exchange.i_cancel_position_or_order_(_ticket)

        rsl = rsp

        return rsl

# __
    @staticmethod
    def is_position_in_profit(_ticket: str) -> bool:      # ?  VERIFY
        """ is Position _In Profit
        :param _ticket:
        :return: int
        """
        rsl = False

        if Util.is_null_ticket(_ticket):
            return rsl

        if MarketPosition.get_position_deal_profit(_ticket) > 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def close_at_profit(_ticket: str) -> bool:
        """ close At Profit
        :param _ticket:
        :return: bool
        """
        rsl: bool = False

        if Util.is_null_ticket(_ticket):
            return rsl

        # check if in profit mode
        is_in_profit = MarketPosition.is_position_in_profit(_ticket)

        if is_in_profit:
            rsl = MarketPosition.close_position_or_order(_ticket)

        return rsl

# __
    @staticmethod
    def place_position(pos_typ: Eaenum.PosType, trd_mod: Eaenum.TradeMode,
                       _price: float, _lot: float,
                       _sl: float = 0, _tp: float = 0,
                       is_isolated: bool = True) -> bool:
        """ place Position
        :return: bool
        """
        rsl: bool  # = False

        # Call To Interface
        rsp = Eagbl.EA_Exchange.i_place_position_(pos_typ, trd_mod, _price, _lot, _sl, _tp, is_isolated)

        rsl = rsp

        return rsl

# __
    @staticmethod
    def place_future_stoploss(_ticket: str, sl_price: float) -> bool:
        """ place Future Position _Stop Loss
        :param _ticket:
        :param sl_price:
        :return: bool
        """
        rsl: bool = False

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call To Interface #
        rsp = Eagbl.EA_Exchange.i_place_stoploss_future_(_ticket=_ticket, sl_price=sl_price)

        rsl = rsp

        return rsl

# __
    @staticmethod
    def place_future_takeprofit(_ticket: str, tp_price: float) -> bool:
        """ place Future Position _Take Profit
        :param _ticket:
        :param tp_price:
        :return: bool
        """
        rsl: bool = False

        if Util.is_null_ticket(_ticket):
            return rsl

        # Call To Interface #
        rsp = Eagbl.EA_Exchange.i_place_takeprofit_future_(_ticket=_ticket, tp_price=tp_price)

        rsl = rsp

        return rsl

#  --- END CLASS MARKET POSITION ---  #


class MarketBridge(object):

    def __init__(self):
        pass  # Not need init for total static class

# __
    @staticmethod
    def set_leverage(lever: int) -> None:
        """ set leverage
        :param lever:
        :return: None
        """
        # Call To Interface #
        is_ok = Eagbl.EA_Exchange.i_set_leverage(lever=lever)

        if is_ok:
            print("EA Leverage Changed Successfully!")
        else:
            print("EA Leverage Change Not Done!")

# __
    @staticmethod
    def i_get_candle_current_tick_price(_pair: str, trd_mod: Eaenum.TradeMode,
                                        trd_direction: Eaenum.TrdDirection) -> float:
        """ get Candle Current Tick Price
        :param _pair:
        :param trd_mod:
        :param trd_direction:
        :return:
        """
        return Eagbl.EA_Exchange.i_get_candle_current_tick_price(_pair, trd_mod, trd_direction)

# __
    @staticmethod
    def i_get_candle_info_by_datetime(_dt: dt.datetime, _timeframe: Eaenum.TimeFrames, _symbol: str) -> list:
        """ get Candle Infos _by Datetime
        :param _dt:
        :param _timeframe:
        :param _symbol:
        :return: list
        """
        return Eagbl.EA_Exchange.i_get_candle_info_by_datetime(_dt=_dt,
                                                               _timeframe=_timeframe,
                                                               _symbol=_symbol)

# __
    @staticmethod
    def i_get_candle_info_by_position(_pos: int, _timeframe: Eaenum.TimeFrames, _symbol: str) -> list:
        """ get Candle Info _By Position
        :param _pos:
        :param _timeframe:
        :param _symbol:
        :return: []
        """
        return Eagbl.EA_Exchange.i_get_candle_info_by_datetime(_pos=_pos,
                                                               _timeframe=_timeframe,
                                                               _symbol=_symbol)

# __
    @staticmethod
    def i_get_coin_balance_spot(_coin: str,
                                blc_typ: Eaenum.SpotBalanceTyp = Eaenum.SpotBalanceTyp.SFree) -> float:
        """ get coin Balance _spot
        :param _coin:
        :param blc_typ:
        :return:
        """
        return Eagbl.EA_Exchange.i_get_coin_balance_spot(_coin=_coin,
                                                         blc_typ=blc_typ)

# __
    @staticmethod
    def i_get_coin_balance_margin(_coin: str,
                                  blc_typ: Eaenum.MarginBalanceTyp = Eaenum.MarginBalanceTyp.MFree) -> float:
        """ get coin Balance _margin
        :param _coin:
        :param blc_typ:
        :return: float

        Get desire balance typ: borrowed | free | interest | locked | netAsset
        """
        return Eagbl.EA_Exchange.i_get_coin_balance_margin(_coin=_coin, blc_typ=blc_typ)

# __
    @staticmethod
    def i_get_coin_balance_future(_coin: str,
                                  f_blc_typ: Eaenum.FutureBalanceTyp = Eaenum.FutureBalanceTyp.FWalletBalance
                                  ) -> float:
        """ get coin Balance _future
        :param _coin:
        :param f_blc_typ:
        :return: float
        """
        return Eagbl.EA_Exchange.i_get_coin_balance_future(_coin=_coin, f_blc_typ=f_blc_typ)

# __
    @staticmethod
    def get_coin_balance(_coin: str,
                         blc_typ: Eaenum.SpotBalanceTyp | Eaenum.MarginBalanceTyp | Eaenum.FutureBalanceTyp = None,
                         trd_mod: Eaenum.TradeMode = None) -> float:
        """ get Coin Balance
        :param _coin:
        :param blc_typ:
        :param trd_mod:
        :return: float
        """
        rsl: float = 0

        if Util.is_null_string(trd_mod.value):
            trd_mod = Pair.get_trading_mode()

        # call to exchange interface #
        if Util.is_trade_mode_spot(trd_mod):
            if Util.is_none_(blc_typ):
                blc_typ = Eaenum.SpotBalanceTyp.SFree             # setting default for spot

            rsl = MarketBridge.i_get_coin_balance_spot(_coin=_coin, blc_typ=blc_typ)

        elif Util.is_trade_mode_margin(trd_mod):
            if Util.is_none_(blc_typ):
                blc_typ = Eaenum.MarginBalanceTyp.MFree           # setting default for margin

            rsl = MarketBridge.i_get_coin_balance_margin(_coin=_coin, blc_typ=blc_typ)

        elif Util.is_trade_mode_future(trd_mod):
            if Util.is_none_(blc_typ):
                blc_typ = Eaenum.FutureBalanceTyp.FWalletBalance  # setting default for future

            rsl = MarketBridge.i_get_coin_balance_future(_coin=_coin, f_blc_typ=blc_typ)

        return rsl

# __
    @staticmethod
    def i_swap_coin_(coin_src: str, coin_dst: str, _amount: float) -> bool:
        """ swap coin
        :param coin_src:
        :param coin_dst:
        :param _amount:
        :return: bool
        """
        return Eagbl.EA_Exchange.i_swap_coin_(coin_src=coin_src, coin_dst=coin_dst, _amount=_amount)

# __
    @staticmethod
    def i_replenish_coin__(_coin: str, _amount: float) -> bool:
        """ replenish coin
        :param _coin:
        :param _amount:
        :return: bool
        """
        return Eagbl.EA_Exchange.i_replenish_coin__(_coin=_coin, _amount=_amount)

# __
    @staticmethod
    def i_withdraw_coin__(_coin: str, _amount: float, _wallet_adr: str) -> bool:
        """ withdraw coin
        :param _coin:
        :param _amount:
        :param _wallet_adr:
        :return: bool
        """
        return Eagbl.EA_Exchange.i_withdraw_coin__(_coin=_coin, _amount=_amount, _wallet_adr=_wallet_adr)

# __
    @staticmethod
    def i_get_min_max_step_volume_spotmargin(_pair: str, trd_mod: Eaenum.TradeMode) -> list:
        """ get min max step _Volume (Lot) spot-margin
        :param _pair:
        :param trd_mod:
        :return: [min,max,step]
        """
        return Eagbl.EA_Exchange.i_get_min_max_step_volume_spotmargin(_pair=_pair, trd_mod=trd_mod)

# __
    @staticmethod
    def i_get_min_max_step_volume_future(_pair: str) -> list:
        """ get min max step _Volume future
        :param _pair:
        :return: [min,max,step]
        """
        return Eagbl.EA_Exchange.i_get_min_max_step_volume_future(_pair=_pair)


#  --- END CLASS MARKET BRIDGE ---  #


class From(object):

    def __init__(self):
        pass  # Not need init for total static class

    @staticmethod
    def from_prices_to_dist_between(_price1: float, _price2: float) -> int:
        """ From Prices To _Dist Between
        :return: int
        """
        rsl: int

        rsl = int(abs(_price1 - _price2))

        return rsl

# __
    @staticmethod
    def from_index_to_ticket(_index: int) -> str:       # --TO CODE--
        """ From Index To _ticket
        :param _index:
        :return: str
        """
        rsl: str = ""

        if Util.is_trade_mode_future(Eainp.EA_Trade_Mode):
            pass

        elif Util.is_trade_mode_spot_or_margin(Eainp.EA_Trade_Mode):
            cfdPos = Eagbl.cfdManaja.getCFDPosInsideList_byIndex(_index, Eaenum.CFDPosListSrc.OpenPosList)
            rsl = cfdPos.get_pos_ticket_opening()       # recover ticket

        return rsl

# __
    @staticmethod
    def from_open_ordertyp_to_coinsidetyp(open_pos_typ: Eaenum.PosType) -> Eaenum.CoinSideTyp:
        """ From Index To _ticket
        :param open_pos_typ:
        :return: CoinSideTyp
        """
        rsl: Eaenum.CoinSideTyp = Eaenum.CoinSideTyp.coinSideNo

        if Util.is_position_type_buy(open_pos_typ):        # when btn BUY origin is Right
            rsl = Eaenum.CoinSideTyp.coinRight
        elif Util.is_position_type_sell(open_pos_typ):     # when btn SELL origin is Left
            rsl = Eaenum.CoinSideTyp.coinLeft

        return rsl

# __
    @staticmethod
    def from_open_btntyp_to_profitable_direction(open_pos_typ: Eaenum.PosType) -> Eaenum.TrdDirection:
        """ From OpenBtnTyp To _Profitable Direction
        :param open_pos_typ:
        :return: TrdDirection
        """
        rsl: Eaenum.TrdDirection = Eaenum.TrdDirection.Unknown

        if Util.is_position_type_buy(open_pos_typ):
            rsl = Eaenum.TrdDirection.Upper
        elif Util.is_position_type_sell(open_pos_typ):
            rsl = Eaenum.TrdDirection.Downer

        return rsl

# __
    @staticmethod
    def from_coinsidetyp_to_btn_open_ordertyp(open_coinside_typ: Eaenum.CoinSideTyp) -> Eaenum.PosType:
        """ From CoinSideTyp To _BtnOpenOrderTyp
        :param open_coinside_typ:
        :return: PosTyp
        """
        rsl: Eaenum.PosType = Eaenum.PosType.OpNo

        if open_coinside_typ == Eaenum.CoinSideTyp.coinRight:
            rsl = Eaenum.PosType.OpBuy
        elif open_coinside_typ == Eaenum.CoinSideTyp.coinLeft:
            rsl = Eaenum.PosType.OpSell

        return rsl

# __
    @staticmethod
    def from_coinsidetyp_to_coin(open_coinside_typ: Eaenum.CoinSideTyp) -> str:
        """From CoinSideTyp To _Coin
        :param open_coinside_typ:
        :return: str
        """
        rsl: str = ''

        # recover the pair
        pair = Pair(_pair=Eainp.EA_Trade_Pair)

        if open_coinside_typ == Eaenum.CoinSideTyp.coinRight:
            rsl = pair.get_coin_right().upper()
        elif open_coinside_typ == Eaenum.CoinSideTyp.coinLeft:
            rsl = pair.get_coin_left().upper()

        return rsl

# __
    @staticmethod
    def from_bool_to_string(bool_state: bool, want_upper_case=False) -> str:
        """ From Boolean To _String
        :param bool_state:
        :param want_upper_case:
        :return: str
        """
        rsl: str = ''

        if Util.is_true(bool_state):
            rsl = 'True'
        elif Util.is_false(bool_state):
            rsl = 'False'

        if Util.is_true(want_upper_case):
            rsl = rsl.upper()

        return rsl

# __
    @staticmethod
    def from_coinbuy_to_coin_amount_invested(open_price: float, _lot: float,
                                             coin_origin_side: Eaenum.CoinSideTyp) -> float:
        """ From Coin Bought To _Coin Amount Invested
        :param open_price:
        :param _lot:
        :param coin_origin_side:
        :return: float
        """
        rsl: float = 0
        amount_invested: float = 0

        if open_price == 0:
            return rsl

        if Util.is_coinside_right(coin_origin_side):
            amount_invested = _lot * open_price
        elif Util.is_coinside_left(coin_origin_side):
            amount_invested = _lot / open_price

        rsl = amount_invested

        return rsl

# __
    @staticmethod
    def from_coinbuy_to_coin_amount_comeback(open_price: float,  open_pos_lot: float,
                                             coin_origin_side: Eaenum.CoinSideTyp) -> float:
        """ __same as former__  (FromCoinBuyTo_coinAmountInvested)
        From Coin Bought To Coin Amount Comeback
        :param open_price:
        :param open_pos_lot:
        :param coin_origin_side:
        :return: float
        """
        rsl: float

        # amount comeback is what invested
        rsl = From.from_coinbuy_to_coin_amount_invested(open_price, open_pos_lot, coin_origin_side)

        return rsl

# __
    @staticmethod
    def from_coinbuy_to_coin_amount_comeback_with_profitloss(close_price: float, open_pos_lot: float,
                                                             coin_origin_side: Eaenum.CoinSideTyp) -> float:
        """ __same as former__  (FromCoinBuyTo_coinAmountInvested)
            From Coin Bought To Coin Amount Comeback
        :param close_price:
        :param open_pos_lot:
        :param coin_origin_side:
        :return: float
        """
        rsl: float
        amount_comeback: float

        # amount comeback is what invested
        amount_comeback = From.from_coinbuy_to_coin_amount_invested(close_price, open_pos_lot, coin_origin_side)

        rsl = amount_comeback

        return rsl

# __
    @staticmethod
    def from_tradedirection_to_btn_postyp(trd_direction: Eaenum.TrdDirection) -> Eaenum.PosType:
        """ From Trade Direction To BtnPosTyp
        :param trd_direction:
        :return: PosTyp
        """
        rsl: Eaenum.PosType = Eaenum.PosType.OpNo

        if Util.is_trade_direction_upper(trd_direction):
            rsl = Eaenum.PosType.OpBuy

        elif Util.is_trade_direction_downer(trd_direction):
            rsl = Eaenum.PosType.OpSell

        return rsl

# __
    @staticmethod
    def from_open_btn_postyp_to_tradedirection(open_pos_typ: Eaenum.PosType) -> Eaenum.TrdDirection:
        """ From Open Btn Pos Typ To_ Trade Direction
        :param open_pos_typ:
        :return: Trade Direction
        """
        rsl: Eaenum.TrdDirection = Eaenum.TrdDirection.Unknown

        if Util.is_position_type_buy(open_pos_typ):
            rsl = Eaenum.TrdDirection.Upper

        elif Util.is_position_type_sell(open_pos_typ):
            rsl = Eaenum.TrdDirection.Downer

        return rsl

# __
    @staticmethod
    def from_price_to_pips(_price: float) -> int:
        """ From Price To _Pips
        :param _price:
        :return: int
        """
        rsl: int

        rsl = int(_price / Pair.point())

        return rsl

# __
    @staticmethod
    def from_pips_to_price(_pips: int) -> float:
        """ From Pips To _price
        :return: float
        """
        rsl: float

        rsl = Util.normalize_price(_pips * Pair.point())

        return rsl

# __
    @staticmethod
    def from_priceinterval_to_pips(_price1: float, _price2: float) -> int:
        """ From Price Interval To _Pips
        :param _price1:
        :param _price2:
        :return: int
        """
        rsl: int

        rsl = From.from_price_to_pips(
            abs(Util.normalize_price_(_price1, Pair.digit()) - Util.normalize_price_(_price2, Pair.digit()))
        )

        return rsl

# __
    @staticmethod
    def from_priceinterval_to_distance_pips(_price1: float, _price2: float) -> int:
        """ From Price Interval To _Distance Pips
        Always return positive Pips
        :param _price1:
        :param _price2:
        :return: int
        """
        rsl: int

        rsl = abs(From.from_priceinterval_to_pips(_price1, _price2))    # Distance may be positive

        return rsl

# __
    @staticmethod
    def from_price_and_pips_to_new_positive_pricetarget_tradedirection_based(_price: float, extra_pips: int,
                                                                             trd_direction: Eaenum.TrdDirection
                                                                             ) -> float:
        """ From Price And Pips To _New Positive Price Target _Trade Direction Based
        :param _price:
        :param extra_pips:
        :param trd_direction:
        :return: float
        """
        rsl: float = 0

        if extra_pips == 0:
            return rsl

        if Util.is_trade_direction_upper(trd_direction):
            rsl = Util.normalize_price_(_price + From.from_pips_to_price(extra_pips), Pair.digit())

        elif Util.is_trade_direction_downer(trd_direction):
            rsl = Util.normalize_price_(_price - From.from_pips_to_price(extra_pips), Pair.digit())

        return rsl

# __
    @staticmethod
    def from_price_and_pips_to_new_positive_pricetarget(open_price: float, extra_pips: int,
                                                        open_pos_typ: Eaenum.PosType) -> float:
        """ From Price And Pips To _New Positive Price Target _PosTyp Based
        :return: float
        """
        rsl: float  # = 0

        if extra_pips == 0:
            rsl = open_price
            return rsl

        trd_direction = From.from_open_btn_postyp_to_tradedirection(open_pos_typ)
        rsl = From.from_price_and_pips_to_new_positive_pricetarget_tradedirection_based(open_price,
                                                                                        extra_pips,
                                                                                        trd_direction)

        return rsl

# __
    @staticmethod
    def from_price_and_pips_to_new_negative_pricetarget_tradedirection_based(_price: float, extra_pips: int,
                                                                             trd_direction: Eaenum.TrdDirection
                                                                             ) -> float:
        """ From Price And Pips To _New Negative Price Target _Trade Direction Based
        :return: float
        """
        rsl: float = 0

        if extra_pips == 0:
            rsl = _price
            return rsl

        if Util.is_trade_direction_upper(trd_direction):
            rsl = Util.normalize_price_(_price - From.from_pips_to_price(extra_pips), Pair.digit())

        elif Util.is_trade_direction_downer(trd_direction):
            rsl = Util.normalize_price_(_price + From.from_pips_to_price(extra_pips), Pair.digit())

        return rsl

# __
    @staticmethod
    def from_price_and_pips_to_new_negative_pricetarget(open_price: float, extra_pips: int,
                                                        open_pos_typ: Eaenum.PosType) -> float:
        """ From Price And Pips To _New Negative Price Target _PosTyp Based
        :return: float
        """
        rsl: float

        if extra_pips == 0:
            rsl = open_price
            return rsl

        trd_direction = From.from_open_btn_postyp_to_tradedirection(open_pos_typ)
        rsl = From.from_price_and_pips_to_new_negative_pricetarget_tradedirection_based(open_price,
                                                                                        extra_pips,
                                                                                        trd_direction)

        return rsl

# __
    @staticmethod
    def from_entryprice_and_pips_to_sl_pricetarget_tradedirection_based(entry_price: float, sl_pips: int,
                                                                        trd_direction: Eaenum.TrdDirection) -> float:
        """ From Entry Price And Pips To _SL Price Target _Trade Direction Based
        :return: float
        """
        rsl = From.from_price_and_pips_to_new_negative_pricetarget_tradedirection_based(entry_price,
                                                                                        sl_pips,
                                                                                        trd_direction)

        return rsl

# __
    @staticmethod
    def from_entryprice_and_pips_to_tp_pricetarget_tradedirection_based(entry_price: float, tp_pips: int,
                                                                        trd_direction: Eaenum.TrdDirection) -> float:
        """ From Entry Price And Pips To _TP Price Target _Trade Direction Based
        :return: float
        """
        rsl = From.from_price_and_pips_to_new_positive_pricetarget_tradedirection_based(entry_price,
                                                                                        tp_pips,
                                                                                        trd_direction)

        return rsl

# __
    @staticmethod
    def from_entryprice_and_pips_to_sl_pricetarget(entry_price: float, sl_pips: int,
                                                   pos_typ: Eaenum.PosType) -> float:
        """ From Entry Price And Pips To _SL Price Target _PosTyp Based
        :return: float
        """
        rsl = From.from_price_and_pips_to_new_negative_pricetarget(entry_price, sl_pips, pos_typ)

        return rsl

# __
    @staticmethod
    def from_entryprice_and_pips_to_tp_pricetarget(entry_price: float, tp_pips: int,
                                                   pos_typ: Eaenum.PosType) -> float:
        """ From Entry Price And Pips To _TP Price Target _PosTyp Based
        :return: float
        """
        rsl = From.from_price_and_pips_to_new_positive_pricetarget(entry_price, tp_pips, pos_typ)

        return rsl

# __
    @staticmethod
    def from_index_to_rank(_index: int) -> int:
        """ From Index to _Rank
        :param _index:
        :return: int
        """
        rsl = _index + 1

        return rsl

# __
    @staticmethod
    def from_rank_to_index(_rank: int) -> int:
        """ From Rank to _Index
        :param _rank:
        :return: int
        """
        rsl = _rank - 1

        return rsl

# __
    @staticmethod
    def from_float_to_float_as_integer(_nb: float) -> float:
        """ From float To _float as Integer
        :return: float
        """
        rsl = Util.normalize_float(_nb, 0)

        return rsl

# __
    @staticmethod
    def from_integer_to_number_of_digit(_nb: int) -> float:
        """ From Integer To _Number Of Digit
        :return: float
        """
        rsl: float

        strg = str(_nb)

        rsl = len(strg)

        return rsl

# __
    @staticmethod
    def from_float_to_number_of_digit_after(_nb: float) -> int:
        """ From float To _Number Of Digit After
        :return: int
        """
        rsl: int  # = 0

        # converting Number To string
        strg: str = str(_nb)

        # let's split the string
        strgList = strg.split(".")                          # let's get a dictionnary of two string
        strg = strgList[1]                                  # just recover the second

        # One must recover Length of string After the dot
        count = len(strg)                                  # length of the new str

        # the number of digit after
        rsl = count

        return rsl

# __
    @staticmethod
    def from_float_to_specific_digit_after(_nb: float, _digit: int) -> float:
        """ From Float to _specific Digit After
        :return: float
        """
        rsl: float  # = 0

        # converting Number To string
        strg: str = str(_nb)

        # let's split the string
        strgList = strg.split(".")           # let's get a dictionnary of two string

        # just recover the second
        str_before: str = strgList[0]
        str_after: str = strgList[1]

        # One must recover specific number after dot
        # let's recover from the first to the x
        _choosedAfterDot = str_after[0:_digit]                    # m:n  (m included, n excluded)

        # the number as String
        the_nb = str_before+"."+_choosedAfterDot

        rsl = float(the_nb)

        return rsl

# __
    @staticmethod
    def from_float_to_point(_nb: float) -> float:
        """ From Float to_Point
        :return: float
        """
        rsl: float  # = 0

        Pair.point()
        digit_after_dot = From.from_float_to_number_of_digit_after(_nb)

        _digit0 = "0"
        _digit1 = "1"

        strg = "0."

        for i in range(digit_after_dot-1):
            strg += _digit0

        strg += _digit1

        rsl = float(strg)

        return rsl

# __
    @staticmethod
    def from_volume_and_purpose_pips_to_profit(_lot: float, purpose_pips: int) -> float:
        """ From Volume And Purpose-Pips To Profit
        :param _lot:
        :param purpose_pips:
        :return: float
        """
        rsl = float(_lot*purpose_pips)                 # let's use the formula purpose = Lot * Pips

        return rsl

# __
    @staticmethod
    def from_entry_exitprice_and_volume_to_expected_profitloss(_entry: float, exit_price_tpsl: float,
                                                               _lot: float) -> float:
        """ From Entry-Exit Price And Volume To Expected Profit
        :param _entry:
        :param exit_price_tpsl:
        :param _lot:
        :return:
        """
        rsl = From.from_volume_and_purpose_pips_to_profit(_lot,
                                                          From.from_priceinterval_to_pips(_entry, exit_price_tpsl))

        return rsl

# __
    @staticmethod
    def from_purpose_and_volume_to_pips(purpose_amount: float, _volume: float) -> int:
        """ From Purpose And Volume To Pips
        :param purpose_amount:
        :param _volume:
        :return: int
        """
        rsl = int(purpose_amount / _volume)                  # let's use the formula purpose = Lot * Pips

        return rsl

# __
    @staticmethod
    def from_lot_to_tick_lot(_volume: float) -> float:
        """ From Lot To _Tick Lot
        :param _volume:
        :return: float
        """
        rsl = Util.normalize_lot(_volume*Pair.point())         # considering _volume * Point()

        return rsl

# __
    @staticmethod
    def from_std_side_to_postyp(std_side: str) -> Eaenum.PosType:
        """ From Standart Side To _Position Typ
        :param std_side:
        :return: PosTyp
        """
        rsl: Eaenum.PosType = Eaenum.PosType.OpNo

        if std_side == bc.BaseClient.SIDE_BUY:
            rsl = Eaenum.PosType.OpBuy
        elif std_side == bc.BaseClient.SIDE_SELL:
            rsl = Eaenum.PosType.OpSell

        return rsl

# __
    @staticmethod
    def from_postyp_to_std_side(pos_typ: Eaenum.PosType) -> str:
        """ From Position-Type To _Standart Side
        :param pos_typ:
        :return: str
        """
        rsl: str = "No"

        if Util.is_position_type_buy(pos_typ):
            rsl = bc.BaseClient.SIDE_BUY
        elif Util.is_position_type_sell(pos_typ):
            rsl = bc.BaseClient.SIDE_SELL

        return rsl

# __
    @staticmethod
    def from_ordtyp_to_std_ord(ordtyp: Eaenum.OrdType) -> str:
        """ From Order-Type To _Standart Order
        :return str
        """
        rsl: str = ""

        if ordtyp == Eaenum.OrdType.OpTypLimit:
            rsl = bc.BaseClient.ORDER_TYPE_LIMIT
        elif ordtyp == Eaenum.OrdType.OpTypMarket:
            rsl = bc.BaseClient.ORDER_TYPE_MARKET
        elif ordtyp == Eaenum.OrdType.OpTypStopLoss:
            rsl = bc.BaseClient.ORDER_TYPE_STOP_LOSS
        elif ordtyp == Eaenum.OrdType.OpTypStopLossLimit:
            rsl = bc.BaseClient.ORDER_TYPE_STOP_LOSS_LIMIT
        elif ordtyp == Eaenum.OrdType.OpTypTakeProfit:
            rsl = bc.BaseClient.ORDER_TYPE_TAKE_PROFIT
        elif ordtyp == Eaenum.OrdType.OpTypTakeProfitLimit:
            rsl = bc.BaseClient.ORDER_TYPE_TAKE_PROFIT_LIMIT
        elif ordtyp == Eaenum.OrdType.OpTypLimitMaker:
            rsl = bc.BaseClient.ORDER_TYPE_LIMIT_MAKER

        return rsl

# __
    @staticmethod
    def from_std_ord_to_ordtyp(std_ordtyp: str) -> Eaenum.OrdType:
        """ From Standart Order To _Order Type
        :return OrdType
        """
        rsl: Eaenum.OrdType = Eaenum.OrdType.OpNo

        if std_ordtyp == bc.BaseClient.ORDER_TYPE_LIMIT:
            rsl = Eaenum.OrdType.OpTypLimit
        elif std_ordtyp == bc.BaseClient.ORDER_TYPE_MARKET:
            rsl = Eaenum.OrdType.OpTypMarket
        elif std_ordtyp == bc.BaseClient.ORDER_TYPE_STOP_LOSS:
            rsl = Eaenum.OrdType.OpTypStopLoss
        elif std_ordtyp == bc.BaseClient.ORDER_TYPE_STOP_LOSS_LIMIT:
            rsl = Eaenum.OrdType.OpTypStopLossLimit
        elif std_ordtyp == bc.BaseClient.ORDER_TYPE_TAKE_PROFIT:
            rsl = Eaenum.OrdType.OpTypTakeProfit
        elif std_ordtyp == bc.BaseClient.ORDER_TYPE_TAKE_PROFIT_LIMIT:
            rsl = Eaenum.OrdType.OpTypTakeProfitLimit
        elif std_ordtyp == bc.BaseClient.ORDER_TYPE_LIMIT_MAKER:
            rsl = Eaenum.OrdType.OpTypLimitMaker

        return rsl

# __
    @staticmethod
    def from_positions_to_cfdposition(ticket_o: str, ticket_c: str = None) -> CFDPosition:
        """ From Positions To _CFDPosition
        :param ticket_o:
        :param ticket_c:
        :return: CFDPosition
        """
        cfdPos: CFDPosition

        o_pos = Position(_ticket=ticket_o)

        if ticket_c is None:    # when closing ticket not set
            cfdPos = From.from_positions_to_cfdposition_(pos_o=o_pos)

        else:                   # when closing ticket set
            c_pos = Position(_ticket=ticket_c)
            cfdPos = From.from_positions_to_cfdposition_(pos_o=o_pos, pos_c=c_pos)

        rsl = cfdPos

        return rsl

# __
    @staticmethod
    def from_positions_to_cfdposition_(pos_o: Position, pos_c: Position = None) -> CFDPosition:
        """ From Positions To CFDPosition
        :param pos_o:
        :param pos_c:
        :return: CFDPosition
        """
        rsl: CFDPosition  # = CFDPosition.get_null_cfdposition()

        open_ticket = pos_o.get_position_ticket()
        _openTyp = pos_o.get_position_typ()
        _openLot = pos_o.get_position_lot()
        _openTime = pos_o.get_position_open_time()
        open_price = pos_o.get_position_open_price()
        _SlPrice = pos_o.get_position_sl_price()
        _TpPrice = pos_o.get_position_tp_price()
        _partialComment = pos_o.get_position_comment()

        cfdPos = CFDPosition(btn_ordtyp=_openTyp, _ticket=open_ticket, _lot=_openLot, open_price=open_price,
                             open_dt=_openTime, sl_price=_SlPrice, tp_price=_TpPrice, _comment=_partialComment)

        if pos_c is not None:
            cfdPos.set_pos_ticket_closing(pos_c.get_position_ticket())
            cfdPos.set_pos_close_datetime(pos_c.get_position_open_time())
            cfdPos.set_pos_closeprice(pos_c.get_position_open_price())

            _cfdPosDealProfit = cfdPos.pos_deal_profit()         # ?
            cfdPos.set_pos_closed_profitloss(_cfdPosDealProfit)   # ?

        rsl = cfdPos

        return rsl

# __
    @staticmethod
    def from_dict_and_key_to_value_as_float(_dc: dict, _key: str) -> float:
        """ From Dict And Key To _Value as Float
        :param _dc:
        :param _key:
        :return: float
        """
        rsl: float

        _val = _dc[_key]

        rsl = float(_val)

        return rsl

#  --- END CLASS FROM ---  #


class Pair(object):

    m_pair: str
    m_coinLeft: str
    m_coinRight: str
    m_coinPivot: str

    def __init__(self, _pair: str = ""):
        # save pair in class var #

        if _pair == "":
            self.m_pair = Eainp.EA_Trade_Pair
        else:
            self.m_pair = _pair

        # split pair in couple of coin #
        coins = self.get_coins_inside_pair(_pair)
        self.m_coinLeft = coins[0]
        self.m_coinRight = coins[1]

    # getters
    def get_coin_left(self):
        return self.m_coinLeft

    def get_coin_right(self):
        return self.m_coinRight

    @property
    def get_coin_pivot(self):
        return self.m_coinPivot

    def get_pair(self):
        return self.m_pair
    #

    # setters
    def set_coin_left(self, _coin):
        self.m_coinLeft = _coin

    def set_coin_right(self, _coin):
        self.m_coinRight = _coin

    def set_coin_pivot(self, _coin):
        self.m_coinPivot = _coin
    #

    # methods
    def is_coin_left(self, _coin) -> bool:
        """ is Coin Left ?
        :param _coin:
        :return: bool
        """
        rsl: bool = False

        if _coin == self.get_coin_left():
            rsl = True

        return rsl

# __
    def is_coin_right(self, _coin) -> bool:
        """ is Coin Right ?
        :param _coin:
        :return: bool
        """
        rsl: bool = False

        if _coin == self.get_coin_right():
            rsl = True

        return rsl

# __
    def get_opposite_coin(self, pivot_coin: str) -> str:
        """ get Opposite Coin
        :param pivot_coin:
        :return: str
        """
        rsl: str = ""

        if pivot_coin == self.m_coinLeft:
            rsl = self.m_coinRight
        elif pivot_coin == self.m_coinRight:
            rsl = self.m_coinLeft

        return rsl

# __
    @staticmethod
    def get_symbol_lot_digit() -> int:    # --TO VERIFY--
        """ get Symbol Lot _Digit
        :return: int
        """
        rsl: int

        # pairCoin = From.FromCoinSideTypTo_coin(CoinsideTyp)
        pair = Pair.get_symbol()
        trdMode = Pair.get_trading_mode()

        # recover mini Lot
        _minLot = Pair.get_min_lot(_pair=pair, trd_mod=trdMode)   # each lot ?

        rsl = From.from_float_to_number_of_digit_after(_minLot)

        return rsl

# __
    def get_major_balance_coin(self) -> str:
        """ get Greater Balance Coin
        :return: str
        """
        rsl: str = ""

        coin_left_balance = MarketBridge.get_coin_balance(_coin=self.m_coinLeft, blc_typ=None)
        coin_right_balance = MarketBridge.get_coin_balance(_coin=self.m_coinRight, blc_typ=None)

        if coin_left_balance > coin_right_balance:
            rsl = self.m_coinLeft
        elif coin_left_balance < coin_right_balance:
            rsl = self.m_coinRight

        return rsl

# __
    def get_minor_balance_coin(self) -> str:
        """ get Minor Balance Coin
        :return: str
        """
        rsl: str = ""

        coin_left_balance = MarketBridge.get_coin_balance(_coin=self.m_coinLeft, blc_typ=None)
        coin_right_balance = MarketBridge.get_coin_balance(_coin=self.m_coinRight, blc_typ=None)

        if coin_left_balance < coin_right_balance:
            rsl = self.m_coinLeft
        elif coin_left_balance > coin_right_balance:
            rsl = self.m_coinRight

        return rsl

# __
    @staticmethod
    def is_minor_balance_need_to_be_replenished() -> bool:        # --TO CODE--
        """ is Minor Balance Needs to Be Relenished ?
        :return: bool
        """
        rsl = False
        # get Minor balance coin
        minor_blc_coin = Eagbl.EAPair.get_minor_balance_coin()
        minor_blc = MarketBridge.get_coin_balance(_coin=minor_blc_coin,     # getting the coin balance (default ?)
                                                  blc_typ=None)

        major_blc_coin = Eagbl.EAPair.get_major_balance_coin()
        major_blc = MarketBridge.get_coin_balance(_coin=major_blc_coin,
                                                  blc_typ=None)             # getting the coin balance (default ? )

        if minor_blc <= major_blc * Eainp.EA_Minor_Coin_Balance_inAlert_PCR:
            rsl = True

        return rsl

# __
    def is_coin_balance_equal(self) -> bool:
        """ is Coin Balance Equal ?
        :return: bool
        """
        rsl = False

        coin_left_balance = MarketBridge.get_coin_balance(_coin=self.m_coinLeft, blc_typ=None)
        coin_right_balance = MarketBridge.get_coin_balance(_coin=self.m_coinRight, blc_typ=None)

        if coin_left_balance == coin_right_balance:
            rsl = True

        return rsl

# __
    @classmethod
    def replenish_coin(cls, _coin: str, _amount: float) -> bool:
        """ replenish Coin
        :param _coin
        :param _amount
        :return: bool
        """
        rsl: bool

        # call to exchange interface #
        rsl = MarketBridge.i_replenish_coin__(_coin, _amount)

        return rsl

# __
    def replenish_opposite_coin(self, pivot_coin: str, _amount: float) -> bool:
        """ replenish Opposite Coin
        :param pivot_coin
        :param _amount
        :return: bool
        """
        rsl: bool

        # Get Opposite Coin
        _coin = self.get_opposite_coin(pivot_coin)

        # call to exchange interface #
        rsl = MarketBridge.i_replenish_coin__(_coin, _amount)

        return rsl

# __
    @staticmethod
    def get_coins_inside_pair(_pair: str) -> list:
        """ get Coin Inside Pair
        :param _pair:
        :return: list of 2 element
        """
        rsl: []

        # Spliting pairs by slash
        rsl = _pair.split('/', 2)

        return rsl

# __
    @staticmethod
    def coin_first_trader() -> None:   # --TO CODE--
        """
        Seek Opportunity for Left coin
        :return: None
        """
        EA.reactive_trader(pos_typ=Eaenum.PosType.OpSell)  # Let's goto Left trade

# __
    @staticmethod
    def coin_second_trader() -> None:  # --TO CODE--
        """
        Seek Opportunity for Right coin
        :return:
        """
        EA.reactive_trader(pos_typ=Eaenum.PosType.OpBuy)   # Let's goto Right trade

# __
    @staticmethod
    def get_symbol() -> str:
        """ know current Trading Symbol
        :return:
        """
        return Eainp.EA_Trade_Pair

# __
    @staticmethod
    def set_symbol(_symb: str) -> None:
        """ set current Trading Symbol
        :param _symb
        :return:
        """
        Eainp.EA_Trade_Pair = _symb

# __
    @staticmethod
    def is_willing_to_change_leverage() -> bool:
        """ is willing to change leverage ?
        :return: bool
        """
        return Eainp.EA_Want_Change_leverage

# __
    @staticmethod
    def get_trading_mode() -> Eaenum.TradeMode:
        """ get Trading Mode
        :return: TradeMode
        """
        return Eainp.EA_Trade_Mode

# __
    @staticmethod
    def get_trading_mode_val_lower() -> str:
        """ get Trading Mode val Lower
        :return: TradeMode
        """
        return Eainp.EA_Trade_Mode.value.lower()

# __
    @staticmethod
    def set_trading_mode(trd_mod: Eaenum.TradeMode) -> None:
        """ get Trading Mode
        :param trd_mod
        :return: TradeMode
        """
        Eainp.EA_Trade_Mode = trd_mod

# __
    @staticmethod
    def is_withdraw_coin_time(_coin: str, _amount: float) -> bool:     # --TO CODE--
        """ is Withdraw Coin Time ?
        :param _coin
        :param _amount
        :return bool
        """
        rsl: bool = False

        if Duration.get_current_time().hour == Eainp.EA_Withdrawal_Time:
            rsl = True

        return rsl

# __
    @staticmethod
    def withdraw_coin(_coin: str, _amount: float, wallet_adr: str) -> bool:
        """ withdraw Coin
        :param _coin
        :param _amount
        :param wallet_adr
        :return: bool
        """
        rsl: bool  # = False

        # get Trade Mode
        # trd_mod = Eainp.EA_Trade_Mode

        # get Trade Pair
        _pair = Eainp.EA_Trade_Pair

        # call to exchange interface #
        rsp = MarketBridge.i_withdraw_coin__(_coin, _amount, wallet_adr)

        rsl = rsp

        return rsl

# __
    @staticmethod
    def add_wallet_adr(_adr: str, _coin: str):
        """ add Wallet Adr
        :param _adr
        :param _coin
        :return: None
        """
        Eainp.EA_Wallets.append(_adr)

# __
    @staticmethod
    def secure_coin_by_swap_coin(coin_src: str, coin_dst: str, _amount: float) -> bool:     # --TO CODE--
        """ Secure Coin By _swap Coin
        :param coin_src
        :param coin_dst
        :param _amount

        :return: bool
        """
        rsl: bool  # = False

        # call to exchange interface #
        rsp = MarketBridge.i_swap_coin_(coin_src, coin_dst, _amount)

        rsl = rsp

        return rsl

# __
    @staticmethod
    def point() -> float:
        """ Point
        :return: float
        """
        rsl: float

        _price = Candle.get_cdl_current_tickprice()
        rsl = From.from_float_to_point(_price)

        return rsl

# __
    @staticmethod
    def _point() -> float:
        """ Point
        :return: float
        """
        return Pair.point()

# __
    @staticmethod
    def digit() -> int:
        """ Digit
        :return: int
        """
        rsl: int

        _price = Candle.get_cdl_current_tickprice()

        rsl = From.from_float_to_number_of_digit_after(_price)

        return rsl

# __
    @staticmethod
    def _digit() -> int:
        """ Digit
        :return: int
        """
        return Pair.digit()

# __
    @staticmethod
    def get_min_lot(_pair: str, trd_mod: Eainp.EA_Trade_Mode) -> float:
        """ get Minimal Lot
        :param _pair
        :param trd_mod
        :return: float
        """
        rsl: float

        rsp = []
        if Util.is_trade_mode_spot_or_margin(trd_mod):
            rsp = MarketBridge.i_get_min_max_step_volume_spotmargin(_pair, trd_mod)

        elif Util.is_trade_mode_future(trd_mod):
            rsp = MarketBridge.i_get_min_max_step_volume_future(_pair)

        rsl = rsp[0]

        return rsl

# __
    @staticmethod
    def get_max_lot(_pair: str, trd_mod: Eainp.EA_Trade_Mode) -> float:
        """ get Maximal Lot
        :param _pair
        :param trd_mod
        :return: float
        """
        rsl: float

        rsp = []
        if Util.is_trade_mode_spot_or_margin(trd_mod):
            # call to exchange interface #
            rsp = MarketBridge.i_get_min_max_step_volume_spotmargin(_pair, trd_mod)

        elif Util.is_trade_mode_future(trd_mod):
            # call to exchange interface #
            rsp = MarketBridge.i_get_min_max_step_volume_future(_pair)

        rsl = rsp[1]

        return rsl

#  --- END CLASS PAIR ---  #


class MMG(object):

    def __init__(self):
        pass  # Not need init for total static class

    @staticmethod
    def calc_mmg_lot(coin_side: Eaenum.CoinSideTyp) -> float:
        """ Calculate Money Management Lot
        :param coin_side:
        :return: float
        """
        rsl: float

        trd_mod = Eainp.EA_Trade_Mode
        _coin = From.from_coinsidetyp_to_coin(coin_side)

        # get Capital
        coin_balance = MarketBridge.get_coin_balance(_coin=_coin, trd_mod=trd_mod)

        # get ratio
        _MMG_ratio = Eainp.EA_MMG_Lot_Capital_PCT / 100

        # calculate
        _lot = coin_balance * _MMG_ratio

        # Normalise Lot
        rsl = Util.normalize_lot(_lot)

        return rsl

# __
    @staticmethod
    def update_mmg_lot():
        """ Update Money Management Lot
        :return: float
        """
        if Util.is_trade_mode_future(Eainp.EA_Trade_Mode):
            Saver.save_last_trade_lot(_lot=Eagbl.EA_MMG_Lot_Calc)

        elif Util.is_trade_mode_spot_or_margin(Eainp.EA_Trade_Mode):
            Saver.save_last_trade_lot_rightcoin(_lot=Eagbl.EA_MMG_Lot_Right_Calc)
            Saver.save_last_trade_lot_leftcoin(_lot=Eagbl.EA_MMG_Lot_Left_Calc)

# __
    @staticmethod
    def get_mmg_daily_valid_lot(coin_side: Eaenum.CoinSideTyp) -> float:   # not need _coinside in futur mode specify no
        """ get Money Management Daily Valide Lot
        :param coin_side:
        :return: float
        """
        rsl: float = 0

        if Util.is_trade_mode_future(Eainp.EA_Trade_Mode):
            rsl = Saver.get_last_trade_lot_saved()

        elif Util.is_trade_mode_spot_or_margin(Eainp.EA_Trade_Mode):
            if Util.is_coinside_left(coin_side):
                rsl = Saver.get_last_trade_lot_leftcoin_saved()

            elif Util.is_coinside_right(coin_side):
                rsl = Saver.get_last_trade_lot_rightcoin_saved()

        return rsl

# __
    @staticmethod
    def get_mmg_daily_max_risk_per_trade_amount():  # don't Need
        """ get MMG daily Max Risk Per Trade Amount
        :return:
        """
        pass

# __
    @staticmethod
    def get_mmg_daily_valid_capital(coin_side: Eaenum.CoinSideTyp) -> float:
        """ get Money Management Daily Valid Capital
        :param coin_side:
        :return: float
        """
        rsl: float = 0

        if Util.is_trade_mode_future(Eainp.EA_Trade_Mode):
            rsl = Saver.get_last_valide_capital_saved()

        elif Util.is_trade_mode_spot_or_margin(Eainp.EA_Trade_Mode):
            if Util.is_coinside_left(coin_side):
                rsl = Saver.get_last_trade_lot_leftcoin_saved()

            elif Util.is_coinside_right(coin_side):
                rsl = Saver.get_last_valide_capital_rightcoin_saved()

        return rsl

#  --- END CLASS MMG ---  #


class Lifetime(object):

    m_starting_dt: dt.datetime

    m_closing_dt: dt.datetime

    m_is_shutdown_asked: bool = False

    def __init__(self):
        pass

    def start_lifetime(self) -> None:
        self.set_bot_lifetime_start()       # Let's consider now as bot starting datetime
        self.set_bot_lifetime_end()         # Let's calculate and define the end

        # self.is_shutdown_asked = False

    def set_bot_lifetime_start(self) -> None:
        self.m_starting_dt = Duration.get_current_time()

    def set_bot_lifetime_end(self) -> None:
        tmstamp = float(self.get_lifetime_timestamp())
        duration_dt = dt.datetime.fromtimestamp(t=tmstamp,
                                                tz=Duration.get_right_timezone())  # ???

        self.m_closing_dt = self.m_starting_dt + duration_dt

# __
    @classmethod
    def get_starting_dt(cls):
        return cls.m_starting_dt

    @classmethod
    def get_starting_date(cls):
        return cls.m_starting_dt.date()

    @classmethod
    def get_starting_time(cls):
        return cls.m_starting_dt.time()

    @classmethod
    def get_closing_dt(cls):
        return cls.m_closing_dt

    @classmethod
    def get_closing_date(cls):
        return cls.m_closing_dt.date()

    @classmethod
    def get_closing_time(cls):
        return cls.m_closing_dt.time()

# __
    @classmethod
    def get_remaining_days(cls) -> int:
        return cls.get_total_lifetime_days() - cls.get_running_days()

    @classmethod
    def get_running_days(cls) -> int:
        return cls.get_lifetime_elapsed_duration().days

    @classmethod
    def get_lifetime_elapsed_duration(cls):
        if not cls.is_lifetime_very_end_reached():
            return dt.datetime.today() - cls.m_starting_dt
        else:
            return cls.m_closing_dt - cls.m_starting_dt

    @classmethod
    def get_total_lifetime_days(cls) -> int:
        return Eainp.EA_Lifetime_Duration_Days

    @classmethod
    def get_lifetime_timestamp(cls) -> int:
        return cls.get_total_lifetime_days() * 24 * 3600 * 1000

    @classmethod
    def is_lifetime_very_end_reached(cls):
        if dt.datetime.today() >= cls.m_closing_dt:
            return True
        else:
            return False

    @classmethod
    def is_shutdown_asked(cls) -> bool:
        return cls.m_is_shutdown_asked

    @classmethod
    def ask_for_shutdown(cls) -> None:
        cls.m_is_shutdown_asked = True

#  --- END CLASS LIFETIME ---  #


class Duration(object):

    def __init__(self):
        pass  # Not need init for total static class

    @staticmethod
    def get_current_time() -> dt.datetime:
        """ Get Time Current Time
        :return: datetime
        """
        rsl: dt.datetime  # = Duration.get_null_datetime()

        _tz = Duration.get_right_timezone()

        rsl = dt.datetime.now(tz=_tz)

        return rsl

# __
    @staticmethod
    def get_right_timezone():
        """ Get Right Time zone
        :return:
        """
        rsl: dt.datetime.tzinfo
        _asFxTime = Eainp.EA_Prefer_Use_ServerTimeThanLocal

        _tz: dt.datetime.tzinfo
        if Util.is_true(_asFxTime):
            _tz = Eaenum.Timezone.utc_moscow.value
        else:
            _tz = Eaenum.Timezone.utc_abidjan.value

        rsl = _tz

        return rsl

# __
    @staticmethod
    def get_null_datetime() -> dt.datetime:
        """ Get Null datetime
        :return: datetime
        """
        return dt.datetime.combine(date=Duration.get_null_date(), time=Duration.get_null_time())

# __
    @staticmethod
    def get_null_date() -> dt.date:
        """ Get Null date
        :return: date
        """
        return dt.date(year=0, month=0, day=0)

# __
    @staticmethod
    def get_null_time() -> dt.time:
        """ Get Null time
        :return: time
        """
        return dt.time(hour=0, minute=0, second=0, microsecond=0)

# __
    @staticmethod
    def is_null_datetime(_datetime: dt.datetime) -> bool:
        """ is Null datetime ?
        :param _datetime:
        :return: bool
        """
        rsl: bool = False

        if Duration.is_null_date(_datetime.date()) and Duration.is_null_time(_datetime.time()):
            rsl = True

        elif _datetime is None:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_null_date(_date: dt.date) -> bool:
        """ is Null date ?
        :param _date:
        :return: bool
        """
        rsl: bool = False

        if _date.year == 0 and _date.month == 0 and _date.day == 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_null_time(_time: dt.time) -> bool:
        """ is Null time ?
        :param _time:
        :return: bool
        """
        rsl: bool = False

        if _time.hour == 0 and _time.minute == 0 and _time.second == 0 and _time.microsecond == 0:
            rsl = True

        return rsl

#  --- END CLASS DURATION ---  #


class Util(object):

    def __init__(self):
        pass  # Not need init for total static class

    @staticmethod
    def is_none(_var) -> bool:
        """ is None ?
        :param _var: type
        :return: bool
        """
        rsl: bool = False

        if _var is None:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_none_(_var: object) -> bool:
        """ is None ?
        :param _var: object
        :return: bool
        """
        rsl: bool = False

        if _var is None:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_zero(_var) -> bool:
        """ is Zero ?
        :param _var
        :return: bool
        """
        rsl: bool = False

        if _var == 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_null(_var) -> bool:
        """ is Null ?
        :param _var
        :return: bool
        """
        rsl: bool = False

        if Util.is_none(_var) or Util.is_zero(_var):
            rsl = True

        return rsl

# __
    @staticmethod
    def is_null_string(_var: str) -> bool:
        """ is Null _String ?
        :param _var:
        :return: bool
        """
        rsl: bool = False

        if _var is None or _var == "":
            rsl = True

        return rsl

# __
    @staticmethod
    def is_null_ticket(_ticket: str) -> bool:
        """ is Null _ticket
        :param _ticket
        :return: bool
        """
        return Util.is_null_string(_ticket)

# __
    @staticmethod
    def is_positive_notnull(_var: float) -> bool:
        """ is Zero ?
        :param _var
        :return: bool
        """
        rsl: bool = False

        if _var > 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def normalize_price(_price: float) -> float:
        """ normalise Price
        :param _price:
        :return: float
        """
        rsl = Util.normalize_float(_price, Pair.digit())

        return rsl

# __
    @staticmethod
    def normalize_price_(_price: float, _digit: int) -> float:
        """ normalise Price
        :param _price:
        :param _digit
        :return: float
        """
        rsl = Util.normalize_float(_price, _digit)

        return rsl

# __
    @staticmethod
    def normalize_float(_price: float, _digit: int) -> float:
        """ normalise float
        :param _price:
        :param _digit:
        :return: float
        """
        rsl: float  # = 0
        _spec: str = ""

        if _digit == 1:
            _spec = ".1f"
        elif _digit == 2:
            _spec = ".2f"
        elif _digit == 3:
            _spec = ".3f"
        elif _digit == 4:
            _spec = ".4f"
        elif _digit == 5:
            _spec = ".5f"
        elif _digit == 6:
            _spec = ".6f"
        elif _digit == 7:
            _spec = ".7f"
        elif _digit == 8:
            _spec = ".8f"
        elif _digit == 9:
            _spec = ".9f"
        elif _digit == 10:
            _spec = ".10f"
        elif _digit == 0:
            _spec = ".0f"

        nbAsString = format(float(_price), _spec)
        rsl = float(nbAsString)

        return rsl

# __
    @staticmethod
    def normalize_float_(_nb: float, _digit: int) -> float:
        """ normalise float
        :param _nb
        :param _digit:
        :return: float
        """
        rsl = From.from_float_to_specific_digit_after(_nb, _digit)

        return rsl

# __
    @staticmethod
    def normalize_lot(_lot: float, c_pair="") -> float:
        """ normalise Lot
        :param _lot:
        :param c_pair: current pair
        :return: float
        """
        Lot_Digit = Pair(c_pair).get_symbol_lot_digit()        # --TO VERIFY--

        return Util.normalize_float(_lot, Lot_Digit)

# __
    @staticmethod
    def is_true(_x: bool) -> bool:
        """ is True ?
        :param _x
        :return: bool
        """
        rsl: bool = False

        if _x is True:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_false(_x: bool) -> bool:
        """ is False ?
        :param _x
        :return: bool
        """
        rsl = not Util.is_true(_x)

        return rsl

# __
    @staticmethod
    def is_position_type_buy(pos_typ: Eaenum.PosType) -> bool:
        """ is Position-Type Buy ?
        :param pos_typ
        :return: bool
        """
        rsl: bool = False

        if pos_typ == Eaenum.PosType.OpBuy:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_position_type_sell(pos_typ: Eaenum.PosType) -> bool:
        """ is Position-Type Sell ?
        :param pos_typ
        :return: bool
        """
        rsl: bool = False

        if pos_typ == Eaenum.PosType.OpSell:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_position_type_opno(pos_typ: Eaenum.PosType) -> bool:
        """ is Position-Type OpNo ?
        :param pos_typ
        :return: bool
        """
        rsl: bool = False

        if pos_typ == Eaenum.PosType.OpNo:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_trade_mode_margin(trd_mod: Eaenum.TradeMode) -> bool:
        """ is Trade Mode _Margin ?
        :param trd_mod
        :return: bool
        """
        rsl: bool = False

        if trd_mod == Eaenum.TradeMode.Margin:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_trade_mode_spot(trd_mod: Eaenum.TradeMode) -> bool:
        """ is Trade Mode _Spot ?
        :param trd_mod
        :return: bool
        """
        rsl: bool = False

        if trd_mod == Eaenum.TradeMode.Spot:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_trade_mode_spot_or_margin(trd_mod: Eaenum.TradeMode) -> bool:
        """ is Trade Mode _Spot Or Margin ?
        :param trd_mod
        :return: bool
        """
        rsl: bool = False

        if Util.is_trade_mode_spot(trd_mod) or Util.is_trade_mode_margin(trd_mod):
            rsl = True

        return rsl

# __
    @staticmethod
    def is_trade_mode_margin_or_future(trd_mod: Eaenum.TradeMode) -> bool:
        """ is Trade Mode _Margin or Future ?
        :param trd_mod
        :return: bool
        """
        rsl: bool = False

        if Util.is_trade_mode_margin(trd_mod) or Util.is_trade_mode_future(trd_mod):
            rsl = True

        return rsl

# __
    @staticmethod
    def is_trade_mode_future(trd_mod: Eaenum.TradeMode) -> bool:
        """ is Trade Mode _Future ?
        :param trd_mod
        :return: bool
        """
        rsl: bool = False

        if trd_mod == Eaenum.TradeMode.Future:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_trade_mode_main_margin() -> bool:
        """ is Trade Mode main _Margin ?
        :return: bool
        """
        trd_mod = Pair.get_trading_mode()
        rsl = Util.is_trade_mode_margin(trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def is_trade_mode_main_spot() -> bool:
        """ is Trade Mode main _Spot ?
        :return: bool
        """
        trd_mod = Pair.get_trading_mode()
        rsl = Util.is_trade_mode_spot(trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def is_trade_mode_main_spot_or_margin() -> bool:
        """ is Trade Mode main _Spot Or Margin ?
        :return: bool
        """
        trd_mod = Pair.get_trading_mode()
        rsl = Util.is_trade_mode_spot_or_margin(trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def is_trade_mode_main_margin_or_future() -> bool:
        """ is Trade Mode main _Margin or Future ?
        :return: bool
        """
        trd_mod = Pair.get_trading_mode()
        rsl = Util.is_trade_mode_margin_or_future(trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def is_trade_mode_main_future() -> bool:
        """ is Trade Mode _Future ?
        :return: bool
        """
        trd_mod = Pair.get_trading_mode()
        rsl = Util.is_trade_mode_future(trd_mod=trd_mod)

        return rsl

# __
    @staticmethod
    def is_future_mode_usd_as_co(future_mode: Eaenum.FutureMod) -> bool:
        """ is Future Mode _Usd as Collateral ?
        :param future_mode
        :return: bool
        """
        rsl: bool = False

        if future_mode == Eaenum.FutureMod.USDAsCo:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_future_mode_coin_as_co(future_mode: Eaenum.FutureMod) -> bool:
        """ is Future Mode _Coin as Collateral ?
        :param future_mode
        :return: bool
        """
        rsl: bool = False

        if future_mode == Eaenum.FutureMod.CoinAsCo:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_trade_direction_upper(trd_direction: Eaenum.TrdDirection) -> bool:
        """ is Trade Direction _Upper ?
        :param trd_direction
        :return bool
        """
        rsl: bool = False

        if trd_direction == Eaenum.TrdDirection.Upper:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_trade_direction_downer(trd_direction: Eaenum.TrdDirection) -> bool:
        """ is Trade Direction _Downer ?
        :param trd_direction
        :return bool
        """
        rsl: bool = False

        if trd_direction == Eaenum.TrdDirection.Downer:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_coinside_left(coin_side: Eaenum.CoinSideTyp):
        """ is Coin Side _Left ?
        :param coin_side
        :return bool
        """
        rsl: bool = False

        if coin_side == Eaenum.CoinSideTyp.coinLeft:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_coinside_right(coin_side: Eaenum.CoinSideTyp):
        """ is Coin Side _Right ?
        :param coin_side
        :return: bool
        """
        rsl: bool = False

        if coin_side == Eaenum.CoinSideTyp.coinRight:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_candle_type_bullish(cdl_typ: Eaenum.CandleTyp):
        """ is Candle Typ _Bullish ?
        :param cdl_typ
        :return: bool
        """
        rsl: bool = False

        if cdl_typ == Eaenum.CandleTyp.Bullish:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_candle_type_bearish(cdl_typ: Eaenum.CandleTyp):
        """ is Candle Typ _Bearish ?
        :param cdl_typ
        :return: bool
        """
        rsl: bool = False

        if cdl_typ == Eaenum.CandleTyp.Bearish:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_candle_type_anonymous(cdl_typ: Eaenum.CandleTyp):
        """ is Candle Typ _Anonymous ?
        :param cdl_typ
        :return bool
        """
        rsl: bool = False

        if cdl_typ == Eaenum.CandleTyp.Anonymous:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_cfdpos_list_src_from_open_poslist(list_src: Eaenum.CFDPosListSrc):
        """ is CFD Position List Source From _Open Position List ?
        :param list_src
        :return bool
        """
        rsl: bool = False

        if list_src == Eaenum.CFDPosListSrc.OpenPosList:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_cfdpos_list_src_from_history_list(list_src: Eaenum.CFDPosListSrc):
        """ is CFD Position List Source From _History List ?
        :param list_src
        :return bool
        """
        rsl: bool = False

        if list_src == Eaenum.CFDPosListSrc.HistoryPosList:
            rsl = True

        return rsl

# __
    @staticmethod
    def get_positions_count(pos_list: list) -> int:
        """ get Position _Count
        :param pos_list
        :return: int
        """
        rsl = len(pos_list)

        return rsl

# __
    @staticmethod
    def add_position_to_list(_pos: object, pos_list: list) -> None:
        """ add Position To _List
        :param _pos
        :param pos_list
        :return: None
        """
        pos_list.append(_pos)

# __
    @staticmethod
    def remove_position_to_list(_pos: object, pos_list: list) -> bool:
        """ remove Position To _List
        :param _pos
        :param pos_list
        :return: bool
        """
        rsl = False

        _posIndex = Util.get_position_inside_list_index(_pos, pos_list)

        if _posIndex != -1:
            pos_list.pop(_posIndex)
            rsl = True

        return rsl

# __
    @staticmethod
    def get_position_inside_list_index(_pos: object, pos_list: list) -> int:    # VERIFY
        """ get Position Inside List _Index
        :param _pos:
        :param pos_list:
        :return: int
        """
        return pos_list.index(_pos)

# __
    @staticmethod
    def position_list_erase(pos_list: list) -> None:
        """ Position List _Erase
        :param pos_list
        :return: None
        """
        pos_list.clear()

# __
    @staticmethod
    def get_position_list_size(pos_list: list) -> int:
        """     __same as get Position List Count__
        get Position-List _Size
        :param pos_list
        :return: int
        """
        return Util.get_positions_count(pos_list)

# __
    @staticmethod
    def get_position_list_latest_index(pos_list: list) -> int:
        """ Get Position List Latest Index
        :param pos_list
        :return: int
        """
        rsl: int  # = 0

        rsl = Util.get_position_list_size(pos_list) - 1

        return rsl

# __
    @staticmethod
    def is_position_list_empty(pos_list: list) -> bool:
        """ is Position List Empty ?
        :param pos_list
        :return: bool
        """
        rsl: bool = False

        if Util.get_position_list_size(pos_list) == 0:
            rsl = True

        return rsl

# __
    @staticmethod
    def is_position_exist_inside_list(_pos, pos_list: list):
        """ is Position Exist _Inside List ?
        :param _pos
        :param pos_list
        :return: bool
        """
        rsl: bool = False

        _posIndex = Util.get_position_inside_list_index(_pos, pos_list)

        if _posIndex > -1:
            rsl = True

        return rsl

#  --- END CLASS UTIL ---  #


class EventHandler(object):

    m_init_executed: bool
    m_timer_tempo: int
    m_timer_last_react_dt: dt.datetime
    m_timer_killed: bool
    m_very_end_state: bool

    def __init__(self):
        self.set_init_executed_state(_state=False)
        self.set_timerkilled_state(_state=False)
        self.set_veryend_state(_state=False)
        self.set_timer(Eainp.EA_TimerSetup_ms)
        self.set_lastreact_datetime(Duration.get_null_datetime())
#

#   getters
    @classmethod
    def get_init_executed_state(cls) -> bool:
        return cls.m_init_executed

    @classmethod
    def get_veryend_state(cls) -> bool:
        return cls.m_very_end_state

    @classmethod
    def get_timerkilled_state(cls) -> bool:
        return cls.m_timer_killed

    @classmethod
    def get_timer_tempo(cls) -> int:
        return cls.m_timer_tempo

    @classmethod
    def get_last_react_datetime(cls) -> dt.datetime:
        return cls.m_timer_last_react_dt
#

#   setters
    @classmethod
    def set_init_executed_state(cls, _state: bool) -> None:
        cls.m_init_executed = _state

    @classmethod
    def set_timerkilled_state(cls, _state: bool) -> None:
        cls.m_timer_killed = _state

    @classmethod
    def set_veryend_state(cls, _state: bool) -> None:
        cls.m_very_end_state = _state

    @classmethod
    def set_timer(cls, time_ms: int) -> None:
        cls.m_timer_tempo = time_ms

    @classmethod
    def set_lastreact_datetime(cls, _dt: dt.datetime) -> None:
        cls.m_timer_last_react_dt = _dt

# __
    @classmethod
    def on_init_call(cls) -> None:
        """ On Init Call
        :return: None
        """
        # Init function will be executed only Once
        if Util.is_false(cls.get_init_executed_state()):

            # Tester Init
            if Eainp.EA_Mode_ActivateTesterMode is True:
                cls.on_tester_init_call()  # On Tester Init Caller

            # On Init
            _Printer.voyant("Event__", ":: Init executing... ::")
            EA.on_init()                                            # init calling is here
            _Printer.voyant("Event__", ":: Init executed ! ::")

            # change state
            cls.set_init_executed_state(_state=True)

# __
    @classmethod
    def on_deinit_call(cls) -> None:
        """ On DeInit Call
        :return: None
        """
        if Util.is_false(cls.get_veryend_state()):

            # Tester DeInit
            if Eainp.EA_Mode_ActivateTesterMode is True:
                cls.on_tester_end_call()                            # asking Tester End Event

            # On DeInit
            _Printer.voyant("Event__", ":: DeInit Executing... ::")
            EA.on_deinit()                                          # asking de-init
            cls.timer_kill()                                        # killing timer
            cls.set_veryend_state(_state=True)                      # change state
            _Printer.voyant("Event__", ":: DeInit executed! ::")

# __
    @classmethod
    def on_timer_call(cls) -> None:
        """ On Timer Call
        :return: None
        """
        # check if timer isn't killed first
        if Util.is_false(cls.get_timerkilled_state()):

            # check timer reached states
            if cls.is_timer_reached():
                _Printer.voyant("Event__", ":: Timer Event executing... ::")
                EA.on_timer_event()                                             # Call of OnTimer Event
                _Printer.voyant("Event__", ":: Timer Event executed ! ::")

# __
    @classmethod
    def is_timer_reached(cls) -> bool:
        """ is Timer Reached ?
        :return: bool
        """
        rsl: bool = False

        _now = Duration.get_current_time()

        _timeRange = _now - cls.m_timer_last_react_dt

        if _timeRange.total_seconds() * 1000 == cls.m_timer_tempo:
            rsl = True

        return rsl

# __
    @classmethod
    def timer_kill(cls) -> None:
        """ timer kill
        :return: None
        """
        cls.set_timerkilled_state(_state=True)
        _Printer.voyant("Event__", "::Timer Killed !::")

# __
    @classmethod
    def on_tester_init_call(cls) -> None:
        """ On Tester Init Call
        :return: None
        """
        _Printer.voyant("Event__", ":: tester Init executing... ::")
        EA.on_tester_init_event()
        _Printer.voyant("Event__", ":: tester Init executed ! ::")

# __
    @classmethod
    def on_tester_end_call(cls) -> None:
        """ On Tester End Call
        :return: None
        """
        _Printer.voyant("Event__", ":: Tester deInit executing... ::")
        EA.on_tester_end_event()
        _Printer.voyant("Event__", ":: Tester deInit executed ! ::")

# __
    @classmethod
    def on_zero_position_call(cls) -> None:
        """ On Zero Position Call
        :return: None
        """
        if EventHandler.is_zero_position():
            _Printer.voyant("Event__", ":: On Zero Position Event Calling... ::")

            EA.on_zero_position_event()     # Zero Position Event calling

            # Check Lifetime very end                               # When zero position running
            if Eagbl.EA_lifetime.is_lifetime_very_end_reached():        # When Lifetime very end reached
                Eagbl.EA_lifetime.ask_for_shutdown()                        # Ask for shutdown
            #

            _Printer.voyant("Event__", ":: On Zero Position Event Handler Ended ! ::")

# __
    @classmethod
    def is_zero_position(cls) -> bool:
        """ is Zero Position ?
        :return: bool
        """
        rsl: bool = False

        # future case
        if Util.is_trade_mode_future(Eainp.EA_Trade_Mode):
            if MarketPosition.get_position_all_count() is 0:
                rsl = True

        # spot or margin
        elif Util.is_trade_mode_spot_or_margin(Eainp.EA_Trade_Mode):
            if not Eagbl.cfdManaja.is_cfdpositions_onmarket():            # when neither position on Market
                rsl = True

        return rsl

# __
    @staticmethod
    def on_running_trade_call() -> None:
        """ On Running Trade Call
        :return: None
        """
        if EventHandler.is_running_trade():
            _Printer.voyant("Event__", ":: On Running Trade Event Calling... ::")
            EA.on_running_trade_event()
            _Printer.voyant("Event__", ":: On Running Trade Event Handler Ended! ::")

# __
    @classmethod
    def is_running_trade(cls) -> bool:
        """ is Running Trade ?
        :return: bool
        """
        rsl: bool = False

        if not cls.is_zero_position():
            rsl = True

        return rsl

# __
    @staticmethod
    def on_tick_call() -> None:
        """ On Tick Call
        :return: None
        """
        if EventHandler.is_tickprice_changed():
            _Printer.voyant("Event__", ":: New Tick Event Calling... ::")
            EA.on_tick_event()
            _Printer.voyant("Event__", ":: On Tick Event Handler Ended ! ::")

# __
    @staticmethod
    def is_tickprice_changed() -> bool:
        """ is Tick Price Changed ?
        :return: bool
        """
        rsl: bool = False

        latest_tick = Candle.get_cdl_current_tickprice()
        if latest_tick != Saver.get_last_tick_saved():
            rsl = True
            Saver.save_last_tick_price(latest_tick)         # save newest tick

        return rsl

# __
    @classmethod
    def on_event_call(cls) -> None:          # std events
        """ On Event Call
        :return: None
        """
        #    ___Event call 1
        cls.on_event(s_param="x")

        #    ___Event call 2

        #    ___Event call 3

        pass

# __
    @staticmethod
    def on_event(s_param: str = None,
                 f_param: float = None,
                 i_param: int = None,
                 l_param: list = None,
                 d_param: dict = None) -> None:         # default event
        """ On Event
        :param s_param:
        :param f_param:
        :param i_param:
        :param l_param:
        :param d_param:

        :return: None
        """
        #    ___X Event Implementation
        if s_param is "x":
            pass
        #

        #    ___Y Event Implementation
        if s_param is "y":
            pass
        #

        #    ___Z Event Implementation
        if s_param is "z":
            pass
        #

# __
    @classmethod
    def on_newbar_call(cls) -> None:
        """ On New Bar Call
        :return: None
        """
        if cls.is_newbar_event():
            _Printer.voyant("Event__", ":: On New Bar Event Calling... ::")
            EA.on_newbar_event()
            _Printer.voyant("Event__", ":: On New Bar Event Handler Called ! ::")

# __
    @classmethod
    def is_newbar_event(cls) -> bool:
        """ is New Bar Event ?
        :return: bool
        """
        rsl: bool = False

        c_bar = Candle(_pos=0)      # recovering current bar

        if c_bar.get_candle_datetime() > Easav.EALastBar_Saved.get_candle_datetime():
            rsl = True
            Saver.save_last_bar(c_bar)
        return rsl

# __
    @classmethod
    def on_newday_call(cls) -> None:
        """ On New Day Call
        :return: None
        """
        if cls.is_new_day():
            _Printer.voyant("Event__", ":: On New Day Event Calling... ::")
            EA.on_newday_event()
            _Printer.voyant("Event__", ":: On New Day Event Handler Called ! ::")

# __
    @classmethod
    def is_new_day(cls) -> bool:
        """ is New Day Event ?
        :return: bool
        """
        rsl: bool = False

        this_date = Duration.get_current_time()
        saved_day = Easav.EALast_SavedDay_date_Saved.day

        if this_date.day != saved_day and not Util.is_null(saved_day):      # Let's compare only day of month
            rsl = True
            Saver.save_last_saved_day_date_saved(this_date)

        # Implementation for initial month saving
        if Util.is_null(saved_day):
            Saver.save_last_saved_day_date_saved(this_date)

        return rsl

# __
    @classmethod
    def on_new_week_call(cls) -> None:
        """ On New Week Call
        :return: None
        """
        if cls.is_new_week():
            _Printer.voyant("Event__", ":: On New Week Event Calling... ::")
            EA.on_new_week_event()
            _Printer.voyant("Event__", ":: On New Week Event Handler Called ! ::")

# __
    @classmethod
    def is_new_week(cls) -> bool:
        """ is New Week Event ?
        :return: bool
        """
        rsl: bool = False

        this_dt = Duration.get_current_time()
        saved_monday_date = Easav.EALast_SaveWeek_monday_date_Saved.date()
        _monday = 1
        if this_dt.weekday() == _monday and this_dt.date() != saved_monday_date\
            and not Duration.is_null_date(saved_monday_date):      # Let's compare only day of month
            rsl = True
            Saver.save_last_save_week_monday_date_saved(this_dt)

        # Implementation for first monday saving
        if Duration.is_null_date(saved_monday_date):
            if this_dt.weekday() == _monday:
                Saver.save_last_save_week_monday_date_saved(this_dt)

        return rsl

# __
    @classmethod
    def on_new_month_call(cls) -> None:
        """ On New Month Call
        :return: None
        """
        if cls.is_new_month():
            _Printer.voyant("Event__", ":: On New Month Event Calling... ::")
            EA.on_new_month_event()
            _Printer.voyant("Event__", ":: On New Month Event Handler Called ! ::")

# __
    @classmethod
    def is_new_month(cls) -> bool:
        """ is New Month Event ?
        :return: bool
        """
        rsl: bool = False

        this_month = Duration.get_current_time().month
        saved_month = Easav.EALast_SaveMonth_Saved

        if this_month != saved_month and not Util.is_null(saved_month):
            rsl = True
            Saver.save_last_save_month_saved(this_month)

        # Implementation for initial month saving
        if Util.is_null(saved_month):
            Saver.save_last_save_month_saved(this_month)

        return rsl

# __
    @classmethod
    def on_new_year_call(cls) -> None:
        """ On New year Call
        :return: None
        """
        if cls.is_new_year():
            _Printer.voyant("Event__", ":: On New Year Event Calling... ::")
            EA.on_new_year_event()
            _Printer.voyant("Event__", ":: On New Year Event Handler Called ! ::")

# __
    @classmethod
    def is_new_year(cls) -> bool:
        """ is New Year Event ?
        :return: bool
        """
        rsl: bool = False

        this_year = Duration.get_current_time().year
        saved_year = Easav.EALast_SaveYear_Saved

        if this_year > saved_year and not Util.is_null(saved_year):
            rsl = True
            Saver.save_last_save_year_saved(this_year)

        # Implementation for initial month saving
        if Util.is_null(saved_year):
            Saver.save_last_save_year_saved(this_year)

        return rsl

# __
    @classmethod
    def events_process(cls) -> None:             # Loops of event --Must be called in Main Loops
        """ Events Process
        :return: None
        """
        #   Base Events call
        cls.on_init_call()                        # On Init Caller            # It will execute itself only on time
        cls.on_timer_call()                       # Timer Caller
        cls.on_tick_call()                        # On Tick Caller
        cls.on_running_trade_call()               # On Running Trade Caller
        cls.on_zero_position_call()               # On Zero Position Caller
        cls.on_event_call()                       # On Event Caller
        cls.on_newbar_call()                      # On New Bar Caller

        #  Extra Events Call
        cls.on_newday_call()                      # On New Day Caller
        cls.on_new_week_call()                    # On New Day Caller
        cls.on_new_month_call()                   # On New Month Caller
        cls.on_new_year_call()                    # On New Year Caller

#  --- END CLASS EVENT ---  #


class Saver(object):

    def __init__(self):
        pass  # Not need init for total static class

# ...............   bar
    @staticmethod
    def get_last_bar_saved():
        """ get Last Bar Saved
        :return: Candle
        """
        return Easav.EALastBar_Saved

# __
    @staticmethod
    def save_last_bar(_cdl: Candle):
        """ save Last Bar
        :param _cdl
        :return: None
        """
        Easav.EALastBar_Saved = _cdl

# __
    @staticmethod
    def get_last_tick_saved() -> float:
        """ get Last Tick Saved
        :return: float
        """
        return Easav.EALastTickPrice_Saved

# __
    @staticmethod
    def save_last_tick_price(tick_price: float):
        """ save Last Tick Price
        :param tick_price: float
        :return: None
        """
        Easav.EALastTickPrice_Saved = tick_price

# __
    @staticmethod
    def get_last_deviation_bar_saved() -> Candle:
        """ get Last Deviation Bar Saved
        :return: Candle
        """
        return Easav.EALastBar_Saved

# __
    @staticmethod
    def save_last_deviation_bar(_cdl: Candle):
        """ save Last Deviation Bar
        :param _cdl
        :return: None
        """
        Easav.EALastDeviationBar_Saved = _cdl
# ...............

# ...............   volume
    @staticmethod
    def get_last_trade_lot_saved() -> float:
        """ get Last Trade Lot Saved
        :return: float
        """
        return Easav.EALastTradeLot_Saved

# __
    @staticmethod
    def save_last_trade_lot(_lot: float):
        """ save Last Trade Lot
        :param _lot
        :return: None
        """
        Easav.EALastTradeLot_Saved = _lot

# __
    @staticmethod
    def get_last_trade_lot_leftcoin_saved() -> float:
        """ get Last Trade Lot _Left Coin Saved
        :return: float
        """
        return Easav.EALastTradeLot_LeftCoin_Saved

# __
    @staticmethod
    def save_last_trade_lot_leftcoin(_lot: float):
        """ save Last Trade Lot _Left Coin
        :param _lot
        :return: None
        """
        Easav.EALastTradeLot_LeftCoin_Saved = _lot

# __
    @staticmethod
    def get_last_trade_lot_rightcoin_saved() -> float:
        """ get Last Trade Lot _Right Coin Saved
        :return: float
        """
        return Easav.EALastTradeLot_RightCoin_Saved

# __
    @staticmethod
    def save_last_trade_lot_rightcoin(_lot: float):
        """ save Last Trade Lot _Right Coin
        :param _lot
        :return: None
        """
        Easav.EALastTradeLot_RightCoin_Saved = _lot
# ...............

# ...............  capital
    @staticmethod
    def get_last_valide_capital_saved() -> float:
        """ get Last _valide Capital Saved
        :return: float
        """
        return Easav.EALast_valideCapital_Saved

# __
    @staticmethod
    def save_last_valide_capital(_cap: float):
        """ save Last _valide Capital
        :param _cap
        :return: float
        """
        Easav.EALast_valideCapital_Saved = _cap

# __
    @staticmethod
    def get_last_valide_capital_leftcoin_saved() -> float:
        """ get Last _valide Capital Left coin Saved
        :return: float
        """
        return Easav.EALast_valideCapital_Left_Saved

# __
    @staticmethod
    def save_last_valide_capital_leftcoin(_cap: float):
        """ save Last _valide Capital Left Coin
        :param _cap
        :return: None
        """
        Easav.EALast_valideCapital_Left_Saved = _cap

# __
    @staticmethod
    def get_last_valide_capital_rightcoin_saved() -> float:
        """ get Last _valide Capital Right coin Saved
        :return: float
        """
        return Easav.EALast_valideCapital_Right_Saved

# __
    @staticmethod
    def save_last_valide_capital_rightcoin(_cap: float):
        """ save Last _valide Capital Right Coin
        :param _cap
        :return: None
        """
        Easav.EALast_valideCapital_Right_Saved = _cap
# ...............

# ............... Date and Timing
# __
    @staticmethod
    def get_last_saved_day_date_saved() -> dt.datetime:
        """ get Last _saved day _date Saved
        :return: datetime
        """
        return Easav.EALast_SavedDay_date_Saved

# __
    @staticmethod
    def save_last_saved_day_date_saved(_dt: dt.datetime):
        """ save Last _saved day _date Saved
        :param _dt:
        :return: None
        """
        Easav.EALast_SavedDay_date_Saved = _dt

# __
    @staticmethod
    def get_last_save_week_monday_date_saved() -> dt.datetime:
        """ get Last _saved Week _Monday date Saved
        :return: datetime
        """
        return Easav.EALast_SaveWeek_monday_date_Saved

# __
    @staticmethod
    def save_last_save_week_monday_date_saved(_dt: dt.datetime):
        """ save Last _saved Week _Monday date Saved
        :param _dt:
        :return: None
        """
        Easav.EALast_SaveWeek_monday_date_Saved = _dt

# __
    @staticmethod
    def get_last_save_month_saved() -> int:
        """ save Last _saved Month Saved
        :return: int
        """
        return Easav.EALast_SaveMonth_Saved

# __
    @staticmethod
    def save_last_save_month_saved(_mt: int):
        """ save Last _saved Month Saved
        :param _mt:
        :return: None
        """
        Easav.EALast_SaveMonth_Saved = _mt

# __
    @staticmethod
    def get_last_save_year_saved() -> int:
        """ get Last _saved Year Saved
        :return: int
        """
        return Easav.EALast_SaveYear_Saved

# __
    @staticmethod
    def save_last_save_year_saved(_year: int):
        """ save Last _saved Year Saved
        :param _year:
        :return: None
        """
        Easav.EALast_SaveYear_Saved = _year

# ...............

#  --- END CLASS SAVER ---  #


class _Printer(object):

    def __init__(self):
        pass  # Not need init for total static class

# ___
    @staticmethod
    def voyant(_title, _msg):
        """ Voyant
        :param _title:
        :param _msg:
        :return: None
        """
        if Eainp.EA_Mode_Debugger:
            print(_title+' : '+_msg)

# __
    @staticmethod
    def voyant_test(_title, _msg):
        """ Voyant Test
        :param _title:
        :param _msg:
        :return: None
        """
        if Eainp.EA_Mode_TestViaVoyant:
            print(_title+' : '+_msg)
        else:
            print("Warning: This msg can only be displayed in 'Test Via Voyant mode' !!!")

# __
    @staticmethod
    def log():      # log in a file
        pass

#  --- END CLASS _PRINTER ---  #


class UserAction(object):

    def __init__(self):
        pass  # Not need init for total static class

    def interrupt_bot(self):
        pass

    def run_bot(self):
        pass

#  --- END CLASS USER-ACTION ---  #


class ExChangeInterface:

    def __init__(self):
        pass  # Not need init for total static class

    @staticmethod
    def get_exchange(selected_xch: str = None):
        rsl = 0
        # ::::
        if selected_xch is None:
            selected_xch = Eainp.EA_DEFAULT_EXCHANGE
        # ::::

        # ::::
        if selected_xch == Eaenum.SupportedExchange.Binance:
            rsl = BinanceInterface()
        elif selected_xch == Eaenum.SupportedExchange.CoinBase:
            rsl = CoinbaseInterface()
        # ::::

        return rsl

# __
    @staticmethod
    def get_exchange_key():
        return Eainp.EA_API_Key

# __
    @staticmethod
    def get_exchange_secret():
        return Eainp.EA_API_Secret

# __
    @staticmethod
    def get_exchange_pw():
        return Eainp.EA_API_PW

#  --- END CLASS EXCHANGE-INTERFACE ---  #
