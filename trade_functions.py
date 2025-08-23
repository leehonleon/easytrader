import time
import re

def extract_stock_code(stock_code):
    """
    提取股票代码中的数字部分
    :param stock_code: 原始股票代码（如 'sh022210.XSED'）
    :return: 数字部分（如 '022210'）
    """
    # 使用正则表达式匹配数字部分
    match = re.search(r'\d+', stock_code)
    if match:
        return match.group()
    return stock_code  # 如果没有数字部分，返回原值

def buy_until_target(user, stock_code, target_quantity):
    """
    买入指定股票直到达到目标数量
    :param user: 用户对象
    :param stock_code: 股票代码
    :param target_quantity: 目标数量
    """
    stock_code = extract_stock_code(stock_code)
    # 获取当前持仓数量
    position = user.position
    current_quantity = 0
    for pos in position:
        if pos['stock_code'].startswith(stock_code):
            current_quantity = pos['volume']
            break
    
    # 计算剩余需要买入的数量
    remaining_quantity = target_quantity - current_quantity
    if remaining_quantity <= 0:
        print(f"已达到目标数量 {target_quantity} 股")
        return
    
    # 委托买入剩余数量
    print(f"委托买入 {remaining_quantity} 股 {stock_code}")
    user.market_buy(stock_code, remaining_quantity)
    
    # 启动监控线程
    import threading
    def monitor_entrust():
        max_attempts = 5
        attempts = 0
        while attempts < max_attempts:
            # 检查委托状态
            entrusts = user.today_entrusts
            found_entrust = False
            for entrust in entrusts:
                if entrust['stock_code'].startswith(stock_code) and entrust['order_type_name'] == '买入':
                    found_entrust = True
                    if entrust['order_status_name'] == '已成':
                        print(f"买入委托已成交，成交数量: {entrust['traded_volume']} 股")
                        break
                    elif entrust['order_status_name'] in ['已报待撤', '已报', '废单']:
                        print(f"买入委托未成交，撤销并重新委托")
                        user.cancel_entrust(entrust['order_id'])
                        # 重新发起委托
                        user.market_buy(stock_code, remaining_quantity)
                        break
            
            if not found_entrust:
                print("未找到相关委托，可能已成交或撤销")
                break
            
            # 等待一段时间后再次检查
            time.sleep(1)
            attempts += 1
        print(f"尝试 {max_attempts} 次仍未成交，放弃监控")
    
    # 启动监控线程
    threading.Thread(target=monitor_entrust).start()


def sell_until_target(user, stock_code, target_quantity):
    """
    卖出指定股票直到达到目标数量
    :param user: 用户对象
    :param stock_code: 股票代码
    :param target_quantity: 目标数量
    """
    stock_code = extract_stock_code(stock_code)
    # 获取当前持仓数量
    position = user.position
    current_quantity = 0
    for pos in position:
        if pos['stock_code'].startswith(stock_code):
            current_quantity = pos['volume']
            break
    
    # 检查是否已达到目标数量
    if current_quantity <= 0:
        print(f"已无持仓可卖")
        return
    
    # 委托卖出目标数量
    sell_quantity = min(current_quantity - target_quantity, current_quantity)
    print(f"委托卖出 {sell_quantity} 股 {stock_code}")
    user.market_sell(stock_code, sell_quantity)
    
    # 启动监控线程
    import threading
    def monitor_entrust():
        time.sleep(2)
        max_attempts = 5
        attempts = 0
        while attempts < max_attempts:
            # 检查委托状态
            entrusts = user.today_entrusts
            found_entrust = False
            for entrust in entrusts:
                if entrust['stock_code'].startswith(stock_code) and entrust['order_type_name'] == '卖出':
                    found_entrust = True
                    if entrust['order_status_name'] == '已成':
                        print(f"卖出委托已成交，成交数量: {entrust['traded_volume']} 股")
                        break
                    elif entrust['order_status_name'] in ['已报待撤', '已报']:
                        print(f"卖出委托未成交，撤销并重新委托")
                        print(user.cancel_entrust(entrust['order_id']))
                        # 重新发起委托
                        user.market_sell(stock_code, sell_quantity)
                        break
            
            if not found_entrust:
                print("未找到相关委托，可能已成交或撤销")
                break
            
            # 等待一段时间后再次检查
            time.sleep(1)
            attempts += 1
        print(f"尝试 {max_attempts} 次仍未成交，放弃监控")
    
    # 启动监控线程
    threading.Thread(target=monitor_entrust).start()