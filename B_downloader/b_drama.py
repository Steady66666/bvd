# -*- coding: UTF-8 -*-
import json,os,time
from blibili_requests import get_response
from cookies import dedeuserid
from v_downloader import chips
base_path = os.getcwd() #根目录

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
        season_type_name = single['season_type_name']
        id_url = f'https://api.bilibili.com/pgc/review/user?media_id={media_id}'
        ep_id = get_response(id_url).json()['result']['media']['new_ep']['id']
        title = single['title'] + '--' + single['season_title']
        sinfo = f'{{\"name\":\"{title}",\"media_id\":\"{media_id}\",\"ep_id\":\"{ep_id}\",\"season_type_name\":\"{season_type_name}\"}}'
        sinfo = json.loads(sinfo)
        info.append(sinfo)
    return info

# 获取所选剧集信息
def seasons_info(vmid,drama_type):
    res = series_list(vmid,drama_type) #{"name":"海绵宝宝","media_id":"sdsd",}
    urls = []
    for sub_res in res:
        os.chdir(base_path)
        dir_name = sub_res['name']              #题目
        work_dir = sub_res['season_type_name'] # 分类名称
        # file_path = base_path+work_dir+dir_name
        # print(file_path)
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)
        os.chdir(work_dir)

        if not os.path.exists(f'{dir_name}'):
            os.mkdir(dir_name)
        os.chdir(dir_name)
        ep_id = sub_res['ep_id']
        url = f'https://api.bilibili.com/pgc/view/web/season?ep_id={ep_id}'
        vs_info = get_response(url).json()['result']['episodes']
        for v_info in vs_info:
            aid = v_info['aid']
            cid = v_info['cid']
            v_title = v_info['share_copy']
            ep_id = v_info['id']
            singel_url = f'https://api.bilibili.com/pgc/player/web/playurl?avid={aid}&cid={cid}&fnver=0&fnval=4048&fourk=1&ep_id={ep_id}'
            singel_url = f'{{\"v_title\":\"{v_title}\",\"singel_url\":\"{singel_url}\",\"file_path_work\":\"{work_dir}\",\"file_path_name\":\"{dir_name}\"}}'
            singel_url = json.loads(singel_url)
            urls.append(singel_url)
    return urls

# 启动
def main(run):
    if run != True:
        exit()
    # drama_type = input(f'1.追番     2.追剧\n')
    drama_type = ["1","2"]
    for i in drama_type:
        os.chdir(base_path)
        urls_json = seasons_info(dedeuserid,i)
        # print(urls_json)
        for urls in urls_json:
            url = urls['singel_url']
            title = urls['v_title']
            title = str(title).replace(' ','')
            file_path_work = urls['file_path_work']
            file_path_name = urls['file_path_name']
            os.chdir(base_path)
            os.chdir(file_path_work)
            os.chdir(file_path_name)
            # print(os.getcwd())

            chips(url,title,v_type='drama')
            print('下一个...')
        print('全部下载完成！')