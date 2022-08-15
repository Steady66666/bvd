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
    print('环境检测完成')
# filesCheck(True)