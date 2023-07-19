
###########################################
#             BINANCE INTERFACE           #
###########################################

# from config import ConnectClient

from eazcore.lib import *
# import eaheader.inputs as Eainp
import eaheader.enums as Eaenum
# import eaheader.globals as Eagbl

import ccxt as cx
import asyncio

import os
import sys
from pprint import pprint


class BinanceInterface(object):

    # client = ConnectClient().make_connection()

    _pair = Eagbl.EAPair  # Pair Obj
    _coinLeft = _pair.get_coin_left()
    _coinRight = _pair.get_coin_right()
    #

    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(root + '/python')

    m_exchange: cx.binance = None
    m_markets: dict = {}
    m_symbol: str = None
    m_position_very_last_filled_onmarket_infos: dict = {}

    if Util.is_trade_mode_spot_or_margin(Eainp.EA_Trade_Mode):
        m_exchange = cx.binance(config={
            'apiKey': Eainp.EA_API_Key,
            'secret': Eainp.EA_API_Secret,
            'password': Eainp.EA_API_PW,
        })

    elif Util.is_trade_mode_future(Eainp.EA_Trade_Mode):

        # When Usd As Collateral Mode
        if Util.is_future_mode_usd_as_co(Eainp.EA_Future_Mode):
            m_exchange = cx.binanceusdm(config={
                'apiKey': Eainp.EA_API_Key,
                'secret': Eainp.EA_API_Secret,
                'password': Eainp.EA_API_PW,
            })

        # When Coin As Collateral Mode
        elif Util.is_future_mode_coin_as_co(Eainp.EA_Future_Mode):
            m_exchange = cx.binancecoinm(config={
                'apiKey': Eainp.EA_API_Key,
                'secret': Eainp.EA_API_Secret,
                'password': Eainp.EA_API_PW,
            })

    m_markets = m_exchange.load_markets()

    m_exchange.verbose = Eainp.EA_Exc_Verbose  # for debugging purpose only if necessary
    m_exchange.enableRateLimit = Eainp.EA_Exc_Enable_RateLimit  # Rate Limit Situation
    m_exchange.rateLimit = Eainp.EA_Exc_RateLimit  # Rate Limit

    m_symbol = Pair.get_symbol()

    def __init__(self):
        pass
    # __

# getters
    def get_exchange(self):
        return self.m_exchange
#

# setters
# ..............................

# .............................. Get Partial Infos - Ticks
# __
    @classmethod
    def i_get_ticker_price_bid_ask(cls, _pair: str, trd_mod: Eaenum.TradeMode) -> list:
        """ get Ticker price Bid
        :param _pair:
        :param trd_mod:
        :return: []
        """
        rsl: list

        params = {
            'type': trd_mod.value
        }

        # Process
        ticker_data = {}
        try:
            # rsp = cx.binance.fetch_bids_asks(symbols=_pair, params={})
            # pprint(rsp)

            ticker_data = cls.m_exchange.fetch_ticker(symbol=_pair, params=params)

        except Exception as e:
            print('Error: Tick _Bid _Ask Request Failed')
            print(type(e).__name__, str(e))

        # ask = float(ticker_data['info']['bidPrice'])                 # recover raw binance ticker data
        bid = float(ticker_data['bid'])

        # ask = float(ticker_data['info']['askPrice'])                 # recover raw binance ticker data
        ask = float(ticker_data['ask'])  # already safe parsed

        # must be normalised
        bid_precis = float(cls.m_exchange.price_to_precision(symbol=_pair, price=bid))
        ask_precis = float(cls.m_exchange.price_to_precision(symbol=_pair, price=ask))

        rsl = [bid_precis, ask_precis]

        return rsl

# __
    @classmethod
    def i_get_ticker_price_bid(cls, _pair: str, trd_mod: Eaenum.TradeMode) -> float:
        """ get Ticker price Bid
        :param _pair:
        :param trd_mod:
        :return: float
        """
        rsl: float

        tick = cls.i_get_ticker_price_bid_ask(_pair=_pair, trd_mod=trd_mod)

        rsl = tick[0]

        return rsl

# __
    @classmethod
    def i_get_ticker_price_ask(cls, _pair: str, trd_mod: Eaenum.TradeMode) -> float:
        """ get Ticker price Ask
        :param _pair:
        :param trd_mod:
        :return: float
        """
        rsl: float

        tick = cls.i_get_ticker_price_bid_ask(_pair=_pair, trd_mod=trd_mod)

        rsl = tick[1]

        return rsl

# __
    @classmethod
    def i_get_candle_current_tick_price(cls, _pair: str, trd_mod: Eaenum.TradeMode,
                                        trd_direction: Eaenum.TrdDirection) -> float:
        """ get Candle current Tick Price
        :param _pair:
        :param trd_mod:
        :param trd_direction
        :return: float
        """
        rsl: float = 0

        if Util.is_trade_direction_upper(trd_direction):
            rsl = cls.i_get_ticker_price_ask(_pair=_pair, trd_mod=trd_mod)

        elif Util.is_trade_direction_downer(trd_direction):
            rsl = cls.i_get_ticker_price_bid(_pair=_pair, trd_mod=trd_mod)

        return rsl

# __
    @classmethod
    def i_get_candle_info_by_datetime(cls, _dt: dt.datetime, _timeframe: Eaenum.TimeFrames, _symbol: str) -> list:
        """ get Candle Infos _by Datetime
        :param _dt:
        :param _timeframe:
        :param _symbol:
        :return: list
        """
        rsl: list  # = []

        params = {}

        # Process
        rsp = {}
        try:
            rsp = cls.m_exchange.fetch_ohlcv(symbol=_symbol, timeframe=_timeframe, since=None, limit=None,
                                             params=params)

        except Exception as e:
            print('Error: Candle Info Request Failed')
            print(type(e).__name__, str(e))

        rsl = list(rsp)

        return rsl

# __
    @classmethod
    def i_get_candle_info_by_position(cls, _pos: int, _timeframe: Eaenum.TimeFrames, _symbol: str) -> list:
        """ get Candle Info _By Position
        :param _pos:
        :param _timeframe:
        :param _symbol:
        :return: []
        """
        rsl: list

        # according to parsing must use
        # method = publicGetKlines or fapiPublicGetKlines or dapiPublicGetKlines

        # let's use mark price : auto set of method | can use instead: fetch_mark_ohlcv()
        _params = {
            'price': 'mark'
        }

        _param = {}
        if Util.is_trade_mode_spot_or_margin(Eainp.EA_Trade_Mode):
            _param = {
                'method': 'dapiPublicGetKlines',
            }

        elif Util.is_trade_mode_future(Eainp.EA_Trade_Mode):
            _param = {
                'method': 'fapiPublicGetKlines'
            }

        # let's extends input parameters
        cls.m_exchange.extend(_param, _params)

        # Process
        ohlcvpt = []
        ohlcvc_i = []

        try:
            rsp = cls.m_exchange.fetch_ohlcvc(symbol=_symbol, timeframe=_timeframe, since=None, limit=500,
                                              params=_params)

            ohlcvc_i = rsp[_pos]          # getting specific position OHLCVP inside list

        except Exception as e:
            print('Error: Candle infos Request Failed')
            print(type(e).__name__, str(e))

        # parsing is here
        opendt_ohlcv_closedt = cls.m_exchange.parse_ohlcv(ohlcv=ohlcvc_i, market=None)

        # let's reorder
        ohlcvpt.append(opendt_ohlcv_closedt[1])      # open
        ohlcvpt.append(opendt_ohlcv_closedt[2])      # high
        ohlcvpt.append(opendt_ohlcv_closedt[3])      # low
        ohlcvpt.append(opendt_ohlcv_closedt[4])      # close
        ohlcvpt.append(opendt_ohlcv_closedt[5])      # vol
        ohlcvpt.append(_pos)                         # pos
        ohlcvpt.append(opendt_ohlcv_closedt[0])      # Open Time

        # ohlcvpt.append(odt_ohlcv_cdt[6])    # Close Time - don't need

        rsl = ohlcvpt

        return rsl

