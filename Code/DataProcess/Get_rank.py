##Description: 抓取排行榜小工具,帮助大家分析排名。初学python，英文不好，望大家体谅
##Author: ericxk(http://weibo.com/u/1445740627/)

import urllib
import urllib2
import json
import csv
from bs4 import BeautifulSoup

cfile=file('./Get_rank.csv','wb')
csvfile=csv.writer(cfile)
csvfile.writerow(['teamName','university','score','precision','recall','date','rank'])
#ali='http://102.alibaba.com/competition/addDiscovery/queryTotalRank.json'
ali='http://tianchi.aliyun.com/competition/rankingList.htm?spm=0.0.0.0.cU1FNp&raceId=1'

def getdata(ali,i):
    postdata=urllib.urlencode({'pageIndex': i})
    res = urllib2.Request(ali,postdata)
    response=urllib2.urlopen(res)
    the_page=response.read()
    return the_page

##the_page都保存了下来，如果大家有自己想查看自己学校的排名或者综合指标，直接读取即可
# the_page={}
# temp=getdata(ali,0)
# print temp
#for i in range(temp['returnValue']['totalPage']):
#	print temp
    #the_page[i+1]=getdata(ali,i+1)
    #for line in the_page[i+1]['returnValue']['datas']:
    #    data=[line['teamName'].encode("GB2312"),line['university'].encode("GB2312"),line['score'],line['precision'],line['recall'],line['dateString'].encode("GB2312"),line['rank']]
    #    csvfile.writerow(data)
# cfile.close()


from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "dl":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    # if variable == "div":
                    self.links.append(value)

if __name__ == "__main__":
    the_page = {}
    html = getdata(ali,0)
    # print temp
    # html_code = """ <a href="www.google.com"> google.com</a> <A Href="www.pythonclub.org"> PythonClub </a> <A HREF = "www.sina.com.cn"> Sina </a> """
    # hp = MyHTMLParser()
    # hp.feed(temp)
    # hp.close()
    # print(hp.links)
    soup = BeautifulSoup(html)
    # body = html.contents[1]
    body = soup.find('body')
    dd = body.findAll('li')[14:]
    # dd = body.findAll('li').find(class='list-item eye-protector-processed')
    cnt = 0
    for element in dd:
        _div = element.findAll('div')
        #队伍排名
        _rank = _div[0].find('p').contents[0].split('\n')[0]
        #队伍名称
        _team_name = _div[1].find('p').contents[0].split('\n')[0]
        _members = _div[1]
        _universiy = _div[2].find('div')
        print _universiy
        # find(attrs={id=True, algin=None})
        # a = _div.find()
        # print _div['']
        # print _div['class']
        cnt += 1
        if _members.contents[1].find('div') != None:
            # print cnt
            member_arr = _members.contents[1].find('div').find('div').contents[0].split('\n')
            # member_arr = member_arr[1: len(member_arr) - 1]
            #队伍人数
            # print len(member_arr) - 2
            # for ele in member_arr:
            #     print ele
            # print _members.contents[1].find('div').find('div').contents[0].split('、')
        # print _div
        # print _team_name
    # print dd
