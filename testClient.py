from easytrader import remoteclient
import datetime
import hashlib
from trade_functions import *

user = remoteclient.use(
    'miniqmt',
    host='file.march-solutions.cn',
    port='1430')
# 生成基于当前日期的hash值
today = datetime.date.today().strftime('%Y-%m-%d')
expected_password = hashlib.md5(today.encode('utf-8')).hexdigest()
user.prepare(
    password=expected_password,
)
# user.sell('002479',9.96, 200)

# user.market_buy('002479', 200)
# user.market_sell('002479', 300)
# print(user.balance)
# print(user.position)
# print(user.today_entrusts)
# print(user.today_trades)
# res = user.cancel_entrust(1098909536)
# print(res)
# buy_until_target(user, '002479', 200)
buy_until_target(user, '600107', 2000)
# sell_until_target(user, '000968', 0)