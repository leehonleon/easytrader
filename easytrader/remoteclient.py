# -*- coding: utf-8 -*-
import requests
import json
def use(broker, host, port=1430, **kwargs):
    return RemoteClient(broker, host, port)

def file2dict(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

class RemoteClient:
    def __init__(self, broker, host, port=1430, **kwargs):
        self._s = requests.session()
        self._api = "http://{}:{}".format(host, port)
        self._broker = broker
        self._is_connected = False

    def common_post(self, endpoint, params):
        """
        共通 POST 请求方法
        :param endpoint: API 端点
        :param params: 请求参数
        :return: 响应结果
        """
        if not self._is_connected:
            return {'error': "未连接"}
        response = self._s.post(self._api + "/" + endpoint + '?a=1', json=params)
        if response.status_code >= 300 or response.status_code == 201:
            # raise Exception(response.json()["error"])
            return {'error': response.json()["error"]}
        return response.json()

    def common_get(self, endpoint):
        """
          共通 GET 请求方法
          :param endpoint: API 端点
          :return: 响应结果
          """
        if not self._is_connected:
            return {'error': "未连接"}
        response = self._s.get(self._api + "/" + endpoint)
        if response.status_code >= 300:
            # raise Exception(response.json()["error"])
            return {'error': response.json()["error"]}
        return response.json()

    def prepare(
        self,
        config_path=None,
        user=None,
        password=None,
        exe_path=None,
        comm_password=None,
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
        :return:
        """
        params = locals().copy()
        params.pop("self")

        if config_path is not None:
            account = file2dict(config_path)
            params["user"] = account["user"]
            params["password"] = account["password"]

        params["broker"] = self._broker

        try:
            response = self._s.post(self._api + "/prepare", json=params)
            if response.status_code >= 300:
                self._is_connected = False
                return {'error': response.json()["error"]}
            else:
                self._is_connected = True
        except Exception as e:
            self._is_connected = False
            return {'error': "连接失败"}

        return response.json()

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
        self._is_connected = False
        return self.common_get("exit")

    def is_connected(self):
        """
        检查是否已连接到服务器
        :return: 连接状态 (True/False)
        """
        return self._is_connected


    def buy(self, security, price, amount, **kwargs):
        params = locals().copy()
        params.pop("self")
        return self.common_post("buy", params)

    def sell(self, security, price, amount, **kwargs):
        params = locals().copy()
        params.pop("self")
        return self.common_post("sell", params)

    def market_buy(self, security, amount, **kwargs):
        params = locals().copy()
        params.pop("self")
        return self.common_post("market_buy", params)

    def market_sell(self, security, amount, **kwargs):
        params = locals().copy()
        params.pop("self")
        return self.common_post("market_sell", params)

    def cancel_entrust(self, entrust_no):
        params = locals().copy()
        params.pop("self")
        return self.common_post("cancel_entrust", params)

