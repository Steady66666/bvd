import time,os
from selenium import webdriver
from PIL import Image
from selenium.webdriver import ActionChains
from bot_api import base64_api

def auto_login(telephone,browser):
    if browser == "Edge":
        driver = webdriver.Edge()
    else:
        driver = webdriver.Chrome()
    driver.get('https://passport.bilibili.com/login')
    driver.implicitly_wait(5) #隐式等待浏览器渲染完成，sleep是强制等待
    driver.maximize_window()#最大化浏览器
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div/div/div[1]/span[2]').click() #手机登录
    driver.find_element_by_xpath('//*[@id="geetest-wrap"]/div/div[3]/div[1]/div/input').send_keys(telephone)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div/div/div[3]/div[3]/button/span').click() #获取验证码
    time.sleep(2)
    img_label = driver.find_element_by_css_selector('body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowclick > div.geetest_panel_next > div > div')
    #保存图片
    driver.save_screenshot('big.png') #截取当前整个页面
    time.sleep(5)
    #location可以获取这个元素左上角坐标
    # print(img_label.location)
    #size可以获取这个元素的宽(width)和高(height)
    # print(img_label.size)
    #计算验证码的左右上下横切面
    left = img_label.location['x']
    top = img_label.location['y']
    right = img_label.location['x'] + img_label.size['width']
    down = img_label.location['y'] + img_label.size['height']
    im = Image.open('big.png')
    im = im.crop((left,top,right,down))
    im.save('yzm.png')
    img_path = 'yzm.png'

    result = base64_api(uname='Ang', pwd='Qjl118318', img=img_path,typeid=27)
    # print(result)
    # print('验证码识别结果：', result)
    result_list = result.split('|')
    for result in result_list:
        print(result)
        x = result.split(',')[0]
        y = result.split(',')[1]
        ActionChains(driver).move_to_element_with_offset(img_label, int(x), int(y)).click().perform()  # perform()执行整个动作链

    #点击确认按钮
    driver.find_element_by_css_selector('body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowclick > div.geetest_panel_next > div > div > div.geetest_panel > a > div').click()
    os.remove("big.png")
    os.remove("yzm.png")
    print('只输入验证码就可以了！！！！  不要点击登录！   20s后自动点击登录  ')
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div/div/div[3]/div[3]/div/input').click() #点击验证码输入区
    time.sleep(20)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div/div/div[5]/a[1]').click() #登录
    time.sleep(5)
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