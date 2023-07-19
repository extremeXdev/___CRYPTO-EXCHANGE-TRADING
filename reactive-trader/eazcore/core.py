
###########################################
#         REACTIVE TRADER EACORE          #
###########################################

# :::::::
# LEVEL 7
# :::::::

# Imports here
from eazcore.lib import *


class EA:

    def __init__(self):
        pass

    @staticmethod
    def on_init():
        """ On Init
        :return:
        """

        # __ Init Saver vars
        # ......... last Bar
        Easav.EALastDeviationBar_Saved = Candle.get_null_candle()
        Easav.EALastBar_Saved = Candle.get_null_candle()
        # .........

        # ......... last Trade
        Easav.EALastTradeLot_Saved = 0
        Easav.EALastTradeLot_RightCoin_Saved = 0
        Easav.EALastTradeLot_LeftCoin_Saved = 0
        # .........

        # ......... saved capital
        Easav.EALast_valideCapital_Saved = 0
        Easav.EALast_valideCapital_Right_Saved = 0
        Easav.EALast_valideCapital_Left_Saved = 0

        # ......... saved prices
        Easav.EALastTickPrice_Saved = 0
        Easav.EARightPriceTo_OpenPos_BtnBuy_Saved = 0
        Easav.EARightPriceTo_OpenPos_BtnSell_Saved = 0
        # .........

        # ......... saved datetime

        # .........

        # __

        # __ Changing Leverage
        if Pair.is_willing_to_change_leverage():
            if Util.is_trade_mode_main_margin_or_future():
                MarketBridge.set_leverage(lever=Eainp.EA_Leverage)

            elif Util.is_trade_mode_main_spot():    # -- ??? is leverage Supported on Spot Market ???
                pass
        # __

    # :::::::

    @staticmethod
    def on_deinit():
        """ On DeInit
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_tick_event():
        """ On Tick Event
        :return:
        """
        # new Reactive Trade process is here
        if not CFDManager.is_cfdpositions_onmarket():     # what of future ???
            EA.trade_process()

    # :::::::

# __
    @staticmethod
    def on_custom_event(s_param: str = None,
                        f_param: float = None,
                        i_param: int = None,
                        l_param: list = None,
                        d_param: dict = None):  # Don't Need Yet
        """ On Custom Event
        :param s_param:
        :param f_param:
        :param i_param:
        :param l_param:
        :param d_param:

        :return:
        """
        # Act according to submitted parameters
        # ...
        pass

    # :::::::

# __
    @staticmethod
    def on_timer_event():
        """ On Timer Event
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_tester_init_event():  # Not Needed
        """ On Tester Init Event
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_tester_end_event():  # Not Needed
        """ On Tester end Event
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_newbar_event():   # Not Used Yet in Our Algorithm
        """ On New Bar Event
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_newday_event():   # Not Used Yet in Our Algorithm
        """ On New Day Event
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_new_week_event():   # Not Used Yet in Our Algorithm
        """ On New Week Event
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_new_month_event():   # Not Used Yet in Our Algorithm
        """ On New Month Event
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_new_year_event():   # Not Used Yet in Our Algorithm
        """ On New Year Event
        :return:
        """
        pass

    # :::::::

# __
    @staticmethod
    def on_zero_position_event():              # VERIFY
        """ On Zero Position Event
        :return:
        """
        # Update Calculated MMG Lot now
        MMG.update_mmg_lot()

        # Replenish Opposite Coin Balance when needed
        if Pair.is_minor_balance_need_to_be_replenished():
            minor_bl_coin = Eagbl.EAPair.getMinorBalance_Coin()
            greater_bl_coin = Eagbl.EAPair.getOppositeCoin(_pivotCoin=minor_bl_coin)

            _replenishAmount = Eagbl.EAPair.getCoinBalance(_coin=greater_bl_coin) * (10/100)  # specify replenish amount
            Eagbl.EAPair.replenishCoin(_coin=minor_bl_coin, _amount=_replenishAmount)

    # :::::::

# __
    @staticmethod
    def on_running_trade_event():
        """ On Running Trade Event
        :return:
        """
        # Close Ancient Position process is here

        # get cfd Open Position
        _PosList = Eagbl.cfdManaja.getCFDPosOpen_List()

        for _Pos in _PosList:

            # if position isn't closed
            if not _Pos.isPosClosed():

                # close that position by opposite Order
                result = Position.close_position_opened(_Pos.getPosTicket_Opening())

                if Util.is_true(result):

                    # recover last trade Filled infos
                    # get ticket
                    _cPosTicket = MarketPosition.get_position_verylast_filled_onmarket_ticket()

                    # get info
                    _cPos = Position(_ticket=_cPosTicket, pos_filltyp=Eaenum.PosFillTyp.ClosePos)

                    # complete infos to existing opened pos
                    _Pos.addPosClosedInfo_toCFDPos(_cPos)

                    # complete infos to existing cfd Partial Position
                    _posInd = Util.get_position_inside_list_index(_Pos, _PosList)

                    Eagbl.cfdManaja.toggleClosedPositionToHistory(_posInd)
    # :::::::