# __
    @classmethod
    def i_get_coin_balances_spot(cls, _coin: str) -> dict:
        """ get coin Balance _spot
        :param _coin:
        :return:
        """
        """
        returned by Exchange
            {   "free":     "float",
                "locked":   "float",
            }
        """
        rsl: dict  # = {}

        # retrieve the right coin balance
        params = {
            'type': 'spot'
        }

        # process
        rsp = {}
        try:
            rsp = cls.m_exchange.fetch_balance(params=params)

        except Exception as e:
            print('Error: Transfert Request Failed')
            print(type(e).__name__, str(e))

        the_coin_asset = {}

        # recover inside internal dict list
        for currency in rsp['balances']:  # seek inside 'balances'
            if currency['asset'] == _coin:
                the_coin_asset = currency
                break

        rsl = the_coin_asset

        return rsl

# __
    @classmethod
    def i_get_coin_balance_spot(cls, _coin: str,
                                blc_typ: Eaenum.SpotBalanceTyp = Eaenum.SpotBalanceTyp.SFree) -> float:
        """ get coin Balance _spot
        :param _coin:
        :param blc_typ:
        :return:
        """

        the_coin_asset = cls.i_get_coin_balances_spot(_coin=_coin)

        # blc: str
        # blc = the_coin_asset[blc_typ.value]  # get desire balance typ: borrowed | free | interest | locked | netAsset

        rsl = cls.m_exchange.safe_float(the_coin_asset, blc_typ.value)

        return rsl

# __
    @classmethod
    def i_get_coin_balances_margin(cls, _coin: str) -> dict:
        """ get coin Balance _margin
        :param _coin:
        :return: float
        """
        """
        returned by Exchange
            {   "borrowed": "float",
                "free":     "float",
                "interest": "float",
                "locked":   "float",
                "netAsset": "float"
            }
        """
        rsl: dict  # = {}

        # retrieve the right coin balance
        params = {
            'type': 'margin'
        }

        # process
        rsp = {}
        try:
            rsp = cls.m_exchange.fetch_balance(params=params)

        except Exception as e:
            print('Error: Transfert Request Failed')
            print(type(e).__name__, str(e))

        the_coin_asset = {}

        # recover inside internal dict list
        for currency in rsp['userAssets']:     # seek inside 'userAssets'
            if currency['asset'] == _coin:
                the_coin_asset = currency
                break

        rsl = the_coin_asset

        return rsl

# __
    @classmethod
    def i_get_coin_balance_margin(cls, _coin: str,
                                  blc_typ: Eaenum.MarginBalanceTyp = Eaenum.MarginBalanceTyp.MFree) -> float:
        """ get coin Balance _margin
        :param _coin:
        :param blc_typ:
        :return: float

        Get desire balance typ: borrowed | free | interest | locked | netAsset
        """

        # Process
        the_coin_asset = cls.i_get_coin_balances_margin(_coin=_coin)

        rsl = cls.m_exchange.safe_float(the_coin_asset, blc_typ.value)

        return rsl

# __
    @classmethod
    def i_get_coin_balances_future(cls, _coin: str) -> dict:
        """ get coin Balances All _future
        :param _coin:
        :return: {}
        """

        """
        returned By Exchange
              {
                 "walletBalance":       "float",
                 "unrealizedProfit":    "float",
                 "marginBalance":       "float",
                 "maintMargin":         "float",
                 "initialMargin":       "float",
                 "positionInitialMargin":   "float",
                 "openOrderInitialMargin":  "float",
                 "maxWithdrawAmount":       "float",
                 "crossWalletBalance":      "float",
                 "crossUnPnl":              "float",
                 "availableBalance":        "float"
             }
        """
        rsl: dict  # = {}

        # retrieve the right coin balance
        params = {
            'type': 'future',
            'method': 'fapiPrivateV2GetAccount'
        }

        # process
        rsp = {}
        try:
            rsp = cls.m_exchange.fetch_balance(params=params)

        except Exception as e:
            print('Error: Transfert Request Failed')
            print(type(e).__name__, str(e))

        the_coin_asset = {}

        # recover inside internal dict list
        for currency in rsp['assets']:  # seek inside 'userAssets'
            if currency['asset'] == _coin:
                the_coin_asset = currency
                break

        rsl = the_coin_asset  # the wished {}

        return rsl

# __
    @classmethod
    def i_get_coin_balance_future(cls, _coin: str,
                                  f_blc_typ: Eaenum.FutureBalanceTyp = Eaenum.FutureBalanceTyp.FWalletBalance
                                  ) -> float:
        """ get coin Balance _future
        :param _coin:
        :param f_blc_typ:
        :return: float
        """

        the_coin_asset = cls.i_get_coin_balances_future(_coin=_coin)

        rsl = cls.m_exchange.safe_float(the_coin_asset, f_blc_typ.value)

        return rsl

# __
    @classmethod
    def i_replenish_coin(cls, _coin: str, _amount: float) -> dict:
        """ replenish coin
        :param _coin:
        :param _amount:
        :return: bool
        """

        # request response
        #     {
        #         "tranId": 13526853623,
        #         "amount": __,
        #         "currency": __,
        #         "fromAccount": __,
        #         "toAccount": __,
        #     }
        #

        rsl: dict

        params = {
            'type': Eainp.EA_Trade_Mode.value
        }

        # process
        coin_code = cls.m_exchange.common_currency_code(currency=Pair.get_symbol())

        rsp = {}
        try:
            rsp = cls.m_exchange.transfer(code=coin_code, amount=_amount,
                                          fromAccount=Eagbl.EAPair.get_opposite_coin(_coin),
                                          toAccount=_coin,
                                          params=params)

        except Exception as e:
            print('Error: Transfert Request Failed')
            print(type(e).__name__, str(e))

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_replenish_coin_(cls, _coin: str, _amount: float) -> int:
        """ replenish coin
        :param _coin:
        :param _amount:
        :return idTrans: int
        """

        rsp = cls.i_replenish_coin(_coin=_coin, _amount=_amount)

        id_trans = cls.m_exchange.safe_integer(rsp, "tranId")

        rsl = id_trans

        return rsl

# __
    @classmethod
    def i_replenish_coin__(cls, _coin: str, _amount: float) -> bool:
        """ replenish coin
        :param _coin:
        :param _amount:
        :return: bool
        """
        id_trans = cls.i_replenish_coin_(_coin=_coin, _amount=_amount)

        # ::::
        if Util.is_positive_notnull(id_trans):
            rsl = True
        else:
            rsl = False
        # ::::

        return rsl

# __
    @classmethod
    def i_withdraw_coin(cls, _coin: str, _amount: float, _wallet_adr: str) -> dict:
        """ withdraw coin
        :param _coin:
        :param _amount:
        :param _wallet_adr:
        :return:
        """

        #  request result
        #   {
        #      'info': '__',
        #      'id': '9a67628b16ba4988ae20d329333f16bc',
        #   }
        
        rsl: dict  # = {}

        # process
        params = {
            'type': Eainp.EA_Trade_Mode.value
        }

        tag = None     # ???

        rsp = {}
        try:
            # cx.binance.market_id(symbol=)
            coin_code = cls.m_exchange.common_currency_code(currency=Pair.get_symbol())     # currency code

            rsp = cls.m_exchange.withdraw(code=coin_code,
                                          amount=_amount,
                                          address=_wallet_adr,
                                          tag=tag,
                                          params=params)

        except Exception as e:
            print('Error: Withdrawal Request Failed')
            print(type(e).__name__, str(e))

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_withdraw_coin_(cls, _coin: str, _amount: float, _wallet_adr: str) -> str:
        """ withdraw coin
        :param _coin:
        :param _amount:
        :param _wallet_adr:
        :return id: str
        """
        rsl: str

        rsp = cls.i_withdraw_coin(_coin=_coin, _amount=_amount, _wallet_adr=_wallet_adr)

        _id = cls.m_exchange.safe_string(rsp, 'id')

        rsl = _id

        return rsl

