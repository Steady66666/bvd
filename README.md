# B番下载   番/电影/综艺/记录/电视剧
# 会遍历下载，需要下载的先追番，不需要的临时取消追番
## Video codec hevc not compatible with flv    
更改flv为mp4，因为兼容性问题    mp4可以兼容更多的视频格式
## 请求会超时有时，所以视频不一定会下载成功，希望留下报错信息来帮助完善程序
## 所见即所得，需要获取Cookies登录信息
没有Cookies信息是默认的游客身份，权限极低，所以这里强制需要Cookies
## 番下载器位于 B_downloader
主程序为main.py
## Cookies.json 获取程序位于 Cookies获取通用
默认地址为：http://127.0.0.1:9876 如果需要更改端口 在get_cookies.py底端更改即可
编译命令为<pyinstaller get_cookies.spec>,不然编译出来的文件没有网页，即没有静态html文件，会报错不能用！
### 投稿视频下载在其他分支，例如test分支，没有完善。但是能用，程序叫<b_video.py>