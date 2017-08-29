#coding:utf-8
from bs4 import BeautifulSoup
# import re
# import datetime
# import traceback
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


class PageParser(object):

    # def __init__(self):
    #     self.r1 = re.compile(r"(\d+\.?\d*)(.*)")             #正则：数字+单位
    #     self.r2 = re.compile(r"(\d+).*")                     #正则：取字符串中的数字

    def parse_urls(self , soup):
        pass

    def parse_datas(self,soup):
        pass

    def is_check(self,soup):
        return False

    def get_soup(self,html,parser_build = 'lxml'):
        # 根据不同的解析器得到soup
        # parser_build:解析器------->html.parser,lxml
        return BeautifulSoup(html,parser_build,from_encoding='urf-8') 

    def parse(self,html_cont,parser_build = 'lxml'):
        # 解析网页的主模块
        soup = slef.get_soup(html_cont,parser_build)

        # soup = BeautifulSoup(html_cont,'lxml',from_encoding='urf-8')        #2016.7.28改用lxml模块解析，否则Q房网解析会有问题
        
        #在这里加上辨识是否有验证码的代码
        if self._ischeck(soup):
            new_urls = raw_input('checkcode!!!  checkcode!!!  \ncheckcode!!!  checkcode!!!\nPlease input how many seconds you want to delay:')
            new_datas = 'checkcode'
        else:
            new_urls = self.parse_urls(soup)
            # 2016.5.30直接从字典里提取数据，不再另外加一个小区名的list
            new_datas = self.parse_datas(soup)
        return new_urls,new_datas
    
    def parse_floor(self,item):
        '''
        高层/(共30层)-->拆成楼层和总层数,        安居客、链家中使用
        传入：        item-->字符串        sep-->分隔符
        '''
        if '(' in unicode(item):
            sep = '('
        elif '/' in unicode(item):
            sep = '/'  
        elif '（' in unicode(item):      #2016.12.1增加全角的（
            sep = '（'    
        else:
            sep = '/'     
        try:

            total_floor = int(filter(str.isdigit,((item.split(sep)[1]) if sep in item else item).encode("utf-8")))
            index = item.split(sep)[0] if sep in item else " "  
            if unicode(index) == u" ":
                floor_index = 0
            elif u"高" in unicode(index):
                floor_index = int(total_floor*5/6)
            elif u"低" in unicode(index):
                floor_index = int(total_floor/6)
            else:
                floor_index = int(total_floor/2)
        except Exception as e:
            with open('logtest.txt','a+') as fout:
                fout.write('\n******' + str(datetime.datetime.now()) + ' *********Erro in parse_floor*************\n')
                fout.write('Parse Failt of :%s \n'%item.encode('utf8'))
                traceback.print_exc(file=fout) 
                print (traceback.format_exc())
        return floor_index,total_floor

    def parse_item(self,string):
        # 2016.8.17增加：传入一个字符串，用正则判断它是面积？户型？单价？楼层？建成年份？优势？解析后返回一个键对值
        try:
            string = string.decode('utf8')
        except:
            string = string

        parse_dict = {}

        r1_1 = '(\d+)平方米'.decode('utf8')
        r1_2 = '(\d+.?\d+)平米'.decode('utf8')        #厦门house的面积是浮点数
        r1_3 = '(\d+.?\d+)㎡'.decode('utf8')         #2016.9.13增加麦田的面积解析
        r1_4 = '(\d+.?\d+)m²'.decode('utf8')        #2017.3.8安居客
        r2_1 = '\d+室'.decode('utf8')
        r2_2 = '\d+房'.decode('utf8')
        r3 = '(\d+)元/'.decode('utf8')
        r4 = '\d+层'.decode('utf8')
        r5_1 = '(\d{4})年'.decode('utf8')
        r5_2 = '年.*(\d{4})'.decode('utf8')


        if re.search(r1_1, string, flags=0):
            parse_dict['area'] = int(re.search(r1_1, string).groups(0)[0])
        elif re.search(r1_2, string, flags=0):
            parse_dict['area'] = int(round(float(re.search(r1_2, string).groups(0)[0]),0))
        elif re.search(r1_3, string, flags=0):                                          #2016.9.13增加麦田的面积解析
            parse_dict['area'] = int(round(float(re.search(r1_3, string).groups(0)[0]),0))
        elif re.search(r1_4, string, flags=0):                                          #2017.3.8安居客的面积解析
            parse_dict['area'] = int(round(float(re.search(r1_4, string).groups(0)[0]),0))
        elif re.search(r2_1, string, flags=0):
            parse_dict['spatial_arrangement'] = string.strip()
        elif re.search(r2_2, string, flags=0):
            parse_dict['spatial_arrangement'] = string.strip()
        elif re.search(r3, string, flags=0):
            pass        #单价准备自己计算，不取值
        elif re.search(r4, string, flags=0):
            parse_dict['floor_index'],parse_dict['total_floor'] = self.parse_floor(string)
        elif re.search(r5_1, string, flags=0):
            parse_dict['builded_year'] = int(re.search(r5_1, string).groups(0)[0])
        elif re.search(r5_2, string, flags=0):
            parse_dict['builded_year'] = int(re.search(r5_2, string).groups(0)[0])
        elif string == '|':
            pass
        else:                           #re.search('[南北东西]', string, flags=0):
            parse_dict['advantage'] = string.strip()
        
        return parse_dict;

    def pipe(self,datadic):
        # 2016.6.4增加方法：清理、有效性检验
        if datadic.has_key('total_floor') and datadic.has_key('total_price') and datadic.has_key('area') and datadic.has_key('community_name'):
            
            if datadic['total_price'] is None or datadic['area'] is None or datadic['community_name'] is None:return False
            if datadic['total_floor'] > 60: datadic['total_floor'] = 35         #把过高楼层的设为35层
            # if datadic['community_name'] is not None:
            datadic['community_name'] = datadic['community_name'].strip()
            if datadic['total_price'] == 0 : return False                       #2016.9.13 价格为0的过滤掉
            
            if datadic.has_key('builded_year'):
                if datadic['builded_year'] < 1900: datadic['builded_year'] = 0
            
            if datadic['area'] > 20000: return False        #面积过大，有时是填写错误，而且面积大于20000的价格参考意义也不大，舍弃
            if not datadic.has_key('price'): return False       #2016.8.1 有时解析过程中出错，跳过了price字段解析，造成没有price,舍弃
            
            #2017.4.14 detail_url字段太长，处理一下
            if len(datadic['details_url']) > 250:datadic['details_url'] = datadic['details_url'][:249]
            
            if len(datadic['advantage']) > 20:datadic['advantage'] = datadic['advantage'][:20]
            return datadic
        else:
            if not datadic.has_key('total_floor'):                    #2016.6.1搜房网老是出现无效数据，进行判断，发现是别墅没有记载楼层信息造成的
                if u"别墅" in datadic['title']:
                    datadic['total_floor'] = 4
                    datadic['floor_index'] = 1
                    datadic['spatial_arrangement'] = datadic['spatial_arrangement'] + u"别墅"
                    return datadic
            return False
        
