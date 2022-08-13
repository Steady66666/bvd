from blibili_requests import get_response
import time,os,subprocess

def chips_download(title,v_url,back_v_url,a_url,back_a_url):
    while True:
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
            print("将使用备用下载")
            for backurl in back_v_url:
                print(backurl)
                try:
                    video_content = get_response(backurl)
                    with open(title + 'v.m4s',mode='wb') as f:
                        for i in video_content.iter_content(chunk_size=10240):
                            f.write(i)
                    with open(title + 'v.m4s',mode='r') as f:
                        real_size = os.fstat(f.fileno()).st_size
                        final_persent = f'{int(real_size/video_size*100)} %'
                        if video_size == real_size:
                            download_success = True
                            break
                        else:
                            print(f'主链接下载失败\n本应下载大小：{video_size}\n实际下载大小：{real_size}\n完成度：{final_persent}')
                            raise IOError('Data Lost')
                except IOError:
                    print('下载失败，将会在3s后重试！')
                    time.sleep(3)
            if download_success:
                break
    while True:
        print(f'开始下载音频...')
        try:
            video_content = get_response(a_url)
            audio_size = int(video_content.headers['Content-Length'])
            with open(title + 'a.m4s',mode='wb') as f:
                for i in video_content.iter_content(chunk_size=1024):
                    f.write(i)
            with open(title + 'a.m4s',mode='r') as f:
                if audio_size == os.fstat(f.fileno()).st_size:
                    break
                else:
                    print('主链接下载失败')
                    raise IOError('Data Lost')
        except IOError:
            print("将使用备用下载")
            for backurl in back_a_url:
                try:
                    video_content = get_response(backurl)
                    with open(title + 'a.m4s',mode='wb') as f:
                        for i in video_content.iter_content(chunk_size=1024):
                            f.write(i)
                    with open(title + 'a.m4s',mode='r') as f:
                        if audio_size == os.fstat(f.fileno()).st_size:
                            download_success = True
                            break
                        else:
                            raise IOError('Data Lost')
                except IOError:
                    print('下载失败，将会在3s后重试！')
                    time.sleep(3)
            if download_success:
                break

      

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
            print(f'{title} 下载完成！\n 开始合并文件...')
            cmd = f'ffmpeg -i {title}v.m4s -i {title}a.m4s -c:v copy -c:a aac -strict experimental {title}.mp4'
            subprocess.call(cmd,shell=True)
            os.remove(title+'a.m4s')
            os.remove(title+'v.m4s')
            print(f'{title}--完成')

# url = 'https://api.bilibili.com/pgc/player/web/playurl?avid=290463136&cid=335163826&qn=120&fnver=0&fnval=4048&fourk=1&ep_id=400869&session=878a9399a51d444ab0340e9daef15263'
# title = 'test'
# chips(url,title,v_type='drama')