# __
    @classmethod
    def i_withdraw_coin__(cls, _coin: str, _amount: float, _wallet_adr: str) -> bool:
        """ withdraw coin
        :param _coin:
        :param _amount:
        :param _wallet_adr:
        :return: bool
        """
        rsl: bool

        _id = cls.i_withdraw_coin_(_coin=_coin, _amount=_amount, _wallet_adr=_wallet_adr)

        # ::::
        if _id is not '':
            rsl = True
        else:
            rsl = False
        # ::::

        return rsl

# __
    @classmethod
    def i_swap_coin(cls, coin_src: str, coin_dst: str, _amount: float) -> dict:
        """ swap coin
        :param coin_src:
        :param coin_dst:
        :param _amount:
        :return: {}
        """
        rsl: dict  # = {}

        params = {
            'type': Eainp.EA_Trade_Mode.value
        }

        # retrieve the right coin balance
        # ...

        # swap ??? ---> <---

        # process
        rsp = {}
        try:
            coin_code = cls.m_exchange.common_currency_code(currency=Pair.get_symbol())  # currency code ???

            rsp = cls.m_exchange.transfer(code=coin_code,
                                          fromAccount=coin_src,
                                          toAccount=coin_dst,
                                          amount=_amount,
                                          params=params)

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_swap_coin_(cls, coin_src: str, coin_dst: str, _amount: float) -> bool:
        """ swap coin
        :param coin_src:
        :param coin_dst:
        :param _amount:
        :return: bool
        """
        rsl: bool = False

        rsp = cls.i_swap_coin(coin_src=coin_src,
                              coin_dst=coin_dst,
                              _amount=_amount)

        # rsl =

        return rsl

# __
    @classmethod
    def i_get_min_max_step_volume_spotmargin(cls, _pair: str, trd_mod: Eaenum.TradeMode) -> list:
        """ get min max step _Volume (Lot) spot-margin
        :param _pair:
        :param trd_mod:
        :return: [min,max,step]
        """
        rsl: list

        params = {
            'type': str.lower(trd_mod.value)
        }

        # process
        rsp = {}
        try:
            rsp = cls.m_exchange.fetch_markets(params=params)   # ???

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        the_pair_asset = {}
        # recover inside internal dict list
        for data in rsp['symbols']:  # seek inside 'userAssets'
            if data['symbol'] == _pair:
                the_pair_asset = data
                break

        wanted_asset = {}
        # recover inside internal dict list
        for data in the_pair_asset['filters']:  # seek inside 'userAssets'
            if data['filterType'] == 'MARKET_LOT_SIZE':
                wanted_asset = data
                break

        minLot: str
        maxLot: str
        stepSize: str
        minLot = wanted_asset['minQty']
        maxLot = wanted_asset['maxQty']
        stepSize = wanted_asset['stepSize']

        rsl = [float(minLot), float(maxLot), float(stepSize)]

        return rsl

# __
    @classmethod
    def i_get_min_max_step_volume_future(cls, _pair: str) -> list:
        """ get min max step _Volume future
        :param _pair:
        :return: [min,max,step]
        """
        rsl: list

        # retrieve the right coin balance
        params = {
            'type': Eaenum.TradeMode.Future.value,       # need specify too future mod params ?
        }

        # process
        rsp = {}
        try:
            rsp = cls.m_exchange.fetch_markets(params=params)  # ???

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        the_pair_asset = {}
        # recover inside internal dict list
        for data in rsp['symbols']:  # seek inside 'userAssets'
            if data['symbol'] == _pair or data['pair'] == _pair:
                the_pair_asset = data
                break

        wanted_asset = {}
        # recover inside internal dict list
        for data in the_pair_asset['filters']:  # seek inside 'userAssets'
            if data['filterType'] == 'MARKET_LOT_SIZE':
                wanted_asset = data
                break

        minLot: str
        maxLot: str
        stepSize: str
        minLot = wanted_asset['minQty']
        maxLot = wanted_asset['maxQty']
        stepSize = wanted_asset['stepSize']

        rsl = [float(minLot), float(maxLot), float(stepSize)]

        return rsl
# ...............................

# ............................... Partials Infos - Position or Order
    @classmethod
    def i_get_position_infos(cls, _ticket: str, trd_mod: Eaenum.TradeMode) -> dict:
        """ get Position Infos
        :param _ticket:
        :param trd_mod:
        :return: {}
        """
        rsl: dict = {}

        # __spot margin
        if Util.is_trade_mode_spot_or_margin(trd_mod):
            rsl = cls.i_get_position_infos_spotmargin(_ticket=_ticket, trd_mod=trd_mod)

        # __future
        elif Util.is_trade_mode_future(trd_mod):
            rsl = cls.i_get_position_infos_future(_ticket=_ticket)

        return rsl

# __
    @classmethod
    def i_get_position_infos_spotmargin(cls, _ticket: str, trd_mod: Eaenum.TradeMode) -> dict:
        """ get position infos _spot-margin
        :param _ticket:
        :param trd_mod:
        :return:
                 {
                     "symbol": str,
                     "id": int,
                     "orderId": int,
                     "price": "float",
                     "qty": "float",
                     "commission": "float",
                     "commissionAsset": str,
                     "time": timestamp,
                     "isBuyer": bool,
                     "isMaker": bool,
                     "isBestMatch": bool,
                 }
            Return by Request
        """
        rsl: dict

        params = {
            'type': trd_mod.value
        }

        # process
        trades_data = {}
        try:
            # symbol = Pair.get_symbol()
            symbol = cls.i_get_position_symbol(_ticket)

            trades_data = cls.m_exchange.fetch_my_trades(symbol=symbol, since=None, limit=500,
                                                         params=params)

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        the_trade = {}
        for trd in trades_data:
            if trd['id'] == int(_ticket):
                the_trade = trd
                break

        rsl = the_trade

        return rsl

