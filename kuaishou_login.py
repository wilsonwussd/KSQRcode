import base64
import requests
import warnings
from threading import Thread
from PIL import Image
from io import BytesIO
import http.cookiejar as cookielib
import time
import os

# 忽略SSL警告
warnings.filterwarnings('ignore')

# 添加headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Origin': 'https://id.kuaishou.com',
    'Referer': 'https://id.kuaishou.com/'
}

class QRCodeDisplay(Thread):
    """显示二维码的线程类"""
    def __init__(self, qr_data):
        Thread.__init__(self)
        self.qr_data = qr_data
    
    def run(self):
        img = Image.open(BytesIO(self.qr_data))
        img.show()

def check_login(session):
    """检查cookies是否有效"""
    try:
        session.cookies.load(ignore_discard=True)
    except Exception:
        return False
        
    try:
        check_url = "https://cp.kuaishou.com/rest/pc/authority/account/current"
        response = session.post(
            check_url,
            json={"kuaishou.web.cp.api_ph": "2ab04b8a59d843e385faa6a4965f0836f53f"},
            headers=headers,
            verify=False,
            timeout=10
        ).json()
        return response.get('result') == 1
    except Exception:
        return False

def complete_login(session, token, signature):
    """完成登录流程"""
    try:
        # 第一步：接受结果
        accept_url = 'https://id.kuaishou.com/rest/c/infra/ks/qr/acceptResult'
        accept_data = {
            "qrLoginToken": token,
            "qrLoginSignature": signature,
            "sid": "kuaishou.web.cp.api"
        }
        accept_resp = session.post(accept_url, data=accept_data, headers=headers, verify=False)
        if not accept_resp.ok:
            return False
            
        qr_token = accept_resp.json().get('qrToken')
        if not qr_token:
            return False
            
        # 第二步：回调
        callback_url = 'https://id.kuaishou.com/pass/kuaishou/login/qr/callback'
        callback_data = {
            "qrToken": qr_token,
            "sid": "kuaishou.web.cp.api"
        }
        callback_resp = session.post(callback_url, data=callback_data, headers=headers, verify=False)
        if not callback_resp.ok:
            return False
            
        auth_token = callback_resp.json().get('kuaishou.web.cp.api.at')
        if not auth_token:
            return False
            
        # 第三步：验证token
        verify_url = 'https://www.kuaishou.com/account/login/api/verifyToken'
        verify_data = {
            "authToken": auth_token,
            "sid": "kuaishou.web.cp.api"
        }
        verify_resp = session.post(verify_url, json=verify_data, headers=headers, verify=False)
        if not verify_resp.ok:
            return False
            
        return True
    except Exception:
        return False

def verify_cookies(session):
    """验证cookies有效性"""
    try:
        response = session.post(
            "https://cp.kuaishou.com/rest/pc/authority/account/current",
            json={"kuaishou.web.cp.api_ph": "2ab04b8a59d843e385faa6a4965f0836f53f"},
            headers=headers,
            verify=False
        ).json()
        return response.get('result') == 1
    except:
        return False

def print_cookies(session):
    """打印cookies信息"""
    for cookie in session.cookies:
        print(f"{cookie.name}={cookie.value}")

def login():
    """主登录流程"""
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
    
    if not check_login(session):
        login_url = 'https://id.kuaishou.com/rest/c/infra/ks/qr/start'
        try:
            qr_response = session.post(
                login_url,
                data={"sid": "kuaishou.web.cp.api"},
                headers=headers,
                verify=False
            ).json()
            
            if 'imageData' not in qr_response:
                return None
                
            qr_data = base64.b64decode(qr_response['imageData'])
            QRCodeDisplay(qr_data).start()
            
            token = qr_response['qrLoginToken']
            signature = qr_response['qrLoginSignature']
            
            retry_count = 0
            while retry_count < 60:
                try:
                    status = session.post(
                        'https://id.kuaishou.com/rest/c/infra/ks/qr/scanResult',
                        data={
                            "qrLoginToken": token,
                            "qrLoginSignature": signature
                        },
                        headers=headers,
                        verify=False
                    ).json()
                    
                    if status.get('result') == 1:
                        if complete_login(session, token, signature):
                            session.cookies.save()
                            is_valid = verify_cookies(session)
                            print("cookies_valid={}".format(is_valid))
                            print_cookies(session)
                            return session
                        return None
                            
                except Exception:
                    pass
                    
                time.sleep(2)
                retry_count += 1
                
        except Exception:
            pass
            
    return session

if __name__ == '__main__':
    login() 