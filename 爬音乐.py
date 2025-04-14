import os
import requests
from tqdm import tqdm
from mutagen.id3 import ID3, USLT
import re

def get_lyrics(song_id):
    try:
        # 获取歌词的API
        lyric_url = f'http://music.163.com/api/song/lyric?os=pc&id={song_id}&lv=-1&kv=-1&tv=-1'
        response = requests.get(lyric_url)
        response.raise_for_status()
        data = response.json()
        
        if 'lrc' in data and 'lyric' in data['lrc']:
            return data['lrc']['lyric']
        return None
    except Exception as e:
        print(f'获取歌词失败: {e}')
        return None

def add_lyrics_to_mp3(file_path, lyrics):
    try:
        # 初始化或加载现有的ID3标签
        try:
            tags = ID3(file_path)
        except:
            tags = ID3()
        
        # 添加歌词
        uslt_output = USLT(encoding=3, lang='chi', desc='', text=lyrics)
        tags['USLT::chi'] = uslt_output
        
        # 保存标签到文件
        tags.save(file_path)
        print('歌词已成功添加到音乐文件')
    except Exception as e:
        print(f'添加歌词失败: {e}')

def download_music(url, save_dir):
    try:
        # 创建保存目录（如果不存在）
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 发送HTTP请求获取音乐文件
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # 从Content-Disposition获取文件名，如果没有则使用默认名称
        filename = '如果.mp3'
        content_length = int(response.headers.get('content-length', 0))
        
        # 构建完整的保存路径
        save_path = os.path.join(save_dir, filename)
        
        # 使用tqdm显示下载进度
        with open(save_path, 'wb') as file, tqdm(
            desc=filename,
            total=content_length,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
        
        print(f'音乐已成功下载到: {save_path}')
        
    except requests.RequestException as e:
        print(f'下载失败: {e}')
    except Exception as e:
        print(f'发生错误: {e}')

# 下载音乐
song_id = '1827591485'
music_url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'
save_directory = r'D:\网易云音乐\CloudMusic（网易云下载的音乐）'

# 下载音乐
download_music(music_url, save_directory)

# 获取歌词并添加到MP3文件
lyrics = get_lyrics(song_id)
if lyrics:
    save_path = os.path.join(save_directory, '如果.mp3')
    add_lyrics_to_mp3(save_path, lyrics)