# __
    @classmethod
    def i_get_position_infos_future(cls, _ticket: str) -> dict:
        """ get position infos _future
        :param _ticket:
        :return:
                {
                     "accountId": int,
                     "buyer": bool,
                     "commission": "float",
                     "commissionAsset": str,
                     "counterPartyId": int,
                     "id": int,
                     "maker": bool,
                     "orderId": int,
                     "price": "float",
                     "qty": "float",
                     "quoteQty": "float",
                     "realizedPnl": "float",
                     "side": str,
                     "symbol": str,
                     "time": timestamp
                 }
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Future.value,
        }

        # process
        trades_data = {}
        try:
            symbol = cls.i_get_position_symbol(_ticket)

            trades_data = cls.m_exchange.fetch_my_trades(symbol=symbol, since=None, limit=500,
                                                         params=params)

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        the_trade = {}
        for trd in trades_data:
            if trd['id'] == int(_ticket):
                the_trade = trd
                break

        rsl = the_trade

        return rsl

# __
    @classmethod
    def i_is_position_filled_on_market(cls, _ticket: str) -> bool:
        """ is Position filled On Market ?
        :param _ticket:
        :return: bool
        """
        rsl: bool = False

        # Process

        return rsl

# __
    @classmethod
    def i_get_position_very_last_filled_onmarket_infos(cls) -> dict:
        """ get Position very last Filled On Market _Infos
        :return: {}
        """
        rsl: dict

        # Process
        rsl = cls.m_position_very_last_filled_onmarket_infos

        return rsl

# __
    @classmethod
    def i_set_position_very_last_filled_onmarket_infos(cls, last_position_filled: dict) -> None:
        """ get Position very last Filled On Market _Infos
        :return: None
        """

        cls.m_position_very_last_filled_onmarket_infos = last_position_filled
    # __

# __
    @classmethod
    def i_set_leverage(cls, lever: int) -> bool:
        """ set Leverage
        :param lever:
        :return: bool
        """
        rsl: bool  # = False

        # __
        if lever < 1:
            lever = 1
        elif lever > 125:
            lever = 125
        # __

        params = {
            'type': Pair.get_trading_mode().value
        }

        _symbol = Pair.get_symbol()

        try:
            rsp = cls.m_exchange.set_leverage(leverage=lever, symbol=_symbol, params=params)

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        # rsp

        rsl = True  # rsp ???

        return rsl
    # __

# __
    @classmethod
    def i_get_last_json_response(cls):
        """ get Last Json Response
        :return: Any
        """

        return cls.m_exchange.last_json_response
    # __

# __
    @classmethod
    def i_get_last_http_response(cls):
        """ get Last HTTP Response
        :return: Any
        """

        return cls.m_exchange.last_http_response
    # __

# __
    @classmethod
    def i_get_position_very_last_filled_onmarket_ticket(cls) -> str:
        """ get Position very Last Filled onMarket _Ticket
        :return: str
        """
        rsl: str  # = ""

        # Process
        rsp = cls.i_get_position_very_last_filled_onmarket_infos()

        _id = (cls.m_exchange.safe_string(rsp, 'id') if 'id' in rsp
               else cls.m_exchange.safe_string(rsp, 'orderId'))

        rsl = _id

        return rsl

# __
    @classmethod
    def i_get_position_closed_infos(cls, _ticket: str, trd_mod: Eaenum.TradeMode) -> dict:
        """ get Position closed Infos
        :param _ticket:
        :param trd_mod:
        :return: {}
        """
        rsl: dict = {}

        # __spot margin
        if Util.is_trade_mode_spot_or_margin(trd_mod):
            rsl = cls.i_get_position_closed_infos_spotmargin(_ticket=_ticket, trd_mod=trd_mod)

        # __future
        elif Util.is_trade_mode_future(trd_mod):
            rsl = cls.i_get_position_closed_infos_future(_ticket=_ticket)

        return rsl

# __
    @classmethod
    def i_get_position_closed_infos_spotmargin(cls, _ticket: str, trd_mod: Eaenum.TradeMode) -> dict:
        """ get position closed infos _spot or margin
        :param _ticket:
        :param trd_mod:
        :return:
                 {
                     "symbol": str,
                     "orderId": int,
                     "clientOrderId": str,
                     "price": "float",
                     "origQty": "float",
                     "executedQty": "float",
                     "cummulativeQuoteQty": "float",
                     "status": str,
                     "timeInForce": str,
                     "type": str,
                     "side": str,
                     "stopPrice": "float",
                     "icebergQty": "float",
                     "time": int,
                     "updateTime":  int,
                     "isWorking": bool
                 }

            Based On Final fetch_orders() results Parsed
        """
        rsl: dict

        params = {
            'type': trd_mod.value
        }

        # process
        trades_data = {}
        try:
            symbol = cls.i_get_position_symbol(_ticket)

            # orders results will get filtered to only closed ones
            trades_data = cls.m_exchange.fetch_closed_orders(symbol=symbol, since=None, limit=500,
                                                             params=params)

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        the_trade = {}
        for trd in trades_data:
            _id = (cls.m_exchange.safe_integer(trd, 'id') if 'id' in trd
                   else cls.m_exchange.safe_integer(trd, 'orderId'))

            if _id == int(_ticket):
                the_trade = trd
                break

        rsl = the_trade

        return rsl

# __
    @classmethod
    def i_get_position_closed_infos_future(cls, _ticket: str) -> dict:
        """ get position closed infos _future
        :param _ticket:
        :return:
                {
                    "symbol": "BTCUSDT",
                    "orderId": 5403233939,
                    "orderListId": -1,
                    "clientOrderId": "x-R4BD3S825e669e75b6c14f69a2c43e",
                    "transactTime": 1617151923742,
                    "price": "0.00000000",
                    "origQty": "0.00050000",
                    "executedQty": "0.00050000",
                    "cummulativeQuoteQty": "29.47081500",
                    "status": "FILLED",
                    "timeInForce": "GTC",
                    "type": "MARKET",
                    "side": "BUY",
                    "fills": [
                        {
                            "price": "58941.63000000",
                            "qty": "0.00050000",
                            "commission": "0.00007050",
                            "commissionAsset": "BNB",
                            "tradeId": 737466631
                        }
                    ]
                }
        """

        """ PARSED AS
        ({
            'info': order,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'timeInForce': timeInForce,
            'postOnly': postOnly,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': None,
            'status': status,
            'fee': None,
            'trades': fills,
        }, market)
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Future.value,
            'newOrderRespType': "FULL"
        }

        # process
        trades_data = {}
        try:
            symbol = cls.i_get_position_symbol(_ticket)

            # orders results will get filtered to only closed ones
            trades_data = cls.m_exchange.fetch_closed_orders(symbol=symbol, since=None, limit=500,
                                                             params=params)

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        the_trade = {}
        for trd in trades_data:
            _id = (cls.m_exchange.safe_integer(trd, 'id') if 'id' in trd
                   else cls.m_exchange.safe_integer(trd, 'orderId'))
            if _id == int(_ticket):
                the_trade = trd
                break

        rsl = the_trade

        return rsl

# __
    @classmethod
    def i_get_positions_by_symbol(cls, _symbol: str) -> dict:
        """ get Position _Symbol
        :param _symbol:
        :return: {}
        """

        # Request Response (fetch my trades)
        # spot trade
        #
        #     [
        #         {
        #             "symbol": "BNBBTC",
        #             "id": 28457,
        #             "orderId": 100234,
        #             "price": "4.00000100",
        #             "qty": "12.00000000",
        #             "commission": "10.10000000",
        #             "commissionAsset": "BNB",
        #             "time": 1499865549590,
        #             "isBuyer": True,
        #             "isMaker": False,
        #             "isBestMatch": True,
        #         }
        #     ]
        #
        # futures trade
        #
        #     [
        #         {
        #             "accountId": 20,
        #             "buyer": False,
        #             "commission": "-0.07819010",
        #             "commissionAsset": "USDT",
        #             "counterPartyId": 653,
        #             "id": 698759,
        #             "maker": False,
        #             "orderId": 25851813,
        #             "price": "7819.01",
        #             "qty": "0.002",
        #             "quoteQty": "0.01563",
        #             "realizedPnl": "-0.91539999",
        #             "side": "SELL",
        #             "symbol": "BTCUSDT",
        #             "time": 1569514978020
        #         }
        #     ]
        #

        rsl: dict

        params = {
            'type': Eainp.EA_Trade_Mode.value
        }

        # process
        rsp = {}
        try:
            # since: now datetime ; limit: toward the past (number to fetch)
            rsp = cls.m_exchange.fetch_my_trades(symbol=_symbol, since=None, limit=500,
                                                 params=params)
            # rsp = cls.m_exchange.filter_by(rsp, 'status', 'opened') # to remove

            # cls.m_exchange.fetch_positions()   #  fetch_position vs fetch_my_trades : who is for on market pos ???

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))
            pprint(rsp)

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_get_position_onmarket_all_buy_future(cls, _symbol: str) -> dict:
        """ get Position onMarket number Of Buy _future
        :param _symbol:
        :return: {}
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Future.value,
            'newOrderRespType': "FULL"
        }

        # Process
        rsp = {}
        try:
            rsp = cls.m_exchange.fetch_open_orders(symbol=_symbol, since=None, limit=500,
                                                   params=params)

            rsp = cls.m_exchange.filter_by(rsp, 'side', 'BUY')   # 'side' work only for future (according to data)

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_get_position_onmarket_numberof_buy_future(cls, _symbol: str) -> int:
        """ get Position onMarket number Of Buy _future
        :param _symbol:
        :return:
        """
        rsl: int

        rsp = cls.i_get_position_onmarket_all_buy_future(_symbol=_symbol)

        rsl = len(rsp)

        return rsl

# __
    @classmethod
    def i_get_position_onmarket_all_sell_future(cls, _symbol: str) -> dict:
        """ get Position onMarket number Of Sell _future
        :param _symbol:
        :return:
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Future.value,
            'newOrderRespType': "FULL"
        }

        # Process
        rsp = {}
        try:
            rsp = cls.m_exchange.fetch_open_orders(symbol=_symbol, since=None, limit=500,
                                                   params=params)

            rsp = cls.m_exchange.filter_by(rsp, 'side', 'SELL')   # 'side' work only for future (according to data)

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_get_position_onmarket_numberof_sell_future(cls, _symbol: str) -> int:
        """ get Position onMarket number Of Sell _future
        :param _symbol:
        :return:
        """
        rsl: int  # = 0

        rsp = cls.i_get_position_onmarket_all_sell_future(_symbol=_symbol)

        rsl = len(rsp)

        return rsl
