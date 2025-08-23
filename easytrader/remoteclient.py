# -*- coding: utf-8 -*-
import requests

from easytrader.utils.misc import file2dict


def use(broker, host, port=1430, **kwargs):
    return RemoteClient(broker, host, port)


class RemoteClient:
    def __init__(self, broker, host, port=1430, **kwargs):
        self._s = requests.session()
        self._api = "http://{}:{}".format(host, port)
        self._broker = broker

    def prepare(
        self,
        config_path=None,
        user=None,
        password=None,
        exe_path=None,
        comm_password=None,
        timeout=10,
        max_retries=3,
        **kwargs
    ):
        """
        登陆客户端
        :param config_path: 登陆配置文件，跟参数登陆方式二选一
        :param user: 账号
        :param password: 明文密码
        :param exe_path: 客户端路径类似 r'C:\\htzqzyb2\\xiadan.exe',
            默认 r'C:\\htzqzyb2\\xiadan.exe'
        :param comm_password: 通讯密码
        :param timeout: 超时时间（秒）
        :param max_retries: 最大重试次数
        :return:
        """
        params = locals().copy()
        params.pop("self")

        if config_path is not None:
            account = file2dict(config_path)
            params["user"] = account["user"]
            params["password"] = account["password"]

        params["broker"] = self._broker

        retries = 0
        last_exception = None
        
        while retries < max_retries:
            try:
                response = self._s.post(self._api + "/prepare", json=params, timeout=timeout)
                if response.status_code >= 300:
                    raise Exception(response.json().get("error", "Unknown error"))
                return response.json()
            except requests.exceptions.RequestException as e:
                last_exception = e
                retries += 1
                if retries < max_retries:
                    import time
                    time.sleep(1)  # 等待 1 秒后重试
        
        raise Exception(f"Failed to connect to server after {max_retries} attempts: {last_exception}")

    @property
    def balance(self):
        return self.common_get("balance")

    @property
    def position(self):
        return self.common_get("position")

    @property
    def today_entrusts(self):
        return self.common_get("today_entrusts")

    @property
    def today_trades(self):
        return self.common_get("today_trades")

    @property
    def cancel_entrusts(self):
        return self.common_get("cancel_entrusts")

    def auto_ipo(self):
        return self.common_get("auto_ipo")

    def exit(self):
        return self.common_get("exit")

    def common_get(self, endpoint, timeout=10, max_retries=3):
        """
        通用 GET 请求方法，增加超时和重试机制
        :param endpoint: API 端点
        :param timeout: 超时时间（秒）
        :param max_retries: 最大重试次数
        :return: 响应数据
        """
        retries = 0
        last_exception = None
        
        while retries < max_retries:
            try:
                response = self._s.get(self._api + "/" + endpoint, timeout=timeout)
                if response.status_code >= 300:
                    raise Exception(response.json().get("error", "Unknown error"))
                return response.json()
            except requests.exceptions.RequestException as e:
                last_exception = e
                retries += 1
                if retries < max_retries:
                    import time
                    time.sleep(1)  # 等待 1 秒后重试
        
        raise Exception(f"Failed to connect to server after {max_retries} attempts: {last_exception}")

    def buy(self, security, price, amount, timeout=10, max_retries=3, **kwargs):
        """
        买入股票
        :param security: 股票代码
        :param price: 价格
        :param amount: 数量
        :param timeout: 超时时间（秒）
        :param max_retries: 最大重试次数
        :return: 响应数据
        """
        params = locals().copy()
        params.pop("self")

        retries = 0
        last_exception = None
        
        while retries < max_retries:
            try:
                response = self._s.post(self._api + "/buy", json=params, timeout=timeout)
                if response.status_code >= 300:
                    raise Exception(response.json().get("error", "Unknown error"))
                return response.json()
            except requests.exceptions.RequestException as e:
                last_exception = e
                retries += 1
                if retries < max_retries:
                    import time
                    time.sleep(1)  # 等待 1 秒后重试
        
        raise Exception(f"Failed to connect to server after {max_retries} attempts: {last_exception}")

    def sell(self, security, price, amount, timeout=10, max_retries=3, **kwargs):
        """
        卖出股票
        :param security: 股票代码
        :param price: 价格
        :param amount: 数量
        :param timeout: 超时时间（秒）
        :param max_retries: 最大重试次数
        :return: 响应数据
        """
        params = locals().copy()
        params.pop("self")

        retries = 0
        last_exception = None
        
        while retries < max_retries:
            try:
                response = self._s.post(self._api + "/sell", json=params, timeout=timeout)
                if response.status_code >= 300:
                    raise Exception(response.json().get("error", "Unknown error"))
                return response.json()
            except requests.exceptions.RequestException as e:
                last_exception = e
                retries += 1
                if retries < max_retries:
                    import time
                    time.sleep(1)  # 等待 1 秒后重试
        
        raise Exception(f"Failed to connect to server after {max_retries} attempts: {last_exception}")

    def market_buy(self, security, amount, timeout=10, max_retries=3, **kwargs):
        """
        市价买入股票
        :param security: 股票代码
        :param amount: 数量
        :param timeout: 超时时间（秒）
        :param max_retries: 最大重试次数
        :return: 响应数据
        """
        params = locals().copy()
        params.pop("self")

        retries = 0
        last_exception = None
        
        while retries < max_retries:
            try:
                response = self._s.post(self._api + "/market_buy", json=params, timeout=timeout)
                if response.status_code >= 300:
                    raise Exception(response.json().get("error", "Unknown error"))
                return response.json()
            except requests.exceptions.RequestException as e:
                last_exception = e
                retries += 1
                if retries < max_retries:
                    import time
                    time.sleep(1)  # 等待 1 秒后重试
        
        raise Exception(f"Failed to connect to server after {max_retries} attempts: {last_exception}")

    def market_sell(self, security, amount, timeout=10, max_retries=3, **kwargs):
        """
        市价卖出股票
        :param security: 股票代码
        :param amount: 数量
        :param timeout: 超时时间（秒）
        :param max_retries: 最大重试次数
        :return: 响应数据
        """
        params = locals().copy()
        params.pop("self")

        retries = 0
        last_exception = None
        
        while retries < max_retries:
            try:
                response = self._s.post(self._api + "/market_sell", json=params, timeout=timeout)
                if response.status_code >= 300:
                    raise Exception(response.json().get("error", "Unknown error"))
                return response.json()
            except requests.exceptions.RequestException as e:
                last_exception = e
                retries += 1
                if retries < max_retries:
                    import time
                    time.sleep(1)  # 等待 1 秒后重试
        
        raise Exception(f"Failed to connect to server after {max_retries} attempts: {last_exception}")

    def cancel_entrust(self, entrust_no, timeout=10, max_retries=3):
        """
        撤销委托
        :param entrust_no: 委托编号
        :param timeout: 超时时间（秒）
        :param max_retries: 最大重试次数
        :return: 响应数据
        """
        params = {"entrust_no": entrust_no}

        retries = 0
        last_exception = None
        
        while retries < max_retries:
            try:
                response = self._s.post(self._api + "/cancel_entrust", json=params, timeout=timeout)
                if response.status_code >= 300:
                    raise Exception(response.json().get("error", "Unknown error"))
                return response.json()
            except requests.exceptions.RequestException as e:
                last_exception = e
                retries += 1
                if retries < max_retries:
                    import time
                    time.sleep(1)  # 等待 1 秒后重试
        
        raise Exception(f"Failed to connect to server after {max_retries} attempts: {last_exception}")
