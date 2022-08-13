#<h3>视频选集</h3><span class="cur-page">(1/3)</span>
# -*- coding: UTF-8 -*-
import json,os,re,subprocess,time
from blibili_requests import get_response
from v_downloader import chips_download

#数据收集
def get_video_info(url):
    response = get_response(url)
    json_data = re.findall('<script>window.__playinfo__=(.*?)</script>',response.text)[0] #json在html里面

    title = re.findall('<meta data-vue-meta="true" itemprop="name" name="title" content="(.*?)"><meta data-vue-meta=',response.text)
    if str(title) == "[]":
        title = '未知标题'
    else:
        title = title[0]
    title = str(title).replace(' ','').replace('&amp;','').replace('&lt;','').replace('&#x27;','').replace('&gt;','').replace('&quot;','').replace('&#770;','').replace('&#771;','').replace('','')

    json_data = json.loads(json_data) #视频信息格式化
    dash = json_data['data']['dash']
    video = dash['video'][0]['baseUrl']
    video_back = dash['video'][0]['backupUrl']
    audio = dash['audio'][0]['baseUrl']
    audio_back = dash['audio'][0]['backupUrl']
    video_info = [title,video,video_back,audio,audio_back] # 标题，视频主链接，视频备用链接
    return video_info

#文件下载
def save_file(title,video,video_back,audio,audio_back):
    if not os.path.exists(f'{title}.flv'):
        chips_download(title,video,video_back,audio,audio_back)
        # print('下载中。。。。')
        # video_content = get_response(video).content
        # audio_content = get_response(audio).content
        # with open(title + '.mp4',mode='wb') as f:
        #     f.write(video_content)
        # with open(title + '.wav',mode='wb') as f:
            # f.write(audio_content)
    print(title + ' 分块下载完毕！')

#视频合成
def translate_file(title):
    if not os.path.exists(f'{title}.flv'):
        print('视频开始合成：'+title)
        cmd = f'ffmpeg -i {title}v.m4s -i {title}a.m4s -c:v copy -c:a aac -strict experimental {title}.flv'
        subprocess.call(cmd,shell=True)
        os.remove(title+'a.m4s')
        os.remove(title+'v.m4s')
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
        save_file(video_info[0],video_info[1],video_info[2],video_info[3],video_info[4])
        name = video_info[0] + str(i)
        title = video_info[0]
        cmd = f'ffmpeg -i {title}.mp4 -i {title}.wav -c:v copy -c:a aac -strict experimental {name}.flv'
        subprocess.call(cmd,shell=True)
        os.remove(title+'.mp4')
        os.remove(title+'.wav')
        print("第 "+str(i)+"/"+str(list_no)+ "个下载完成")
    print('全部下载完成')
    os.chdir(os.pardir)

def link_type(link):
    # print(re.findall('<h3>视频选集</h3><span class="cur-page">((.*?))</span>',get_response(link).text))
    if str(re.findall('<h3>视频选集</h3><span class="cur-page">((.*?))</span>',get_response(link).text)) == '[]':
        video_info = get_video_info(link)
        save_file(video_info[0],video_info[1],video_info[2],video_info[3],video_info[4])
        translate_file(video_info[0])
    else:
        print('该链接中视频为列表，现进行列表下载————>>')
        video_list(link)


def download(choice):
    if choice == '3':
        up_link = input('输入需要下载所有视频的up主主页URL：') #https://space.bilibili.com/xxxxxxxxx
        mid = re.findall('\d+',up_link)[0] # up主号码
        pn = 0
        up_name = str(re.findall('<title>(.*?)的个人空间_哔哩哔哩_Bilibili</title>',get_response(up_link).text)[0])
        path_up = str(mid)+'_'+str(up_name)
        if not os.path.exists(f'{path_up}'):
            os.makedirs(path_up)
        os.chdir(path_up)
        while pn<15:
            pn = pn + 1
            url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&tid=0&pn={pn}&keyword=&order=pubdate&jsonp=jsonp'
            # time.sleep(10)
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
                    link_type(link)
        os.chdir(os.path.pardir)

    elif choice == '2':
        video_link = input('输入需要下载视频的网址：\n')
        link_type(video_link)

    else:
        print('输入错误！！！再见！')
        exit()
