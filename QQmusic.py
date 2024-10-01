import requests,html,json
from bs4 import BeautifulSoup
import csv
# url_1 = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'

# i = input('请输入需要查询歌词的歌曲名称：')
# i = '泡沫'
# url_1 = f"https://y.qq.com/n/ryqq/search?w={i}&t=song&remoteplace=txt.yqq.center"
# url_1 = 'https://y.qq.com/n/ryqq/toplist/26'

# 美国热歌榜
# url_1 = 'https://y.qq.com/n/ryqq/toplist/108'

# youtube热歌榜
# url_1 = 'https://y.qq.com/n/ryqq/toplist/128'

# 英国热歌榜
# url_1 = 'https://y.qq.com/n/ryqq/toplist/107'

# 韩国热歌榜
# url_1 = 'https://y.qq.com/n/ryqq/toplist/129'

# 日本热歌榜
url_1 = 'https://y.qq.com/n/ryqq/toplist/105'

headers = {
'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
    # 标记了请求从什么设备，什么浏览器上发出
    }

# params = {'ct': '24', 'qqmusic_ver': '1298', 'new_json': '1', 'remoteplace': 'txt.yqq.song', 'searchid': '71600317520820180', 't': '0', 'aggr': '1', 'cr': '1', 'catZhida': '1', 'lossless': '0', 'flag_qc': '0', 'p': '1', 'n': '10', 'w': i, 'g_tk': '5381', 'loginUin': '0', 'hostUin': '0', 'format': 'json', 'inCharset': 'utf8', 'outCharset': 'utf-8', 'notice': '0', 'platform': 'yqq.json', 'needNewCode': '0'}
params = {
  "cv": "4747474",
  "ct": "24",
  "format": "json",
  "inCharset": "utf-8",
  "outCharset": "utf-8",
  "notice": "0",
  "platform": "yqq.json",
  "needNewCode": "1",
  "uin": "3193848589",
  # "g_tk_new_20200303": "236888301",
  'g_tk_new_20200303':'5381',
  "g_tk" : "5381",
  # "cid": "205360410",
  # "reqtype": "1",
  # "from": "2"
  "ck": "MusicJsonCallback"

}


res_music = requests.get(url_1,headers=headers,params=params)
print('status_code:',res_music.status_code)
html_content = res_music.text
soup = BeautifulSoup(html_content, 'html.parser')

from bs4 import BeautifulSoup

# Assuming 'soup' is your BeautifulSoup object, initialized with some HTML content
ul_tags = soup.find('ul', class_="songlist__list")  # Attempt to find the first 'ul' with the specified class

if ul_tags is not None:  # Check if an 'ul' tag was actually found
    li_tags = ul_tags.find_all('li')  # Find all 'li' tags within the found 'ul'
    songs = []
    for li in li_tags:
        song_rank = li.find('div', class_="songlist__number").text
        print('song_rank:', song_rank)
        link= li.find('span', class_='songlist__songname_txt')
        song_name= link.text
        a_tags = link.find_all('a')
        for a in a_tags:
          if 'songDetail' in a['href']:
              song_link='https://y.qq.com'+a['href']
        songs.append({
            'song_rank': song_rank,
            'song_name': song_name,
            'song_link': song_link
        })
        
# Specify the CSV file name
csv_file = 'QQ_日本热歌榜.csv'

# Save the data to a CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['song_rank', 'song_name', 'song_link'])
    writer.writeheader()
    writer.writerows(songs)

print(f"Data saved to {csv_file}")