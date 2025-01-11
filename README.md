# 快手扫码登录工具

这是一个使用Python实现的快手扫码登录工具，可以获取和验证登录cookies。

## 功能特点

1. 自动获取登录二维码
2. 显示二维码等待扫描
3. 自动完成登录流程
4. 获取并保存cookies
5. 验证cookies有效性
6. 支持cookies自动保存和加载

## 使用方法

### 1. 环境要求
- Python 3.x
- 必需的Python包：
  ```bash
  pip install pillow requests urllib3==1.26.6
  ```

### 2. 使用步骤

1. 克隆仓库：
```bash
git clone https://github.com/your-username/KS-QR.git
cd KS-QR
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python kuaishou_login.py
```

4. 使用快手APP扫描显示的二维码

5. 程序将自动获取cookies并验证，输出格式如下：
```
cookies_valid=True
did=xxx
userId=xxx
didv=xxx
kuaishou.web.cp.api_st=xxx
kuaishou.web.cp.api_ph=xxx
passToken=xxx
```

### 3. cookies说明

获取的cookies包含以下字段：
- `did`: 设备ID
- `userId`: 用户ID
- `didv`: 设备验证ID
- `kuaishou.web.cp.api_st`: API认证token
- `kuaishou.web.cp.api_ph`: API认证哈希
- `passToken`: 通行证token

cookies将自动保存在当前目录的`cookies.txt`文件中。

## 注意事项

1. 首次运行时需要扫码登录
2. cookies有效期有限，失效后需要重新登录
3. 使用时请遵守快手平台的使用规则和条款
4. 本工具仅供学习和研究使用 