# ..................    ...................

# ..................    ...................
# __
    @classmethod
    def i_get_position_type(cls, _ticket: str, trd_mod: Eaenum.TradeMode) -> Eaenum.PosType:
        """ get Position Type
        :param _ticket:
        :param trd_mod:
        :return: PosTyp
        """
        rsl: Eaenum.PosType = Eaenum.PosType.OpNo

        # __spot margin
        if Util.is_trade_mode_spot_or_margin(trd_mod):
            rsp = cls.i_get_position_closed_infos_spotmargin(_ticket=_ticket, trd_mod=trd_mod)

            if Util.is_true(rsp['isBuyer']):
                rsl = Eaenum.PosType.OpBuy
            else:
                rsl = Eaenum.PosType.OpSell

        # __future
        elif Util.is_trade_mode_future(trd_mod):
            rsp = cls.i_get_position_infos_future(_ticket=_ticket)

            rsl = From.from_std_side_to_postyp(rsp['side'])

        return rsl

# __
    @classmethod
    def i_get_position_opentime(cls, _ticket: str, trd_mod: Eaenum.TradeMode) -> dt.datetime:
        """ get Position _OpenTime
        :param _ticket:
        :param trd_mod:
        :return: datetime
        """
        rsl: dt.datetime  # = Duration.get_null_datetime()

        rsp = cls.i_get_position_infos(_ticket=_ticket, trd_mod=trd_mod)

        tmst = cls.m_exchange.safe_integer(rsp, 'time')

        rsl = dt.datetime.fromtimestamp(t=tmst)

        return rsl

# __
    @classmethod
    def i_get_position_lot(cls, _ticket: str, trd_mod: Eaenum.TradeMode) -> float:
        """ get Position Lot
        :param _ticket:
        :param trd_mod:
        :return: float
        """
        rsl: float  # = 0

        lot: float = 0

        if Util.is_trade_mode_spot_or_margin(trd_mod):
            rsp = cls.i_get_position_closed_infos_spotmargin(_ticket=_ticket, trd_mod=trd_mod)

            lot = float(rsp['qty'])

        elif Util.is_trade_mode_future(trd_mod):
            rsp = cls.i_get_position_infos_future(_ticket=_ticket)

            lot = cls.m_exchange.safe_float(rsp, 'qty')

        rsl = lot

        return rsl

# __
    @classmethod
    def i_get_position_openprice(cls, _ticket: str, trd_mod: Eaenum.TradeMode) -> float:
        """ get Position Open Price
        :param _ticket:
        :param trd_mod:
        :return: float
        """
        rsl: float  # = 0

        rsp = cls.i_get_position_infos(_ticket=_ticket, trd_mod=trd_mod)

        rsl = cls.m_exchange.safe_float(rsp, 'price')

        return rsl

# __
    @classmethod
    def i_get_position_dealprofit_future(cls, _ticket: str) -> float:
        """ get Position Deal Profit _future
        :param _ticket:
        :return: float
        """
        rsl: float  # = 0

        rsp = cls.i_get_position_infos_future(_ticket=_ticket)

        rsl = cls.m_exchange.safe_float(rsp, 'realizedPnl')

        return rsl

# __
    @classmethod
    def i_get_position_closedtime_future(cls, _ticket: str) -> dt.datetime:
        """ get Position ClosedTime _future
        :param _ticket:
        :return:
        """
        rsl: dt.datetime  # = Duration.get_null_datetime()

        rsp = cls.i_get_position_closed_infos_future(_ticket=_ticket)

        tmst = cls.m_exchange.safe_integer(rsp, 'transactTime')       # transactTime contain close time ???

        rsl = dt.datetime.fromtimestamp(t=tmst)

        return rsl

# __
    @classmethod
    def i_get_position_closedprice_future(cls, _ticket: str) -> float:
        """ get Position ClosedPrice _future
        :param _ticket:
        :return:
        """
        rsl: float  # = 0

        rsp = cls.i_get_position_closed_infos_future(_ticket=_ticket)

        # Enter inside orders filling infos
        closedInf = rsp['trades'][0]                    # first list infos

        rsl = cls.m_exchange.safe_float(closedInf, 'price')

        return rsl

# __
    @classmethod
    def i_get_position_closed_commission_future(cls, _ticket: str) -> float:
        """ get Position _Closed Commission _future
        :param _ticket:
        :return: float
        """
        rsl: float  # = 0

        rsp = cls.i_get_position_closed_infos_future(_ticket=_ticket)

        # Enter inside orders filling infos
        closedInf = rsp['trades'][0]                                # first list infos

        rsl = cls.m_exchange.safe_float(closedInf, 'commission')

        return rsl

# __
    @classmethod
    def i_get_position_closed_profit_future(cls, _ticket: str) -> float:
        """ get Position _Closed Profit _future
        :param _ticket:
        :return:
        """
        rsl: float  # = 0

        rsl = cls.i_get_position_dealprofit_future(_ticket=_ticket)

        return rsl

# __
    @classmethod
    def i_get_position_closed_symbol_future(cls, _ticket: str) -> str:
        """ get Position _Symbol
        :param _ticket:
        :return:
        """
        rsl: str  # = ""

        rsp = cls.i_get_position_closed_infos_future(_ticket=_ticket)

        # Enter inside orders filling infos
        closedInf = rsp['trades'][0]  # first list infos

        rsl = cls.m_exchange.safe_float(closedInf, 'symbol')

        return rsl
# ................    .................

# ................    ...............
# __
    @classmethod
    def i_get_position_symbol(cls, _ticket: str) -> str:
        """ get Position _Symbol
        :param _ticket:
        :return:
        """
        rsl: str  # = ""

        # trd_mod: Eainp.EA_Trade_Mode

        # don't exist recovering by _ticket

        symbol = Pair.get_symbol()

        rsl = symbol

        return rsl

# __
    @classmethod
    def i_get_position_comment(cls, _ticket: str) -> str:
        """ get Position _Comment
        :param _ticket:
        :return:
        """
        rsl: str = ""

        # process
        # nothing to get from now from binance

        return rsl

# __
    @classmethod
    def i_get_position_tp_price(cls, _ticket: str) -> float:
        """ get Position _Tp Price
        :param _ticket:
        :return:
        """
        rsl: float = 0

        # process

        return rsl

# __
    @classmethod
    def i_get_position_sl_price(cls, _ticket: str) -> float:
        """ get Position _Sl Price
        :param _ticket:
        :return:
        """
        rsl: float = 0

        # process

        return rsl

# .................     ...................

# .................     ...................
# __
    @classmethod
    def i_get_open_orders_all_count(cls, _symbol: str, trd_mod: Eaenum.TradeMode) -> list:
        """ get Waiting Orders _AllCount
        :param _symbol:
        :param trd_mod:
        :return: []
        """
        rsl: list

        params = {
            'type': trd_mod.value,
            'newOrderRespType': "FULL"
        }

        # Process
        rsp = []
        try:
            rsp = cls.m_exchange.fetch_open_orders(symbol=_symbol, since=None, limit=500,
                                                   params=params)

            # rsp = cls.m_exchange.filter_by(rsp, 'status', 'opened')  # filtering  --don't need

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_get_open_orders_all_count_(cls, _symbol: str, trd_mod: Eaenum.TradeMode) -> int:
        """ get Open Orders _AllCount
        :param _symbol:
        :param trd_mod:
        :return: int
        """
        rsl: int  # = 0

        rsp = cls.i_get_open_orders_all_count(_symbol=_symbol, trd_mod=trd_mod)

        rsl = len(rsp)

        return rsl

