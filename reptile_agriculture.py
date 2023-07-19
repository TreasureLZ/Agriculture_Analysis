import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def getData(zb,zb_code,data):
    millis = int(round(time.time() * 1000))
    url = 'https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22{}%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}'.format(zb_code,millis)
    headers = {
        'Connection': 'keep-alive',
        'Cookie':'wzws_sessionid=oGQ6m6aAMTE5LjM5LjEzMy43N4JmYzVlZTGBMzVkYWQ3; JSESSIONID=CwqE7x_DL8afP48RRS0lnYUSPHymBClZKx0UKJjeYPtWpDSVZW0E!1171792879; u=6',
        'Host':'data.stats.gov.cn',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.get(url=url,headers=headers, verify=False)
    results = response.json()
    unit = results['returndata']['wdnodes'][0]['nodes'][0]['unit']
    area_code = {}
    for item in results['returndata']['wdnodes'][1]['nodes']:
        name = item['cname']
        code = item['code'] 
        area_code[code] = name
    for item in results['returndata']['datanodes']:
        value = item['data']['data']
        area = area_code[item['wds'][1]['valuecode']]
        updateTime = item['wds'][2]['valuecode']
        data.append([area,value,unit,zb,updateTime])
   
def writeData(data):
    with open('./data/data_agriculture.csv','w+',encoding='utf-8') as fp:
        fp.write('\t'.join(['area','value','unit','zb','updateTime'])+'\n')
        for item in data:
            fp.write('\t'.join([str(_) for _ in item])+'\n')
        
if __name__ == '__main__':
    zb_code_list = [{'zb':'夏收粮食产量','zb_code':'A0D0Q02'},{'zb':'秋收粮食产量','zb_code':'A0D0Q02'},{'zb':'夏收粮食播种面积','zb_code':'A0D0P03'},{'zb':'秋收粮食播种面积','zb_code':'A0D0P04'},{'zb':'受灾面积','zb_code':'A0D1801'},{'zb':'有效灌溉面积','zb_code':'A0D0H01'},{'zb':'农用化肥施用折纯量','zb_code':'A0D0H02'}]
    data = []
    for item in zb_code_list:
        zb = item['zb']
        zb_code = item['zb_code']
        getData(zb,zb_code,data)
        print('指标：{}数据采集完成!'.format(zb))
        time.sleep(3)
    writeData(data)