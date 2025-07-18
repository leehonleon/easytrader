import easytrader
from easytrader.joinquant_follower import JoinQuantFollower
from easytrader.universal_clienttrader import UniversalClientTrader

import signal
import sys

user: UniversalClientTrader = easytrader.use('universal_client')
user.setEntrust('market')
user.connect(r'C:\\Apps\\同花顺软件\\同花顺\\xiadan.exe')
user.enable_type_keys_for_editor()
user.buy('sh000736', 4.20, 100)