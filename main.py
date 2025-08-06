import easytrader
# import win32api

# user = easytrader.use('universal_client')
# user.connect(r'C:\\Apps\\同花顺软件\\同花顺\\xiadan.exe')
# user.enable_type_keys_for_editor() # 同花顺需要使用仿真输入
# user.setEntrust('market') # 启动市价委托
user = easytrader.use('miniqmt')

user.connect(
    miniqmt_path=r"D:\\gjqmt\\userdata_mini",  # QMT 客户端下的 miniqmt 安装路径
    stock_account="8884420208",  # 资金账号
    trader_callback=None, # 默认使用 `easytrader.miniqmt.DefaultXtQuantTraderCallback`
)

target = 'jq'  # joinquant
follower = easytrader.follower(target)
follower.login(user='18698607330', password='47IuoBux')
follower.follow(user, [
        'https://www.joinquant.com/algorithm/live/index?backtestId=88fb5e6f325440def3e7589c5f8881dd', # ST股选股弱转强国九条筛选
        'https://www.joinquant.com/algorithm/live/index?backtestId=6c4dac368821a5d4dedbd9e020b9dc96', # ETF套利小鸡吃米V2.2
        'https://www.joinquant.com/algorithm/live/index?backtestId=88de576631c6b9765f5d31a9393b8c32' # 小市值抽取其他 v1
        ],
        trade_cmd_expire_seconds=300,
        request_timerange=[("09:00", "11:35"), ("12:50", "15:10")],
        slippage=0.001,
)
print("程序执行完了")