if __name__=="__main__":

    url = 'http://xm.ganji.comhttp://aozdclick.ganji.com/gjadJump?gjadType=3&target=pZwY0jCfsL6VshI6UhGGshPfUiqhmyOMPitzPWDvn1E1nHDYXaOCIAYhuj6-n176mhNVuAm1niYYP1FhsH91rjnVP1I6nAcYuHnvPynzFWDkPjmQPHDOPWchnHEOnH03rj9zPW9vPH93FWcvnHm1PjnQnHEhP1utsgkVFWItnW7tsgkVFW0LPjmQmWmLsH9QnvEVPj6BnaY3rjmQsyELP1DLnAP6rymQuamQPjbznjmYn1mzP1DdFhIJUA-1IZGbFWDh0A7zmyYhnau8IyQ_FWEhnHDLsWcOsWDvnz3QPjchUMR_UamQFhOdUAkhUMR_UT&end=end'
    print(len(url) )


    # str2 = ’0123456789′
    # print str[0:3] #截取第一位到第三位的字符
    # parser = HtmlParser()
    # # str1 ='4层2008年建'
    # str1 = '中楼层(共10层)2006年建塔楼'
    # if ')' not in str1:
    # #     split = ')'
    # # else:
    #     str1 = str1.replace('层', '层)')
    #     print str1
    #     # index = str1.index() + 1
    #     # # str1 = str1(0:index)
    #     # print str1[0:index]+')'+str1[index:]+' '

    # # str1 ='4层'
    # # a = (parser.parse_item(str1))
    # for item in str1.split(')'):     #2017.4.1链家格式有改
    # # for i in range(0,len(position)-2):
    #     d1 = {}
    #     # d1 = self.parse_item(position[i].strip())
    #     d1 = parser.parse_item(item.strip())          #2017.4.1链家格式有改
    #     print(d1)
        # each_data = dict(each_data, **d1)
    # print a



