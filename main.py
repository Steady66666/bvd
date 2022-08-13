from envCheck import filesCheck
filesCheck(True)
from CheckCookie import check_cookie
check_cookie(True)
from b_video import download

# 功能选择
target = input('1.番剧/综艺/电影    2.单个投稿视频    3.UP所有视频\n')
if target == '1':
    print('你选择的是：番剧/综艺 \n加载中，请稍后。。。\n')
    from b_drama import main
    main(True)
elif target == '2':
    print('你选择的是：单个投稿视频\n准备好视频链接即可') 
    while True:
        download(target)
        keepgoing = input('是否继续下载？\n1.yes    2.no\n')
        if keepgoing == '1':
            download(target)
        else:
            exit()
elif target == '3':
    print('你选择的是：UP所有视频 \n加载中，请稍后。。。\n')
    while True:
        download(target)
        keepgoing = input('是否继续下载？\n1.yes    2.no\n')
        if keepgoing == '1':
            download(target)
        else:
            exit()
else:
    print('退出程序中。。。')
    exit()