import requests,html,json
from bs4 import BeautifulSoup

#url_3 = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
url_3='https://y.qq.com/n/ryqq/songDetail/002MFDAV3rPFlo'
headers = {
'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    # 标记了请求从什么设备，什么浏览器上发出
    }
params = {
	'g_tk_new_20200303': '534881390',
	'g_tk':'534881390',
    'uin':'3193848589',
	'loginUin':'0',
	'hostUin':'0',
	'format':'json',
	'inCharset':'utf-8',
	'outCharset':'utf-8',
	'notice':'0',
	'platform':'yqq.json',
	'needNewCode':'1',
	# 'cid':'205360772',
	# 'reqtype':'1',
	# 'biztype':'1',
	# 'topid':'330621483',
	# 'cmd':'8',
	# 'needmusiccrit':'0',
	# 'pagenum':'0',
	'pagesize':'25',
	# 'lasthotcommentid':'',	
	# 'domain':'qq.com',
	'ct':'24',
	'cv':'4747474'
}

res_music = requests.get(url_3,headers=headers,params=params)
print('status_code:',res_music.status_code)

# 发起请求
html_content = res_music.json()
print('html_content:',html_content)
# soup = BeautifulSoup(html_content, 'html.parser')


# ul_tags = soup.find('div', class_="main") 
# print('mod_comment', ul_tags.text)
# list_comment = ul_tags.find_all('li',class_="comment__list_item c_b_normal")
# for comment_list in ul_tags:
# 	com_loc = comment_list.find('div',class_="comment__date c_tx_thin")
# 	print('common_location/time:', com_loc.text)
