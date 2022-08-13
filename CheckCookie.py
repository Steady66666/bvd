from blibili_requests import get_response
from b_auto_login import auto_login
from b_login import login
import time
# 检测cookie是否失效
def check_cookie(check):
    if check != True:
        exit()
    check_url = f'https://account.bilibili.com/site/getCoin'
    check_result = get_response(check_url).json()
    if check_result['code'] == 0:
        coin_num = check_result['data']['money']
        print(f'Cookie有效，目前硬币为:{coin_num}')
    else:
        print('Cookie失效！！！')
        print('cookie存储文件为"cookie.json", 请按照格式填写！！')
        choices = input('是否通过程序获取？(序号)\n 1.程序获取    2.我自己添加\n')
        if choices == "1":
            auto_get = input('请按回车键！')
            if auto_get =='Ang':
                print('作者通道，将会自动验证，虽然没有用！！')
                browser = input('输入你使用的浏览器编号: \n 1.Edge  2.Chrome \n')
                tele = input('输入电话号码：')
                if browser == "1":
                    browser = "Edge"
                    auto_login(tele,browser)
                elif browser == "2":
                    browser = "Chrome"
                    auto_login(tele,browser)
                else:
                    print('错误编号，请选择上述浏览器，再见！')
                    exit()
            else:
                print('目前只支持Chrome和Edge，其他浏览器不考虑 \n 接下来你需要在程序打开浏览器后 40s 内完成短信登录，并且登录成功 \n成功后浏览器会自动关闭并且程序会提示 硬币 数量')
                time.sleep(10)
                browser = input('输入你使用的浏览器编号: \n 1.Edge  2.Chrome \n')
                tele = input('输入电话号码：')
                if browser == "1":
                    browser = "Edge"
                    login(tele,browser)
                    check_cookie(True)
                elif browser == "2":
                    browser = "Chrome"
                    login(tele,browser)
                    check_cookie(True)
                else:
                    print('错误编号，请选择上述浏览器，再见！')
                    exit()
                print('请重新打开程序')
                exit()
        else:
            print('一定要注意Cookies格式哦！！ 祝你好运！文件名称：cookies.json')
            exit()
# check_cookie(True)