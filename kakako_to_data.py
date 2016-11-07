# -*- coding: utf-8 -*-
import re #정규표현
import codecs #코덱
import datetime; import time; import csv
import json

class File_to_data:
    def __init__(self,fname):
        #원래 txt 자체는 ascii 파일이라  다시 바꿔주는 작업.
        f = codecs.open(fname, encoding = 'utf-8')
        data = f.read()
        date_list,url_list,content_list,num_data = getDataSeperateDateContent(data)
        self.content_list = write_json(date_list,url_list,content_list,num_data)

    def get_dict_list(self):
        return self.content_list
    def save_dict_list(self):
        print("현재 디렉토리로 저장됩니다.")
        print("파일 이름을 입력하세요.")
        fname = input()
        fname += ".json"
        save(self.content_list,fname)
        print("저장완료.")

    
def  getDataSeperateDateContent(data):
    #정규식 이용/하나에 너무 많아서 객체로(compile)로 반환하는게 좋
    #n = data.find(u'회원')#u changes from krean to unicode
    #https://wikidocs.net/4308(정규식 대략 설명)
    #http://kwonnam.pe.kr/wiki/python/unicode(정규식 unicode URL)
    reg_ex = re.compile(u'201[ 가-힣a-zA-Z0-9\:\,]+회원님 : ')
    #p = re.compile(unicode(r'201[ 가-힣a-zA-Z0-9\:\,]+회원님','utf-8'), re.UNICODE)
    reg_matchs = reg_ex.finditer(data)
    
    #list 일단 읽기
    date_index = []
    for each_match in reg_matchs:
        one_date_index = each_match.span()#span is the re fucntion that return the start and the end.
        #print(one_date_index)
        date_index.append(one_date_index)
        
    #날짜 입력
    date_list = []
    for i in range(len(date_index)):
        date = ""
        for j in range(date_index[i][0],date_index[i][1]-2):#delet ' :"
            date = date + data[j]
        date_list.append(date)

    #날짜 정제
    for i in range(len(date_index)):
        year =  date_list[i][0:4]
        index = date_list[i].index(u'월')
        month = date_list[i][index-2:index] if date_list[i][index-2].isdigit() else date_list[i][index-1]
        index = date_list[i].index(u'일')
        day = date_list[i][index-2:index] if date_list[i][index-2].isdigit() else date_list[i][index-1]

        index = date_list[i].index(':')
        hour = date_list[i][index-2:index] if date_list[i][index-2].isdigit() else date_list[i][index-1]
        hour = int(hour) + 12 if date_list[i].find(u'후') else int(hour) #morning/afternoon
        if hour ==24: hour = 0 #there is no 24 in timestamp
        
        index2 = date_list[i].index(',')
        minute = date_list[i][index+1 : index2]

        time_stamp = datetime.datetime(int(year),int(month),int(day),hour,int(minute))
        date_list[i] = time_stamp.strftime('%Y-%m-%d %H:%M')
        
    #내용 입력
    content_list = []
    for i in range(len(date_index)-1):
        content = ""
        last_content = ""
        if i == len(date_index)-2:
            for j in range(date_index[i][1],date_index[i+1][0]):
                content = content + data[j]
            for j in range(date_index[i+1][1],len(data)):
                last_content = last_content + data[j]
            content_list.append(content)
            content_list.append(last_content)
        else:
            for j in range(date_index[i][1],date_index[i+1][0]):
                content = content + data[j]
            content_list.append(content)
    #print (len(date_index))
    
    #내용 정제
    #(http|https):\/\/(([\xA1-\xFEa-z0-9_\-]+\.[\xA1-\xFEa-z0-9:;&#@=_~%\?\/\.\,\+\-]+))
    url_reg_ex = re.compile(u'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    date_reg_ex = re.compile(u'201[ 가-힣a-zA-Z0-9\:\,]+')
    url_list = []
    for i in range(len(date_index)):
        #DELETE useless sentence
        content_list[i] = content_list[i].replace('\r\n','') #\r\n 
        date_sentence = reg_matchs = date_reg_ex.findall(content_list[i]) #date sentence
        if len(date_sentence) == 1: content_list[i] = content_list[i].replace(date_sentence[0],'')
        
        #extract URL
        url_reg_matchs = url_reg_ex.findall(content_list[i])
        url_list.append(url_reg_matchs)
    return (date_list,url_list,content_list,len(date_index))


def write_json(date_list,url_list,content_list,num):
    contents_list = []

    for i in range(num):
        dic = {}
        dic['content_names'] = i
        dic['content_dates'] = date_list[i]
        dic['content_link'] = url_list[i]
        dic['content_coms'] = content_list[i]
        #print(dic)
        contents_list.append(dic)

    print("DONE")
    return contents_list


def save(data,fname):
    with open(fname, 'w') as f:
         json.dump(data, f)


#deprecated
def write_csv(date_list,url_list,content_list,num):
    with open('data %s.csv' % date_list[num-1][0:date_list[num-1].index(' ')],'w') as file:#wb는 byte로 읽음
        w = csv.writer(file)
        w.writerow(['content_names','content_dates','content_link','content_coms'])
    for i in range(num):
        w.writerow([i,date_list[i],url_list[i],content_list[i].encode('euc-kr','replace')])




