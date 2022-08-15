from blibili_requests import get_response
import time,os,subprocess

# 省事，音频部分直接复制视频部分代码，有时间再优化
def chips_download(title,v_url,back_v_url,a_url,back_a_url):
    false_times = 0
    while false_times <= 2:
        print(f'正在下载视频：{title}')
        try:
            video_content = get_response(v_url)
            video_size = int(video_content.headers['Content-Length'])
            with open(title + 'v.m4s',mode='wb') as f:
                for i in video_content.iter_content(chunk_size=10240):
                    f.write(i)
            with open(title + 'v.m4s',mode='r') as f:
                real_size = os.fstat(f.fileno()).st_size
                final_persent = f'{int(real_size/video_size*100)} %'
                if video_size == real_size:
                    break
                else:
                    print(f'主链接下载失败\n本应下载大小：{video_size}\n实际下载大小：{real_size}\n完成度：{final_persent}')
                    raise IOError('Data Lost')
        except IOError:
            false_times = false_times+1
            print("将使用备用1下载")
            try:
                video_content = get_response(back_v_url[0])
                with open(title + 'v.m4s',mode='wb') as f:
                    for i in video_content.iter_content(chunk_size=10240):
                        f.write(i)
                with open(title + 'v.m4s',mode='r') as f:
                    real_size = os.fstat(f.fileno()).st_size
                    final_persent = f'{int(real_size/video_size*100)} %'
                    if video_size == real_size:
                        break
                    else:
                        print(f'备用链接1 下载失败\n本应下载大小：{video_size}\n实际下载大小：{real_size}\n完成度：{final_persent}')
                        raise IOError('Data Lost')
            except IOError:
                print('下载失败，将会在3s后重试！')
                time.sleep(3)
                print("将使用备用2下载")
                video_content = get_response(back_v_url[1])
                with open(title + 'v.m4s',mode='wb') as f:
                    for i in video_content.iter_content(chunk_size=10240):
                        f.write(i)
                with open(title + 'v.m4s',mode='r') as f:
                    real_size = os.fstat(f.fileno()).st_size
                    final_persent = f'{int(real_size/video_size*100)} %'
                    if video_size == real_size:
                        break
                    else:
                        print(f'备用链接2 下载失败\n本应下载大小：{video_size}\n实际下载大小：{real_size}\n完成度：{final_persent}')
                        print('当前网络质量差，请换个时间段下载！')
                        return 'failed'
    false_times = 0
    while false_times <= 2:
        print(f'正在下载音频：{title}')
        try:
            video_content = get_response(a_url)
            video_size = int(video_content.headers['Content-Length'])
            with open(title + 'a.m4s',mode='wb') as f:
                for i in video_content.iter_content(chunk_size=10240):
                    f.write(i)
            with open(title + 'a.m4s',mode='r') as f:
                real_size = os.fstat(f.fileno()).st_size
                final_persent = f'{int(real_size/video_size*100)} %'
                if video_size == real_size:
                    break
                else:
                    print(f'主链接下载失败\n本应下载大小：{video_size}\n实际下载大小：{real_size}\n完成度：{final_persent}')
                    raise IOError('Data Lost')
        except IOError:
            false_times = false_times+1
            print("将使用备用1下载")
            try:
                video_content = get_response(back_a_url[0])
                with open(title + 'a.m4s',mode='wb') as f:
                    for i in video_content.iter_content(chunk_size=10240):
                        f.write(i)
                with open(title + 'a.m4s',mode='r') as f:
                    real_size = os.fstat(f.fileno()).st_size
                    final_persent = f'{int(real_size/video_size*100)} %'
                    if video_size == real_size:
                        break
                    else:
                        print(f'备用链接1 下载失败\n本应下载大小：{video_size}\n实际下载大小：{real_size}\n完成度：{final_persent}')
                        raise IOError('Data Lost')
            except IOError:
                print('下载失败，将会在3s后重试！')
                time.sleep(3)
                print("将使用备用2下载")
                video_content = get_response(back_a_url[1])
                with open(title + 'a.m4s',mode='wb') as f:
                    for i in video_content.iter_content(chunk_size=10240):
                        f.write(i)
                with open(title + 'a.m4s',mode='r') as f:
                    real_size = os.fstat(f.fileno()).st_size
                    final_persent = f'{int(real_size/video_size*100)} %'
                    if video_size == real_size:
                        break
                    else:
                        print(f'备用链接2 下载失败\n本应下载大小：{video_size}\n实际下载大小：{real_size}\n完成度：{final_persent}')
                        print('当前网络质量差，请换个时间段下载！')
                        return 'failed'
def chips(url,title,v_type):
    if not os.path.exists(f'{title}.mp4'):
        v_a_url = get_response(url).json()
        if v_type == 'drama':
            v_url = v_a_url['result']['dash']['video'][0]['baseUrl']
            a_url = v_a_url['result']['dash']['audio'][0]['baseUrl']
            back_v_url = v_a_url['result']['dash']['video'][0]['backupUrl']
            back_a_url = v_a_url['result']['dash']['audio'][0]['backupUrl']
            # video_size = v_a_url['result']['dash']['video'][0]['size']
            # audio_size = v_a_url['result']['dash']['audio'][0]['size']
            chips_download(title,v_url,back_v_url,a_url,back_a_url)
            if chips_download == 'failed':
                exit(1)
            print(f'{title} 下载完成！\n 开始合并文件...')
            cmd = f'ffmpeg -i {title}v.m4s -i {title}a.m4s -c:v copy -c:a aac -strict experimental {title}.mp4 -loglevel quiet'
            subprocess.call(cmd,shell=True)
            os.remove(title+'v.m4s')
            os.remove(title+'a.m4s')
            print(f'{title}--完成')