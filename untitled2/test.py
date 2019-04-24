from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from pymongo import MongoClient
import time
import random
import re

def get_one_page(page, ip_list):
    url = "https://wh.lianjia.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36',
        'Host': 'wh.lianjia.com',
        'Referer': 'https://www.lianjia.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    newUrl = url + 'ershoufang/' + 'pg' + str(page)+'/co52'
    tag=1
    proxy_ip = random.choice(ip_list)
    ip = {'https:':proxy_ip} # proxy ip needed for requests
    try:
        response = requests.get(newUrl, headers=headers, proxies=ip,timeout=2)
        soup = BeautifulSoup(response.text, 'html.parser')
    except RequestException as e:
        tag=0
        print("error: 网络超时" )

    #soup = BeautifulSoup(response.text, 'html.parser')

    #  需要抓取： 小区名称， 面积大小， 均价， 以及详细信息的链接
    result = []
    if tag==1:
        for item in soup.select('li .clear'):
            detailed_info = item.select('div .houseInfo')[0].text
            community_name = detailed_info.split('|')[0].strip() #房屋楼盘名
            #area = re.findall('(\d+(\.\d+)?)',detailed_info.split('|')[2].strip())[0][0]  #去除多余汉字，用于之后的数据分析
            average_price = re.findall('(\d+(\.\d+)?)',item.select('div .unitPrice span')[0].text)[0][0] #房价
            detailed_url = item.select('a')[0].get('href')          #房屋详细链接

            try:
                inner_page=requests.get(detailed_url, headers=headers, proxies=ip,timeout=4)
            except RequestException as e:
                tag=0
                print("error: 内部网络超时")                                #进入详细连接获取详细信息
            if tag==1:
                txt=BeautifulSoup(inner_page.text, 'html.parser')
                info=txt.select('div.base div.content li')
                house_type=info[0].text[4:].strip()                                         #房屋类型
                floor=info[1].text[4:].strip()                                              #楼层信息
                building_area=info[2].text.strip()                                          #建筑面积
                building_area=re.sub(r'[^\x00-\x7F]+',"",building_area)           #去除中文方便数据处理
                try:
                    structure=info[3].text[4:].strip()                                          #户型结构
                    house_area=info[4].text[4:].strip()                                         #套内面积
                    #house_area=re.sub(r'[^\x00-\x7F]+',"",house_area)
                    building_type=info[5].text[4:].strip()                                      #建筑类型
                    house_orientation=info[6].text[4:].strip()                                  #房屋朝向
                    building_structure=info[7].text[4:].strip()                                 #建筑结构
                    renovation=info[8].text[4:].strip()                                         #装修情况

                    scale=info[9].text[4:].strip()                                              #梯户比例
                    elevator= info[10].text[4:].strip()                                          #配备电梯
                    age_limit=info[11].text[4:].strip()                                          #产权年限
                except Exception as e:
                    structure='暂无数据'
                    house_area='暂无数据'
                    building_type='暂无数据'
                    house_orientation='暂无数据'
                    building_structure='暂无数据'
                    renovation='暂无数据'
                    scale='暂无数据'
                    elevator='暂无数据'
                    age_limit='暂无数据'
                    print('暂无数据')

                infoo=txt.select('div.transaction div.content li')                      #另一个标签组合查询
                list_time=infoo[0].text[6:].strip()                                         #挂牌时间
                business=infoo[1].text[6:].strip()                                           #交易权属
                last_deal=infoo[2].text[6:].strip()                                         #上次交易
                house_using=infoo[3].text[6:].strip()                                       #房屋用途
                house_life=infoo[4].text[6:].strip()                                        #房屋年限
                ownship=infoo[5].text[6:].strip()                                           #产权所属
                mortgage_info=infoo[6].text[6:43].strip()                                     #抵押信息
                house_sparepart=infoo[7].text[6:].strip()                                   #房本备件

                area=txt.select('div.areaName a')[0].text                                  #房屋所在地区，进行区域分析

                #print(list_time,business,last_deal,house_using,house_life,ownship,mortgage_info,house_sparepart)
                print(community_name,area,average_price,house_type,floor,building_area,structure,house_area,building_type,
                      house_orientation,building_structure,renovation,scale,elevator,age_limit,list_time,business,last_deal,
                      house_using,house_life,ownship,mortgage_info,house_sparepart,detailed_url)

                '''
                house_type=detailed_info.split('|')[1].strip()                 #房屋类型
                floor=item.select('div.positionInfo')[0].text.split('-')[0]
                position=item.select('div.positionInfo')[0].text.split('-')[1]
                House_orientation=detailed_info.split('|')[3]
                Renovation=detailed_info.split('|')[4]
                if len(detailed_info.split('|'))<6 or detailed_info.split('|')[5]=='无电梯':
                    elevator = '无电梯'
                else :
                    elevator=detailed_info.split('|')[5]
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(community_name, area, average_price, house_type ,
                floor,position,House_orientation,Renovation,elevator,detailed_url))
                '''

                result.append({'小区名称':community_name, '所在区域':area, '平均价格(元/平方)':average_price, '房屋类型':house_type, '所在楼层':floor, '建筑面积':building_area,'户型结构':structure,
                               '套内面积':house_area,'建筑类型':building_type,'房屋朝向':house_orientation,'建筑结构':building_structure,'装修情况':renovation ,'梯户比例':scale ,'配备电梯':elevator,
                               '产权年限':age_limit,'挂牌时间':list_time,'交易权属':business,'上次交易时间':last_deal,'房屋用途':house_using,'房屋年限':house_life,'产权所属':ownship,
                               '抵押信息':mortgage_info, '房本备件':house_sparepart,'详细信息链接':detailed_url})
            else:
                tag=1

                result.append({'小区名称':'','所在区域':'','平均价格(元/平方)':'','房屋类型':'','建筑面积':''})
    else:
        tag=1
        strr="无"
        result.append({'小区名称':'','所在区域':'','平均价格(元/平方)':'','房屋类型':'','建筑面积':''})
    return result


def read_ip():
    result = []
    with open('ip.txt', 'r', encoding='gb18030', newline='') as f:
        for line in f:
            result.append('http://'+line)
        return result

def store_in_db(result):
    conn = MongoClient('localhost', 27017)
    db = conn.test  # db name is test
    #my_set = db.text_set  # set type
    my_set = db.wuhan_watchmost
    my_set.insert(result)


def getdata(page, ip_list):

    for i in range(1,page):
        result = get_one_page(i, ip_list)
        store_in_db(result)
        print('data storgae from page '+str(i)+'complete!')
        if i >= 10 and i % 10 == 0:
            time.sleep(30)


def main(page):
    ip_list = read_ip() #读取文档中的ip
    getdata(page, ip_list)
    #get_one_page(47,ip_list)



if __name__ == '__main__':
    main(100)