# __
    @staticmethod
    def trade_process():
        """ Trade Process
        :return:
        """
        # compare three former bar similarity
        if Bar.isbar_three_former_bars_similar():      # is three former bar similar

            # recover current candle
            _lastCdl = Candle.get_cdl_latest_candle()
            c_bar = Bar(_lastCdl)

            # get tick Price
            _tickPrice = Candle.get_cdl_current_tickprice()

            # check if Profit margin exist between current bar High and Low
            if c_bar.isbar_profit_margin_between_high_and_low():

                # check if Price Upper
                if Bar.is_current_price_upper_price():
                    if Util.is_true(Eainp.EA_Trade_SideLeft):       # when Trade with Left Coin balance active
                        Pair.coin_first_trader()       # Let's goto Left trade

                # check if Price Bottom
                elif Bar.is_current_price_bottom_price():
                    if Util.is_true(Eainp.EA_Trade_SideRight):        # when Trade with Right Coin balance active
                        Pair.coin_second_trader()      # Let's goto Right trade

    # :::::::

# __
    @staticmethod
    def reactive_trader(pos_typ: Eaenum.PosType):
        """ Reactive Trader
        :param pos_typ:
        :return:
        """
        if Util.is_trade_mode_spot(Eainp.EA_Trade_Mode):
            EA.reactive_spot_trader(pos_typ)

        elif Util.is_trade_mode_margin(Eainp.EA_Trade_Mode):
            EA.reactive_margin_trader(pos_typ)

        elif Util.is_trade_mode_future(Eainp.EA_Trade_Mode):
            EA.reactive_future_trader(pos_typ)

    # :::::::

# __
    @staticmethod
    def reactive_spot_trader(pos_typ: Eaenum.PosType):

        # position Buy
        if Util.is_position_type_buy(pos_typ):

            _entryPrice = Bar.get_market_bottom_price()

            _sl = From.from_entryprice_and_pips_to_sl_pricetarget(entry_price=_entryPrice,
                                                                  sl_pips=Eainp.EA_SL_SecurityPips,
                                                                  pos_typ=pos_typ)
            _tp = From.from_entryprice_and_pips_to_tp_pricetarget(entry_price=_entryPrice,
                                                                  tp_pips=Eainp.EA_TP_TargetPips,
                                                                  pos_typ=pos_typ)

            # recovering pivot coin according to position type
            # _coinsideTyp = From.from_open_ordertyp_to_coinsidetyp(open_postyp=pos_typ)
            # _pivotcoin = From.from_coinsidetyp_to_coin(open_coinside_typ=_coinsideTyp)

            _amount = Saver.get_last_trade_lot_leftcoin_saved()                     # LeftCoin Is Capital

            # pivot_coin=_pivotcoin (no longer used inside following function)
            _isOk = Position.buy_bottom(_amount=_amount, _sl=_sl, _tp=_tp,
                                        is_isolated=Eainp.EA_IsIsolated)   # Right Trader...is here

            if Util.is_true(_isOk):

                # Recover last Traded Position via Market Infos
                _ticket = MarketPosition.get_position_verylast_filled_onmarket_ticket()

                # add as cfd Position To CFD Opened Position List
                Eagbl.cfdManaja.saveFilledOpenPosOnMarket_ToCFDPosition(_ticket=_ticket, _tpPrice=_tp, _slPrice=_sl)

        # Position Sell
        elif Util.is_position_type_sell(pos_typ):

            _entryPrice = Bar.get_market_upper_price()

            _sl = From.from_entryprice_and_pips_to_sl_pricetarget(entry_price=_entryPrice,
                                                                  sl_pips=Eainp.EA_SL_SecurityPips,
                                                                  pos_typ=pos_typ)
            _tp = From.from_entryprice_and_pips_to_tp_pricetarget(entry_price=_entryPrice,
                                                                  tp_pips=Eainp.EA_TP_TargetPips,
                                                                  pos_typ=pos_typ)

            # recovering pivot coin according to position type
            # _coinsideTyp = From.from_open_ordertyp_to_coinsidetyp(open_postyp=pos_typ)
            # _pivotcoin = From.from_coinsidetyp_to_coin(open_coinside_typ=_coinsideTyp)

            _amount = Saver.get_last_trade_lot_rightcoin_saved()                    # RightCoin Is Capital

            # pivot_coin=_pivotcoin (no longer used inside following function)
            _isOk = Position.sell_upper(_amount=_amount, _sl=_sl, _tp=_tp,
                                        is_isolated=Eainp.EA_IsIsolated)     # Left Trader...is here

            if Util.is_true(_isOk):

                # Recover last Traded Position via Market Infos
                _ticket = MarketPosition.get_position_verylast_filled_onmarket_ticket()

                # add as cfd Position To CFD Opened Position List
                Eagbl.cfdManaja.saveFilledOpenPosOnMarket_ToCFDPosition(_ticket=_ticket, _tpPrice=_tp, _slPrice=_sl)

    # :::::::

# __
    @staticmethod
    def reactive_margin_trader(pos_typ: Eaenum.PosType):
        """ Reactive Margin Trader
        :param pos_typ:
        :return:
        """
        EA.reactive_spot_trader(pos_typ)   # it's the same algorithms like Spot

    # :::::::

# __
    @staticmethod
    def reactive_future_trader(pos_typ: Eaenum.PosType):
        """ reactive Future Trader
        :param pos_typ:
        :return:
        """
        _sl = 0    # for now we don't know
        _tp = 0    # for now we don't know

        _amount = Saver.get_last_trade_lot_saved()  # ???
        # _pivotcoin = None (not need)

        if Util.is_position_type_buy(pos_typ):
            Position.buy_bottom(_amount=_amount, _sl=_sl, _tp=_tp)   # Right Trader

        elif Util.is_position_type_sell(pos_typ):
            Position.sell_upper(_amount=_amount, _sl=_sl, _tp=_tp)   # Left Trader

    # :::::::

#  --- END CLASS EA ---  #
