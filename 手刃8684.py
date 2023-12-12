import requests
import re
import csv

url = 'https://wuhan.8684.cn/x_24f5dad9'
headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
responses = requests.get(url = url,headers = headers)

pagecontent = responses.text

#解析数据
obj = re.compile(r'<li>.*?aria-label=".*?"(?P<bus>.*?)</a>',re.S)
#开始匹配
result = obj.finditer(pagecontent)
f = open('data.csv',mode='w')
csvwriter = csv.writer(f)
for it in result:

    dic = it.groupdict("bus")
    csvwriter.writerow(dic.values())
 #print(it.group("bus"))
    #dic = it.groupdict()
#dic["year"] = dic['year'].strip()
    #csvwriter.writerow(dic.values())
#responses.close()'''