# __
    @classmethod
    def i_get_waiting_orders_onmarket_all_count(cls, _symbol: str, trd_mod: Eaenum.TradeMode) -> int:
        """ get Waiting Orders on Market _AllCount
        :param _symbol:
        :param trd_mod:
        :return: int
        """
        rsl: int  # = 0

        rsl = cls.i_get_open_orders_all_count_(_symbol=_symbol, trd_mod=trd_mod)

        return rsl

# __
    @classmethod
    def i_is_waiting_orders_onmarket(cls, _symbol: str, trd_mod: Eaenum.TradeMode) -> bool:
        """ is Waiting Orders onMarket ?
        :param _symbol:
        :param trd_mod:
        :return: bool
        """
        rsl: bool = False

        # Process
        wait_ords_count = cls.i_get_waiting_orders_onmarket_all_count(_symbol=_symbol, trd_mod=trd_mod)

        if wait_ords_count > 0:
            rsl = True

        return rsl

# __
    @classmethod
    def i_cancel_position_or_order(cls, _ticket: str) -> dict:
        """ Cancel Position or Order
        :param _ticket:
        :return: {}
        """
        rsl: dict

        params = {
            'type': Pair.get_trading_mode().value,
        }

        # process
        rsp = {}
        try:
            rsp = cls.m_exchange.cancel_order(id=_ticket, symbol=Pair.get_symbol(),
                                              params=params)  # request result is returned as Parsed
        except Exception as e:
            print('Error: Cancel Order Request Failed')
            print(type(e).__name__, str(e))

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_cancel_position_or_order_(cls, _ticket: str) -> bool:
        """ Cancel Position or Order
        :param _ticket:
        :return: bool
        """
        rsl: bool = False

        rsp = cls.i_cancel_position_or_order(_ticket=_ticket)

        # rsl =

        return rsl


# __
    @classmethod
    def i_close_waiting_order(cls, _ticket: str) -> bool:
        """ close waiting order
        :param _ticket:
        :return: bool
        """
        rsl: bool = False

        if Util.is_null_ticket(_ticket):
            return rsl

        rsp = cls.i_cancel_position_or_order(_ticket=_ticket)

        # recovering data inside results
        id_1 = cls.m_exchange.safe_string(rsp, 'id')
        id_2 = cls.m_exchange.safe_string(rsp, 'clientOrderId')

        if not Util.is_null_string(id_1) or not Util.is_null_string(id_2):
            if id_1 is _ticket or id_2 is _ticket:
                rsl = True

        return rsl

# __
    @classmethod
    def i_cancel_positions_or_orders(cls, _symbol: str) -> list or dict:
        """ Cancel Position or Order
        :param _symbol:
        :return:
        """
        rsl: list or dict = []

        params = {
            'type': Pair.get_trading_mode().value,
        }

        # process
        try:
            rsp = cls.m_exchange.cancel_all_orders(symbol=_symbol,
                                                   params=params)
            rsl = rsp

        except Exception as e:
            print('Error: Cancel Order Request Failed')
            print(type(e).__name__, str(e))

        return rsl

# __
    @classmethod
    def i_close_waiting_orders_all(cls, _symbol: str) -> bool:
        """ close waiting orders All
        :param _symbol:
        :return:
        """
        rsl: bool = False

        params = {
            'type': Pair.get_trading_mode().value,
        }

        # process
        rsp: list
        try:
            rsp = cls.m_exchange.cancel_all_orders(symbol=_symbol,
                                                   params=params)

        except Exception as e:
            print('Error: Cancel Order Request Failed')
            print(type(e).__name__, str(e))
            return rsl

        # treat rsp
        if isinstance(rsp, list):      # parsed dict list returned request results
            if len(rsp) > 1:           # the proof that many orders have been closed
                rsl = True
        elif isinstance(rsp, dict):    # not parsed dict returned request results
            id_1 = cls.m_exchange.safe_string(rsp, 'orderId')
            id_2 = cls.m_exchange.safe_string(rsp, 'clientOrderId')

            if not Util.is_null_string(id_1) or not Util.is_null_string(id_2):
                rsl = True
        # __

        return rsl
# ................................

# ................................ Resume Place Order or Close
    @classmethod
    def i_place_position(cls, pos_type: Eaenum.PosType, trd_mod: Eaenum.TradeMode,
                         _price: float, _lot: float,
                         _sl: float = 0, _tp: float = 0,
                         is_isolated: bool = True) -> dict:
        """ place position
        :param pos_type:
        :param trd_mod:
        :param _price:
        :param _lot:
        :param _sl:
        :param _tp:
        :param is_isolated:
        :return: dict
        """
        rsl: dict

        rsp = {}

        # Margin Mode
        if Util.is_trade_mode_margin(trd_mod):

            if Util.is_position_type_buy(pos_type):
                rsp = cls.i_open_position_buy_margin(_qty=_lot,
                                                     _symbol=Eainp.EA_Trade_Pair,
                                                     open_price=_price,
                                                     is_isolated=is_isolated,
                                                     )

            elif Util.is_position_type_sell(pos_type):
                rsp = cls.i_open_position_sell_margin(_qty=_lot,
                                                      _symbol=Eainp.EA_Trade_Pair,
                                                      open_price=_price,
                                                      is_isolated=is_isolated,
                                                      )

        # Spot Mode
        elif Util.is_trade_mode_spot(trd_mod):

            if Util.is_position_type_buy(pos_type):
                rsp = cls.i_open_position_buy_spot(_qty=_lot,
                                                   _symbol=Eainp.EA_Trade_Pair,
                                                   open_price=_price,
                                                   )

            elif Util.is_position_type_sell(pos_type):
                rsp = cls.i_open_position_sell_spot(_qty=_lot,
                                                    _symbol=Eainp.EA_Trade_Pair,
                                                    open_price=_price,
                                                    )

        # Future Mode
        elif Util.is_trade_mode_future(trd_mod):
            if Util.is_position_type_buy(pos_type):
                rsp = cls.i_open_position_buy_future(_qty=_lot,
                                                     _symbol=Eainp.EA_Trade_Pair,
                                                     open_price=_price,
                                                     )
                # ... tp sl ?
                # ...

            elif Util.is_position_type_sell(pos_type):
                rsp = cls.i_open_position_sell_future(_qty=_lot,
                                                      _symbol=Eainp.EA_Trade_Pair,
                                                      open_price=_price,
                                                      )
                # ... tp sl ?
                # ...

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_place_position_(cls, pos_type: Eaenum.PosType, trd_mod: Eaenum.TradeMode,
                          _price: float, _lot: float,
                          _sl: float = 0, _tp: float = 0,
                          is_isolated: bool = True) -> bool:
        """ place position
        :param pos_type:
        :param trd_mod:
        :param _price:
        :param _lot:
        :param _sl:
        :param _tp:
        :param is_isolated:
        :return: bool
        """
        rsl: bool

        rsp = cls.i_place_position(pos_type=pos_type, trd_mod=trd_mod,
                                   _price=_price, _lot=_lot,
                                   _sl=_sl, _tp=_tp,
                                   is_isolated=is_isolated)

        # rsl =

        return rsl

    # __
    @classmethod
    def i_close_position_spotmargin(cls, open_postyp: Eaenum.PosType, trd_mod: Eaenum.TradeMode, _symbol: str,
                                    _price: float, _lot: float, _sl: float = 0, _tp: float = 0,
                                    is_isolated: bool = True) -> dict:
        """ close Position Spot or Margin
        :param open_postyp:
        :param trd_mod:
        :param _symbol:
        :param _price:
        :param _lot:
        :param _sl:
        :param _tp:
        :param is_isolated:
        :return: {}
        """
        rsl = {}

        if Util.is_trade_mode_spot(trd_mod):          # Spot Mode
            rsl = cls.i_close_position_spot(open_postyp=open_postyp,
                                            _qty=_lot,
                                            _symbol=_symbol,
                                            close_price=_price,
                                            )

        elif Util.is_trade_mode_margin(trd_mod):      # Margin Mode
            rsl = cls.i_close_position_margin(open_postyp=open_postyp,
                                              _qty=_lot,
                                              _symbol=_symbol,
                                              close_price=_price,
                                              is_isolated=is_isolated,
                                              )
        return rsl
