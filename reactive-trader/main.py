# ######################################### #
#        REACTIVE TRADER MAIN FILE          #
# ######################################### #

# from config import Connect
# from order import Order
# import datetime as dt
import time
import eazcore.lib as ea_lib


class Main(object):

    def __init__(self):
        # Event Handler set
        self.EA_handler = ea_lib.EventHandler()  # Entry point is here

        # Start Bot process
        self.start_process()

    def start_process(self):
        ea_lib._Printer.voyant("BOT__", "::: Bot Handler started... ::")

        # ea_lib.ExChangeInterface.get_exchange()
        ea_lib.Eagbl.EA_lifetime.start_lifetime()  # EA Lifetime setting

        # Loop Process is here
        while not ea_lib.Eagbl.EA_lifetime.is_shutdown_asked():  # Will leave loop when shutdown asked
            self.EA_handler.events_process()                                # Event Process

            time.sleep(1)   # just pause a few

        # down handler
        self.end_process()

    def end_process(self):
        self.EA_handler.on_deinit_call()
        ea_lib._Printer.voyant("BOT__", "::: Bot Handler ended ! ::")


# END CLASS MAIN #

# ......... Main Process is Here
Main()
# .........
