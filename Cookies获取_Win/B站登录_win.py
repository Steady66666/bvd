import time,os
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By

def login(telephone,browser):
    if browser == "Edge":
        options = webdriver.EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Edge(options=options)  
    else:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://passport.bilibili.com/login')
    driver.implicitly_wait(5) #隐式等待浏览器渲染完成，sleep是强制等待
    driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div/div/div[1]/span[2]').click() #手机登录
    driver.find_element(By.XPATH,'//*[@id="geetest-wrap"]/div/div[3]/div[1]/div/input').send_keys(telephone)
    driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div/div/div[3]/div[3]/button/span').click() #获取验证码
    time.sleep(40)
    cookies = {}
    cks = driver.get_cookies()
    for cookie in cks:
        cookies[cookie['name']]=cookie['value']
    cookies = str(cookies).replace('\'','\"')
    cookie_info = f'{{\"cookies\":{cookies}}}'
    with open('cookies.json','w')as f:
        f.write(cookie_info)
        f.close()
    print(cookie_info)
    print('获取完成！\n关闭浏览器')
    driver.quit()

if __name__ == "__main__":
    print('只支持Windows系统的浏览器：Chrome和Edge')
    print('对应文件：\nEdge:msedgedriver.exe\nChrome:chromedriver.exe')
    print('Edge:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
    print('Chrome:https://chromedriver.chromium.org/downloads')
    print('版本号查看：浏览器——设置——关于')
    if os.path.exists('msedgedriver.exe'):
        browser = 'Edge'
    elif os.path.exists('chromedrive.exe'):
        browser = 'Chrome'
    else:
        print('没有找到对应的浏览器驱动，请先根据上述说明下载！')
        exit(1)
    telephone = input('输入11位手机号码：')
    if len(telephone) != 11:
        print('电话号码输入错误！再见！')
        exit(1)
    if telephone:
        print('接下来，请手动点击验证，并且输入验证码登录，请在40秒内完成，40秒到时会自动关闭并且获取生成cookies.json')
        time.sleep(3)
        login(telephone,browser)