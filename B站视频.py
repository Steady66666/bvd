#<h3>视频选集</h3><span class="cur-page">(1/3)</span>
# -*- coding: UTF-8 -*-
import json,os,re,requests,subprocess,time

#网站请求
def get_response(url):
    headers = {'origin': 'https://www.bilibili.com','referer': 'https://www.bilibili.com','user-agent': 'Mozilla/5.0(iPad;CPUOS13_3likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)CriOS/87.0.4280.77Mobile/15E148Safari/604.1'}
    response = requests.get(url=url,headers=headers)
    return response

#数据收集
def get_video_info(url):
    response = get_response(url)
    json_data = re.findall('<script>window.__playinfo__=(.*?)</script>',response.text)[0]

    title = re.findall('<meta data-vue-meta="true" itemprop="name" name="title" content="(.*?)"><meta data-vue-meta=',response.text)
    if str(title) == "[]":
        title = '未知标题'
    else:
        title = title[0]
    title = str(title).replace(' ','')

    json_data = json.loads(json_data)
    dash = json_data['data']['dash']
    video = dash['video'][0]['baseUrl']
    audio = dash['audio'][0]['baseUrl']
    video_info = [title,video,audio]
    return video_info

#文件下载
def save_file(title,video,audio):
    video_content = get_response(video).content
    audio_content = get_response(audio).content
    with open(title + '.mp4',mode='wb') as f:
        f.write(video_content)
    with open(title + '.wav',mode='wb') as f:
        f.write(audio_content)
    print(title + ' 分块下载完毕！')

#视频合成
def translate_file(title):
    print('视频开始合成：'+title)
    cmd = f'ffmpeg -i {title}.mp4 -i {title}.wav -c:v copy -c:a aac -strict experimental {title}.flv'
    subprocess.call(cmd,shell=True)
    os.remove(title+'.mp4')
    os.remove(title+'.wav')
    print('完成')

# <h3>视频选集</h3><span class="cur-page">(1/3)</span>
def video_list(url):
    response = get_response(url)
    title = re.findall('<meta data-vue-meta="true" itemprop="name" name="title" content="(.*?)"><meta data-vue-meta=',response.text)
    if str(title) == "[]":
        title = '未知标题'
    else:
        title = title[0]
    title = str(title).replace(' ','')
    path_name = title
    os.makedirs(path_name)
    os.chdir(path_name)
    list_no = re.findall('<h3>视频选集</h3><span class="cur-page">((.*?))</span>',response.text)[0]
    list_no = str(list_no)
    list_no = int(re.findall(r"\d+",list_no)[1])
    print('查询到共有：'+str(list_no)+'个视频')
    url = str(re.findall('(.*?)\?',url)[0])
    for i in range(list_no):
        i=i+1
        print('正在处理第'+str(i)+'个视频')
        new_url = url + "?p="+ str(i)
        print(new_url)
        video_info = get_video_info(new_url)
        # path_name = video_info[0]
        # os.makedirs(path_name)
        # os.chdir(path_name)
        save_file(video_info[0],video_info[1],video_info[2])
        name = video_info[0] + str(i)
        title = video_info[0]
        cmd = f'ffmpeg -i {title}.mp4 -i {title}.wav -c:v copy -c:a aac -strict experimental {name}.flv'
        subprocess.call(cmd,shell=True)
        os.remove(title+'.mp4')
        os.remove(title+'.wav')
        print("第 "+str(i)+"/"+str(list_no)+ "个下载完成")
    print('全部下载完成')
    os.chdir(os.pardir)

def main(link):
    # print(re.findall('<h3>视频选集</h3><span class="cur-page">((.*?))</span>',get_response(link).text))
    if str(re.findall('<h3>视频选集</h3><span class="cur-page">((.*?))</span>',get_response(link).text)) == '[]':
        video_info = get_video_info(link)
        save_file(video_info[0],video_info[1],video_info[2])
        translate_file(video_info[0])
    else:
        print('该链接中视频为列表，现进行列表下载————>>')
        video_list(link)

# 检测cookie是否失效
def check_cookie():
    check_url = f'https://account.bilibili.com/site/getCoin'
    check_result = get_response(check_url).json()
    if check_result['code'] == 0:
        coin_num = check_result['data']['money']
        print(f'Cookie有效，目前硬币为{coin_num}')
    else:
        print('请重新获取Cookie!!')
        cookie = input('输入你获取到的Cookie:')
        # cookie = quote(cookie,'utf-8')
        with open('cookie','w')as f:
            f.write(cookie)
            f.close()
        print('再次运行本程序！')
        exit()

if __name__ == "__main__":
    # get_cookies = input('请输入你的cookie，会不定时失效哦！')
    cookie = open('cookie').read()
    # print(cookie)
    check_cookie()
    # headers = {'origin': 'https://www.bilibili.com','referer': 'https://www.bilibili.com','user-agent': 'Mozilla/5.0(iPad;CPUOS13_3likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)CriOS/87.0.4280.77Mobile/15E148Safari/604.1','cookie':cookie}
    choice = int(input('1、下载up主所有视频；   2、下载单个视频（支持下载列表）：'))
    print(type(choice))
    if choice == 1:
        up_link = input('输入需要下载所有视频的up主主页：') #https://space.bilibili.com/xxxxxxxxx
        mid = re.findall('\d+',up_link)[0] # up主号码
        pn = 0
        up_name = str(re.findall('<title>(.*?)的个人空间_哔哩哔哩_Bilibili</title>',get_response(up_link).text)[0])
        path_up = str(mid)+'_'+str(up_name)
        os.makedirs(path_up)
        os.chdir(path_up)
        while pn<15:
            pn = pn + 1
            url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&tid=0&pn={pn}&keyword=&order=pubdate&jsonp=jsonp'
            time.sleep(10)
            res = json.loads(get_response(url).text)
            r = res['data']['list']['vlist']
            if r == '[]':
                pn = pn-1
                print(pn)
                break
            else:
                for mid_d in r:
                    bvid = mid_d['bvid']
                    link = f'https://www.bilibili.com/video/{bvid}?'
                    main(link)

    elif choice == 2:
        video_link = input('输入需要下载视频的网址：\n')
        main(video_link)

    else:
        print('输入错了！！！再见！')
        exit()
