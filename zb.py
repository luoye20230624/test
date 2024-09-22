import requests
import re
import base64
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Fofa API 配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

urls = ["Hunan"]
channelsx = [
    "湖南卫视,http://8.8.8.8:8/udp/239.76.245.115:1234",
    "湖南经视,http://8.8.8.8:8/udp/239.76.245.116:1234",
    "湖南都市,http://8.8.8.8:8/udp/239.76.245.117:1234",
    "湖南电视剧,http://8.8.8.8:8/udp/239.76.245.118:1234",
    # 省略其他频道以节省空间
]

def query_fofa(region):
    results = []
    urls_all = []

    for url in urls:
        url_0 = str(base64.b64encode((f'"udpxy" && region="{url}" && org="Chinanet"').encode("utf-8")), "utf-8")
        url_64 = f'https://fofa.info/result?qbase64={url_0}'
        logging.info(f"查询网址: {url_64}")

        try:
            response = requests.get(url_64, headers=headers, timeout=15)
            response.raise_for_status()
            logging.info(f"{url} 访问成功")

            pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
            page_urls = re.findall(pattern, response.text)
            for urlx in page_urls:
                try:
                    response = requests.get(url=urlx + '/stat', timeout=1)
                    response.raise_for_status()
                    page_content = response.text
                    if 'connections online' in page_content:
                        urls_all.append(urlx)
                        logging.info(f"{urlx} 可以访问")
                except requests.RequestException:
                    continue
        except requests.RequestException:
            logging.error(f"{url_64} 访问失败")
            continue

    urls_all = set(urls_all)  # 去重得到唯一的URL列表
    for urlx in urls_all:
        channel = [f'{name},{url.replace("http://8.8.8.8:8", urlx)}' for name, url in
                   [line.strip().split(',') for line in channelsx]]
        results.extend(channel)

    results = sorted(results)
    return results

def check_download_speed(ip_list):
    speeds = []

    for ip in ip_list:
        start_time = time.time()
        try:
            response = requests.get(f"{ip}/stat", timeout=5)
            response.raise_for_status()
            elapsed_time = time.time() - start_time
            # 速度计算
            speed = 1 / elapsed_time if elapsed_time > 0 else 0
            speeds.append((ip, speed))
            logging.info(f"{ip} 下载速度: {speed:.2f} MB/s")
        except requests.RequestException:
            logging.error(f"{ip} 下载失败")
            continue

    # 根据速度排序，选取前三个最快的
    speeds.sort(key=lambda x: x[1], reverse=True)
    return speeds[:3]

def save_to_playlist(all_channels):
    with open('播放列表.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")  # M3U 文件头
        for name, url in all_channels:
            f.write(f"#EXTINF:-1,{name}\n{url}\n")
    logging.info("所有频道已保存至播放列表文件：播放列表.m3u")

if __name__ == "__main__":
    channels = query_fofa("Hunan")
    if channels:
        logging.info("开始检测下载速度...")
        fastest_ips = check_download_speed([url.split(',')[1] for url in channels])
        
        # 将所有频道写入播放列表
        save_to_playlist(channels)
    else:
        logging.warning("没有找到可用的频道。")
