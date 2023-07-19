import requests
from bs4 import BeautifulSoup
headers = {
    'Host': 'www.tianqihoubao.com',
    'Cookie':'__bid_n=1878575f93aae937d14207; FPTOKEN=Jz+CYvXOSXF6FcPjWSSYCsaw5NBfrRkaEE+9BmEmS/jTR7nhA1F905G+MiECTiGDA10970eSZX4OAA18yzQe8lxb8TbVwclfwlJUfKt0/mb6P7BNXIXdlYhQpRDNXXTFXGJoIjtYvD2sWIYx2B6tBHxzkOGZWkh6KJsjVIAo2Y0YLx8xcayqsCvMpuMDi2OIIj3pOh8z5YdB1+AsruPDZCjT8zQ++gX2mSxka9B8FqBlrRmEFeBPqHvxrAnazPwALLy81Sik0VeFMnmjpQsLXGI4sD0TrZFgS/G0kKfx1tFtkG+zpqfbLanLyMkAZia2SWZqA8mlQiOeNM7Oi5hh8gOg4nT2Q8hcr5QAhrlqR9Mko2arko1pa7csLH3RZS1fkltGNCQqjRTZdIwwI4Blog==|hiN2LZK89/f4k+s27BotOOicQyzL8s7hG44mpvHwR78=|10|5c6d79e2131cb244b35ab6c4c697c8c1; Hm_lvt_f48cedd6a69101030e93d4ef60f48fd0=1681571314; __gads=ID=cb101988ea567ad5-2253ddbf2cdf00c8:T=1681571314:RT=1681571314:S=ALNI_MYA6qRyhWyL5sICMMFHZYDtVHhOlA; __gpi=UID=00000bf4d3146c9e:T=1681571314:RT=1681571314:S=ALNI_MaoQ-kiq8bdZXEXprAzBTj07qmlOA; Hm_lpvt_f48cedd6a69101030e93d4ef60f48fd0=1681574861',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}
def getURL():
    url = 'http://www.tianqihoubao.com/qihou/'
    response = requests.get(url=url,headers=headers)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text,'lxml')
    li_list = soup.select('div#content div.box ul li')
    city_href = {}
    for li in li_list:
        href = 'http://www.tianqihoubao.com' + li.select('a')[0].get('href')
        city = li.select('a')[0].text
        city_href[city] = href
    return city_href

def getData(city,href,data):
    url = href 
    response = requests.get(url=url,headers=headers)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text,'lxml')
    tr_list = soup.select('div.qihou table tr')
    for tr in tr_list[1:]:
        month = tr.select('td')[0].text
        avg_max_temperature = tr.select('td')[1].text
        avg_min_temperature = tr.select('td')[2].text
        avg_precipitation = tr.select('td')[3].text
        histroy_max_temperature = tr.select('td')[4].text
        histroy_min_temperature = tr.select('td')[5].text
        data.append([city,month,avg_max_temperature,avg_min_temperature,avg_precipitation,histroy_max_temperature,histroy_min_temperature])

def whiteData(data):
    with open('./data/data_meteorology.csv','w+',encoding='utf-8') as fp:
        fp.write('\t'.join(['city','month','avg_max_temperature','avg_min_temperature','avg_precipitation','histroy_max_temperature','histroy_min_temperature'])+'\n')
        for item in data:
            fp.write('\t'.join([str(_) for _ in item])+'\n')

if __name__ == '__main__':
    city_href = getURL()
    # city_href = {'阿巴嘎旗':'http://www.tianqihoubao.com/qihou/abagaqi.htm'}
    page = 0
    data = []
    for city in city_href:
        href = city_href[city]
        page += 1
        getData(city,href,data)
        print("城市：{}的气象数据采集成功！".format(city))
        # time.sleep(3)
    whiteData(data)