# ..................................

# .................................. SPOT specific
    @classmethod
    def i_open_position_spot(cls, pos_type: Eaenum.PosType,
                             _qty: float, _symbol: str, open_price: float = None) -> dict:
        """ open Position Spot
        :param pos_type:
        :param _qty:
        :param _symbol:
        :param open_price:
        :return: {}
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Spot.value.lower(),
            'timeInForce': Eainp.EA_TimeInForce.value,
        }

        # when close price not defined use current Tick Price
        if open_price is 0:
            open_price = Candle.get_cdl_current_tickprice()  # Tick Price

        _side = From.from_postyp_to_std_side(pos_type)  # std side

        # Process
        rsp = {}
        error_occured = False
        try:
            rsp = cls.m_exchange.create_market_order(symbol=_symbol, side=_side, amount=_qty, price=open_price,
                                                     params=params)
        except cx.InsufficientFunds as e:
            print('Error: Order Failed, not Enough Money')
            print(type(e).__name__, str(e))
            error_occured = True
        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))
            error_occured = True

        # await cx.binanceusdm.close()

        rsl = rsp

        if not error_occured:
            cls.i_set_position_very_last_filled_onmarket_infos(rsl)

        return rsl

# __
    @classmethod
    def i_open_position_sell_spot(cls, _qty: float, _symbol: str, open_price: float = None) -> dict:
        """ open Position Spot Sell
        :param _qty:
        :param _symbol:
        :param open_price:
        :return: {}
        """
        rsl: dict

        rsl = cls.i_open_position_spot(pos_type=Eaenum.PosType.OpSell,
                                       _qty=_qty, _symbol=_symbol,
                                       open_price=open_price)

        return rsl

# __
    @classmethod
    def i_open_position_buy_spot(cls, _qty: float, _symbol: str, open_price: float = None) -> dict:
        """ open Position Spot Buy
        :param _qty:
        :param _symbol:
        :param open_price:
        :return:
        """
        rsl: dict

        rsl = cls.i_open_position_spot(pos_type=Eaenum.PosType.OpBuy,
                                       _qty=_qty, _symbol=_symbol,
                                       open_price=open_price)

        return rsl

# __
    @classmethod
    def i_close_position_spot(cls, _qty: float, open_postyp: Eaenum.PosType, _symbol: str,
                              close_price: float = None) -> dict:
        """ close Position _spot
        :param _qty:
        :param open_postyp:
        :param _symbol:
        :param close_price:
        :return: {}
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Spot.value.lower(),
            'timeInForce': Eainp.EA_TimeInForce
        }

        #   when close price not defined use current Tick Price
        if close_price is 0:  # needed ?
            close_price = Candle.get_cdl_current_tickprice()  # Tick Price

        #
        _closeTyp = Eaenum.PosType.getOpposite_PositionType(open_postyp)  # getting Open Opposite Order
        _side = From.from_postyp_to_std_side(_closeTyp)  # closing order std Side

        # Process
        rsp = {}
        error_occured = False
        try:
            rsp = cls.m_exchange.create_market_order(symbol=_symbol, side=_side, amount=_qty, price=close_price,
                                                     params=params)
        except cx.InsufficientFunds as e:
            print('Error: Close Order Failed, not Enough Money')
            print(type(e).__name__, str(e))
            error_occured = True
        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))
            error_occured = True

        # await cx.binanceusdm.close()

        rsl = rsp

        if not error_occured:
            cls.i_set_position_very_last_filled_onmarket_infos(rsl)

        return rsl
# ...............................

# ............................... MARGIN specific

    @classmethod
    def i_open_position_margin(cls, pos_type: Eaenum.PosType, _qty: float, _symbol: str, open_price: float = None,
                               is_isolated=True) -> dict:
        """ open Position Margin Sell
        :param pos_type:
        :param _qty:
        :param _symbol:
        :param open_price:
        :param is_isolated:
        :return: {}
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Margin.value.lower(),
            'isolated': From.from_bool_to_string(is_isolated),
            'timeInForce': Eainp.EA_TimeInForce.value,
        }

        _side = From.from_postyp_to_std_side(pos_type)

        # Process
        rsp = {}
        error_occured = False
        try:
            rsp = cls.m_exchange.create_market_order(symbol=_symbol, side=_side, amount=_qty, price=open_price,
                                                     params=params)
        except cx.InsufficientFunds as e:
            print('Error: Order Failed, not Enough Money')
            print(type(e).__name__, str(e))
            error_occured = True
        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))
            error_occured = True

        # await cx.binanceusdm.close()

        rsl = rsp

        if not error_occured:
            cls.i_set_position_very_last_filled_onmarket_infos(rsl)

        return rsl

# __
    @classmethod
    def i_open_position_sell_margin(cls, _qty: float, _symbol: str, open_price: float = None,
                                    is_isolated=True) -> dict:
        """ open Position Margin Sell
        :param _qty:
        :param _symbol:
        :param open_price:
        :param is_isolated:
        :return: {}
        """

        rsl = cls.i_open_position_margin(pos_type=Eaenum.PosType.OpSell,
                                         _qty=_qty, _symbol=_symbol, open_price=open_price,
                                         is_isolated=is_isolated)

        return rsl

# __
    @classmethod
    def i_open_position_buy_margin(cls, _qty: float, _symbol: str, open_price: float = None,
                                   is_isolated=True) -> dict:
        """ open Position Margin Buy
        :param _qty:
        :param _symbol:
        :param open_price:
        :param is_isolated:
        :return: {}
        """

        rsl = cls.i_open_position_margin(pos_type=Eaenum.PosType.OpBuy,
                                         _qty=_qty, _symbol=_symbol, open_price=open_price,
                                         is_isolated=is_isolated)

        return rsl

# __
    @classmethod
    def i_open_position_oco_order_margin(cls, _qty: float, open_postyp: Eaenum.PosType, _symbol: str,
                                         open_price: float = None, is_isolated=True) -> dict:
        """ open Position Margin oco order
        :param _qty:
        :param open_postyp:
        :param _symbol:
        :param open_price:
        :param is_isolated:
        :return: {}
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Margin.value.lower(),
            'isIsolated': From.from_bool_to_string(is_isolated),
            'timeInForce': Eainp.EA_TimeInForce.value,
        }

        _side = From.from_postyp_to_std_side(open_postyp)

        # when close price not defined use current Tick Price
        if open_price is 0:
            open_price = Candle.get_cdl_current_tickprice()     # Tick Price

        # How To Specify OCO ???
        rsp = {}
        error_occured = False
        try:
            rsp = cls.m_exchange.create_order(symbol=_symbol, side=_side, type="MARGIN",
                                              amount=_qty, price=open_price,
                                              params=params)
        except cx.InsufficientFunds as e:
            print('Error: OCO Order Request Failed, not Enough Money!')
            print(type(e).__name__, str(e))
            error_occured = True
        except Exception as e:
            print('Error: OCO Order Request Failed')
            print(type(e).__name__, str(e))
            error_occured = True

        # await cx.binanceusdm.close()

        rsl = rsp

        if not error_occured:
            cls.i_set_position_very_last_filled_onmarket_infos(rsl)

        return rsl

