import requests
import http.cookiejar as cookielib

def test_cookies():
    """测试保存的cookies是否有效"""
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
    
    try:
        # 加载cookies
        session.cookies.load(ignore_discard=True)
        
        # 测试cookies
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        
        # 访问快手个人信息接口
        response = session.post(
            "https://cp.kuaishou.com/rest/pc/authority/account/current",
            json={"kuaishou.web.cp.api_ph": "2ab04b8a59d843e385faa6a4965f0836f53f"},
            headers=headers,
            verify=False
        ).json()
        
        if response.get('result') == 1:
            print('Cookies有效，当前登录用户信息：')
            print(f"用户名: {response.get('user', {}).get('user_name', '未知')}")
            return True
    except Exception as e:
        print(f'验证cookies时发生错误: {str(e)}')
    return False

if __name__ == '__main__':
    test_cookies() 