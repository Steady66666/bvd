import os

# 环境检测
def filesCheck(check):
    if check != True:
        exit()
    cookie_file = os.path.exists('cookies.json')
    # print(cookie_file)
    if not cookie_file:
        print('cookie文件不存在,自动创建')
        ckEnv = f"{{\"cookies\":{{}}}}"
        with open('cookies.json','w')as f:
            f.write(ckEnv)
            f.close()
        print('CK初始化完成！')
    # bot_file = os.path.exists('settings.json')
    # if not bot_file:
    #     print('settings文件不存在')
    #     botEnv = f"{{\"user_name\":\"\",\"password\":\"\"}}"
    #     print('http://www.kuaishibie.cn \n去该网站注册得到用户名和密码')
    #     with open('settings.json','w')as f:
    #         f.write(botEnv)
    #         f.close()
    #     print('请完善setting的参数！')
    #     exit()
    browser_file = os.path.exists('chromedriver.exe') or os.path.exists('msedgedriver.exe')
    if not browser_file:
        print('环境不满足，请先下载好chromedriver或者msedgedriver后重新打开该程序！')
        print('Edge:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
        print('Chrome:https://chromedriver.chromium.org/downloads')
        print('版本看浏览器设置里面的——关于')
        exit()
    print('环境检测完成')
# filesCheck(True)