# __
    @classmethod
    def i_close_position_margin(cls, _qty: float, open_postyp: Eaenum.PosType, _symbol: str,
                                close_price: float = None, is_isolated=True) -> dict:
        """ close Position Margin
        :param _qty:
        :param open_postyp:
        :param _symbol:
        :param close_price:
        :param is_isolated:
        :return:
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Margin.value.lower(),
            'isolated': From.from_bool_to_string(is_isolated),
            'timeInForce': Eainp.EA_TimeInForce.value,
        }

        _closeTyp = Eaenum.PosType.getOpposite_PositionType(open_postyp)  # getting Open Opposite Order
        _side = From.from_postyp_to_std_side(_closeTyp)  # closing order std Side

        # when close price not defined use current Tick Price
        if close_price is 0:
            close_price = Candle.get_cdl_current_tickprice()        # Tick Price

        # process
        rsp = {}
        error_occured = False
        try:
            rsp = cls.m_exchange.create_market_order(symbol=_symbol, side=_side, amount=_qty, price=close_price,
                                                     params=params)
        except cx.InsufficientFunds as e:
            print('Error: Order request Failed, not Enough Money')
            print(type(e).__name__, str(e))
            error_occured = True
        except Exception as e:
            print('Error: Order Request Failed')
            print(type(e).__name__, str(e))
            error_occured = True

        # await cx.binanceusdm.close()

        rsl = rsp

        if not error_occured:
            cls.i_set_position_very_last_filled_onmarket_infos(rsl)

        return rsl
# ..............................

# .............................. FUTURE specific
    @classmethod
    def i_open_position_future(cls, pos_type: Eaenum.PosType,
                               _qty: float, _symbol: str,
                               open_price: float = None) -> dict:
        """ open Position Sell _Future
        :param pos_type:
        :param _qty:
        :param _symbol:
        :param open_price:
        :return: {}
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Future.value.lower(),
            'timeInForce': Eainp.EA_TimeInForce.value
        }

        _side = From.from_postyp_to_std_side(pos_type)

        # process
        rsp = {}
        error_occured = False
        try:
            rsp = cls.m_exchange.create_market_order(symbol=_symbol, side=_side, amount=_qty, price=open_price,
                                                     params=params)
        except cx.InsufficientFunds as e:
            print('Error: Open Sell Order Failed, not Enough Money')
            print(type(e).__name__, str(e))
            error_occured = True
        except Exception as e:
            print('Error: Open Sell Order Failed')
            print(type(e).__name__, str(e))
            error_occured = True

        # await cx.binanceusdm.close()

        rsl = rsp

        if not error_occured:
            cls.i_set_position_very_last_filled_onmarket_infos(rsl)

        return rsl

# __
    @classmethod
    def i_open_position_sell_future(cls, _qty: float, _symbol: str, open_price: float = None) -> dict:
        """ open Position Sell _Future
        :param _qty:
        :param _symbol:
        :param open_price:
        :return: {}
        """
        rsl: dict

        rsl = cls.i_open_position_future(pos_type=Eaenum.PosType.OpSell,
                                         _qty=_qty, _symbol=_symbol,
                                         open_price=open_price)

        return rsl

# __
    @classmethod
    def i_open_position_buy_future(cls, _qty: float, _symbol: str, open_price: float = None) -> dict:
        """ open Position Buy Future
        :param _qty:
        :param _symbol:
        :param open_price:
        :return:
        """
        rsl: dict

        rsl = cls.i_open_position_future(pos_type=Eaenum.PosType.OpBuy,
                                         _qty=_qty, _symbol=_symbol,
                                         open_price=open_price)

        return rsl

# __
    @classmethod
    def i_open_position_buy_future_(cls, _qty: float, _symbol: str,
                                    open_price: float = None,
                                    _sl: float = 0, _tp: float = 0) -> dict:
        """ open Position Buy _Future
        :param _qty:
        :param _symbol:
        :param open_price:
        :param _sl:
        :param _tp:
        :return: {}
        """
        rsl: dict = {}

        # rsl =

        return rsl

# __
    @classmethod
    def i_open_position_sell_future_(cls, _qty: float, _symbol: str,
                                     open_price: float = None,
                                     _sl: float = 0, _tp: float = 0) -> dict:
        """ open Position Sell _Future
        :param _qty:
        :param _symbol:
        :param open_price:
        :param _sl:
        :param _tp:
        :return: {}
        """
        rsl: dict = {}

        # rsl =

        return rsl

# __
    @classmethod
    def i_close_position_future(cls, _ticket: str) -> dict:
        """ close Position future
        :param _ticket:
        :return:
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Future.value.lower(),
            'timeInForce': Eainp.EA_TimeInForce,
        }

        _symbol = Pair.get_symbol()

        # process
        rsp = {}
        try:
            rsp = cls.m_exchange.cancel_order(id=_ticket, symbol=_symbol,
                                              params=params)

        except cx.InsufficientFunds as e:
            print('Error: Order Failed, not Enough Money')
            print(type(e).__name__, str(e))
        except Exception as e:
            print('Error: Open Order Failed')
            print(type(e).__name__, str(e))

        # await cx.binanceusdm.close()

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_place_stoploss_future(cls, _ticket, sl_price: float) -> dict:
        """ place Stop Loss _Future
        :param _ticket:
        :param sl_price:
        :return:
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Future.value.lower(),
            'timeInForce': Eainp.EA_TimeInForce,
        }

        args = None  # ???

        _symbol = Pair.get_symbol()

        needToReverse = False

        if Util.is_false(Eainp.EA_Exc_Enable_RateLimit):
            Eainp.EA_Exc_Enable_RateLimit = True
            needToReverse = True

        cls.m_exchange.enableRateLimit = Eainp.EA_Exc_Enable_RateLimit  # edit order need Enable rate limit

        # process
        rsp = {}
        try:
            rsp = cls.m_exchange.edit_order(id=_ticket, symbol=_symbol,
                                            args=args)      # params ???, sl_price ??? --CODE--
        except Exception as e:
            print('Error: Order Failed')
            print(type(e).__name__, str(e))

        if needToReverse:
            Eainp.EA_Exc_Enable_RateLimit = False

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_place_takeprofit_future(cls, _ticket, tp_price: float) -> dict:
        """ place Take Profit _Future
        :param _ticket:
        :param tp_price:
        :return: {}
        """
        rsl: dict

        params = {
            'type': Eaenum.TradeMode.Future.value.lower(),
            'timeInForce': Eainp.EA_TimeInForce,
        }

        # args = [Pair.get_symbol(), type, side, amount, price=None, params={}]     # ???

        # args = Pair.get_symbol(), Pair.get_trading_mode(), Eaenum.PosType.OpBuy, 0.8, None, params

        args = None  # ???

        _symbol = Pair.get_symbol()

        needToReverse = False

        if Util.is_false(Eainp.EA_Exc_Enable_RateLimit):
            Eainp.EA_Exc_Enable_RateLimit = True
            needToReverse = True

        cls.m_exchange.enableRateLimit = Eainp.EA_Exc_Enable_RateLimit  # edit order need Enable rate limit

        # process
        rsp = {}
        try:                   # edit order delete that order before is right ???
            rsp = cls.m_exchange.edit_order(id=_ticket, symbol=_symbol,
                                            args=args)      # params ???, tp_price ???  --CODE--

        except Exception as e:
            print('Error: Request Failed')
            print(type(e).__name__, str(e))

        if needToReverse:
            Eainp.EA_Exc_Enable_RateLimit = False

        rsl = rsp

        return rsl

# __
    @classmethod
    def i_place_takeprofit_future_(cls, _ticket, tp_price: float) -> bool:
        """ place Take Profit _Future
        :param _ticket:
        :param tp_price:
        :return: bool
        """
        rsl: bool = False

        # rsl

        return rsl


# __
    @classmethod
    def i_place_stoploss_future_(cls, _ticket, sl_price: float) -> bool:
        """ place Stop Loss _Future
        :param _ticket:
        :param sl_price:
        :return: bool
        """
        rsl: bool = False

        # rsl

        return rsl
# .................................

# __
"""
    reduce_margin(self, symbol, amount, params={})

    add_margin(self, symbol, amount, params={})
    
    handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody)
    
    set_position_mode(self, hedged, symbol=None, params={})
    
    set_margin_mode(self, marginType, symbol=None, params={}):
    
    futures_transfer(self, code, amount, type, params={})
    
    fetch_order_status(self, id, symbol=None, params={})
    
    cx.binance.last_json_response

"""

#  --- END CLASS BINANCE-INTERFACE ---  #
