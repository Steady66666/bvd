import time
from selenium import webdriver

def login(telephone,browser):
    if browser == "Edge":
        driver = webdriver.Edge()
    else:
        driver = webdriver.Chrome()
    driver.get('https://passport.bilibili.com/login')
    driver.implicitly_wait(5) #隐式等待浏览器渲染完成，sleep是强制等待
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div/div/div[1]/span[2]').click() #手机登录
    driver.find_element_by_xpath('//*[@id="geetest-wrap"]/div/div[3]/div[1]/div/input').send_keys(telephone)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div/div/div[3]/div[3]/button/span').click() #获取验证码
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
    print('获取完成！')
    driver.quit()
# login(telephone='15025582580',browser='Edge')