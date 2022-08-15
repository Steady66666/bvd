from blibili_requests import get_response
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
        print('请打开《B站登录》自动获取Cookies')
        print('自己获取的话：cookie存储文件为"cookie.json", 请按照格式填写！！')
        exit(1)