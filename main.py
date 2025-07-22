import easytrader
# import win32api

user = easytrader.use('universal_client')
user.connect(r'C:\\Apps\\同花顺软件\\同花顺\\xiadan.exe')
user.enable_type_keys_for_editor() # 同花顺需要使用仿真输入
# user.setEntrust('market') # 启动市价委托
target = 'jq'  # joinquant
follower = easytrader.follower(target)
follower.login(user='18698607330', password='47IuoBux')
follower.follow(user, [
        'https://www.joinquant.com/algorithm/live/index?backtestId=88fb5e6f325440def3e7589c5f8881dd', # ST股选股弱转强国九条筛选
        'https://www.joinquant.com/algorithm/live/index?backtestId=6965531d80c487ccca690ea8b0f221a7', # ETF套利小鸡吃米V2.2
        'https://www.joinquant.com/algorithm/live/index?backtestId=ef67b2e3ba8abff1391985ba867fd12f' # 小市值抽取其他 v1
        ],
        request_timerange=[("09:00", "11:35"), ("12:50", "15:00")],
        slippage=0.005,
)
print("程序执行完了")
