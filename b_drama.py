# -*- coding: UTF-8 -*-
import json,os,time
from blibili_requests import get_response
from cookies import dedeuserid
from v_downloader import chips

# 获取追剧列表
def series_list(vmid,drama_type):
    # vmid = re.findall(r"\d+\.?\d*",url)[0] 
    millis = int(round(time.time() * 1000))
    url = f'https://api.bilibili.com/x/space/bangumi/follow/list?type={drama_type}&follow_status=0&pn=1&ps=30&vmid={vmid}&ts={millis}' #获取50个剧集信息
    # print(url)
    series_list_info = get_response(url).json()['data']['list']
    info = []
    for single in series_list_info:
        media_id = single['media_id']
        id_url = f'https://api.bilibili.com/pgc/review/user?media_id={media_id}'
        ep_id = get_response(id_url).json()['result']['media']['new_ep']['id']
        title = single['title'] + '--' + single['season_title']
        sinfo = f'{{\"name\":\"{title}",\"media_id\":\"{media_id}\",\"ep_id\":\"{ep_id}\"}}'
        sinfo = json.loads(sinfo)
        info.append(sinfo)
    return info

# 获取所选剧集信息
def seasons_info(vmid,drama_type):
    res = series_list(vmid,drama_type)
    a = 0
    for list_info in res:
        a=a+1
        msg = str(a) + '. ' +list_info['name']
        print(msg)
    chooise = int(input("输入编号："))-1
    dir_name = res[chooise]['name']
    if not os.path.exists(f'{dir_name}'):
        os.mkdir(dir_name)
    os.chdir(dir_name)
    ep_id = res[chooise]['ep_id']
    url = f'https://api.bilibili.com/pgc/view/web/season?ep_id={ep_id}'
    vs_info = get_response(url).json()['result']['episodes']
    urls = []
    for v_info in vs_info:
        aid = v_info['aid']
        cid = v_info['cid']
        v_title = v_info['share_copy']
        ep_id = v_info['id']
        singel_url = f'https://api.bilibili.com/pgc/player/web/playurl?avid={aid}&cid={cid}&fnver=0&fnval=4048&fourk=1&ep_id={ep_id}'
        singel_url = f'{{\"v_title\":\"{v_title}\",\"singel_url\":\"{singel_url}\"}}'
        singel_url = json.loads(singel_url)
        urls.append(singel_url)
    return urls
'''
# 下载视频和音频
def download(url,title):
    # print(url)#调试
    if not os.path.exists(f'{title}.flv'):
        v_a_url = get_response(url).json()
        v_url = v_a_url['result']['dash']['video'][0]['baseUrl']
        a_url = v_a_url['result']['dash']['audio'][0]['baseUrl']

        print(f'正在下载视频：{title}')
        video_content = get_response(v_url).content
        with open(title + 'v.m4s',mode='wb') as f:
            f.write(video_content)
        
        print('开始下载音频...')
        audio_content = get_response(a_url).content
        with open(title + 'a.m4s',mode='wb') as f:
            f.write(audio_content)    
        
        print(f'{title} 下载完成！\n 开始合并文件...')
        cmd = f'ffmpeg -i {title}v.m4s -i {title}a.m4s -c:v copy -c:a aac -strict experimental {title}.flv'
        subprocess.call(cmd,shell=True)
        os.remove(title+'a.m4s')
        os.remove(title+'v.m4s')
        print(f'{title}--完成')
'''
# 启动
def main(run):
    if run != True:
        exit()
    drama_type = input(f'1.追番     2.追剧\n')
    urls_json = seasons_info(dedeuserid,drama_type)
    # print(urls_json)#调试
    for urls in urls_json:
        url = urls['singel_url']
        title = urls['v_title']
        title = str(title).replace(' ','')
        # print(url)
        # download(url,title)
        chips(url,title,v_type='drama')
        print('下一个...')
    print('全部下载完成！')
    keepgoing = input('是否继续下载？\n1.yes    2.no\n')
    if keepgoing == '1':
        os.chdir(os.path.pardir)
        main(True)
    else:
        exit()
