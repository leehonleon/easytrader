import easytrader
import win32api
user = easytrader.use('universal_client')
user.connect(r'C:\\Apps\\同花顺软件\\同花顺\\xiadan.exe')
user.enable_type_keys_for_editor() # 同花顺需要使用仿真输入
user.setEntrust('market') # 启动市价委托
target = 'jq'  # joinquant
follower = easytrader.follower(target)
follower.login(user='18698607330', password='47IuoBux')
follower.follow(user, [
        #    'https://www.joinquant.com/algorithm/live/index?backtestId=d0db5b91d613f2216af177f29e895ab9', # 小市值
        'https://www.joinquant.com/algorithm/live/index?backtestId=88fb5e6f325440def3e7589c5f8881dd', # ST股选股弱转强国九条筛选
        'https://www.joinquant.com/algorithm/live/index?backtestId=838d4b59b63eb1098c68389596eb4c68' # ETF套利小鸡吃米V2.1-Clone-Clone-模拟交易
        ],
)