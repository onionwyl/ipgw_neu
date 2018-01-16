import requests
import random

class IPGW_Crawler:
    def __init__(self):
        self.ip = ""
        self.cookies = {}

    def login(self, username, password, mode=1):
        url = ""
        headers = {}
        if mode == 1:
            url = "https://ipgw.neu.edu.cn/srun_portal_pc.php?ac_id=1&"
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }
        elif mode == 2:
            url = "https://ipgw.neu.edu.cn/srun_portal_phone.php?ac_id=1&"
            headers = {
                'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36"
            }
        data = {
            'action': 'login',
            'ac_id': '1',
            'username': username,
            'password': password
        }
        req = requests.post(url, data=data, headers=headers)
        req.encoding = 'UTF-8'
        self.cookies = req.cookies
        if(req.text.find("用户不存在") != -1):
            return 1    # 用户名不存在
        elif(req.text.find("不一致") != -1):
            return 2    # 密码错误
        self.query()
        return 0    # 登陆成功

    def logout(self, username, password, mode):
        url = {}
        headers = {}
        # headers for mode 1 & mode 3
        url = "https://ipgw.neu.edu.cn/srun_portal_pc.php?ac_id=1&"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        # data for mode 1 & mode 2
        data = {
            'action': 'auto_logout',
            'ip': self.ip,
            'username': username
        }
        if mode == 2:
            url = "https://ipgw.neu.edu.cn/srun_portal_phone.php?ac_id=1&"
            headers = {
                'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36"
            }
        if mode == 3:
            data = {
                'action': 'logout',
                'ajax': '1',
                'username': username,
                'password': password
            }
        req = requests.post(url, data=data, headers=headers)
        req.encoding = 'UTF-8'

    def query(self):
        cookie = self.cookies
        k = random.random() * (100001)
        url = "https://ipgw.neu.edu.cn/include/auth_action.php?k=" + str(k)
        data = {
            'action': 'get_online_info',
            'key': k
        }
        req = requests.post(url, data, cookies=cookie)
        message = req.text.split(',')
        used_flux = float(message[0]) / (1000 * 1000)
        used_time = (int(int(message[1]) / 3600), int((int(message[1]) % 3600) / 60), int(message[1]) % 3600 % 60)
        user_balance = message[2]
        ip_addr = message[5]
        self.ip = ip_addr
        # print("已用流量：%.2fM" % (float(message[0]) / (1000 * 1000)))
        # print(
        #     "已用时长：%d:%02d:%02d" % (int(message[1]) / 3600, (int(message[1]) % 3600) / 60, int(message[1]) % 3600 % 60))
        # print("帐户余额：￥" + message[2])
        # print("IP地址：" + message[5])
        return used_flux, used_time, user_balance, ip_addr

if __name__ == "__main__":
    ipgw = IPGW_Crawler()
    ipgw.login('username', 'password', 1)
