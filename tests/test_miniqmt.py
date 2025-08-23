import easytrader
from easytrader.miniqmt.miniqmt_trader import MiniqmtTrader

user: MiniqmtTrader = easytrader.use('miniqmt')

user.connect(
    miniqmt_path=r"D:\\Apps\\国金QMT交易端模拟\\userdata_mini",  # QMT 客户端下的 miniqmt 安装路径
    stock_account="55011468",  # 资金账号
    trader_callback=None, # 默认使用 `easytrader.miniqmt.DefaultXtQuantTraderCallback`
)
print(user.balance) # 账户资金 对象数组
# user.buy('301288', price=14.0, amount=100)
# user.sell('600138',9.96, 200)
# user.market_buy('002652',1000)
# target = 'jq'  # joinquant
# follower = easytrader.follower(target)
# follower.login(user='18698607330', password='47IuoBux')
# follower.follow(user, [
#         'https://www.joinquant.com/algorithm/live/index?backtestId=88fb5e6f325440def3e7589c5f8881dd', # ST股选股弱转强国九条筛选
#         'https://www.joinquant.com/algorithm/live/index?backtestId=6965531d80c487ccca690ea8b0f221a7', # ETF套利小鸡吃米V2.2
#         'https://www.joinquant.com/algorithm/live/index?backtestId=ef67b2e3ba8abff1391985ba867fd12f' # 小市值抽取其他 v1
#         ],
#         trade_cmd_expire_seconds=30000,
#         request_timerange=[("09:00", "11:35"), ("12:50", "15:10")],
#         slippage=0.005,
#                 cmd_cache=False,
# )
print(user.position) # 持仓股票 对象数组
print(user.today_entrusts) # 今日委托
print(user.today_trades) # 今日成交
#user.cancel_entrust(entrust_no) 撤销委托
