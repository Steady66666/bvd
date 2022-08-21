# 已购课程下载
from blibili_requests import get_response
from cookies import bili_jct
from v_downloader import chips_download
import os,json,subprocess

def live_download(base_dir):
    csrf = bili_jct
    
    live_list_url = 'https://api.bilibili.com/pugv/pay/web/my/paid?ps=10&pn=1'  #课程列表
    list_res = json.loads(str(get_response(live_list_url).json()['data']['data']).replace('\'','\"').replace('False','\"False\"'))
    print(list_res)##############
    for obj in list_res:
        os.chdir(base_dir)
        season_id = obj['id']   #课程id
        title = obj['title']    #课程名称（文件夹名称）
        if not os.path.exists(title):
            os.makedirs(title)
        os.chdir(title)
        obj_url = f'https://api.bilibili.com/pugv/view/web/season?season_id={season_id}&csrf={csrf}'
        obj_res_list = get_response(obj_url).json()['data']['episodes'] #获取到的所有视频信息
        for obj_res_info in obj_res_list:
            avid = obj_res_info['aid']
            cid = obj_res_info['cid']
            obj_title = str(obj_res_info['title']).replace(' ','_') # 单个视频题目
            ep_id = obj_res_info['id']
            if not os.path.exists(obj_title):
                obj_res_info_url = f'https://api.bilibili.com/pugv/player/web/playurl?avid={avid}&cid={cid}&qn=0&fnver=0&fnval=16&fourk=1&ep_id={ep_id}'
                single_dash_url = get_response(obj_res_info_url).json()['data']['dash']
                base_v_url = single_dash_url['video'][0]['base_url']
                back_v_url = single_dash_url['video'][0]['backup_url'] #这个是个列表
                base_a_url = single_dash_url['audio'][0]['base_url']
                back_a_url = single_dash_url['audio'][0]['backup_url'] #这个是个列表
                chips_download(obj_title,base_v_url,back_v_url,base_a_url,back_a_url) # 下载器下载
                cmd = f'ffmpeg -i {obj_title}v.m4s -i {obj_title}a.m4s -c:v copy -c:a aac -strict experimental {obj_title}.mp4 -loglevel quiet'
                print('开始合并。。。')
                subprocess.call(cmd,shell=True)
                os.remove(obj_title+'v.m4s')
                os.remove(obj_title+'a.m4s')

live_download('E:\\Documents\\Github\\打卡')
