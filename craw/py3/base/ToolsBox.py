#coding:utf-8
import traceback
import datetime
import time

def mylog(func):
    def _deco(*a, **b):
        try:
            # result = func(*a,**b) 
            # func(*a,**b)                  #以前只有return,但发现有返回值的函数加装饰器时，总是返回空，所以改成return func(*a,**b)
            return func(*a,**b)
            # return
        except Exception, e:
            # result = None
            with open('logtest.txt','a+') as fout:
                fout.write('\n               *******' + func.__name__ + '*******,error record by @mylog on ' + str(datetime.datetime.now()) + '*************\n')
                traceback.print_exc(file=fout) 
                print(traceback.format_exc())
        # return func
        # return result
    return _deco

def exeTime(func):  
    def newFunc(*args, **args2):  
        t0 = time.time()  
        back = func(*args, **args2)  
        print( "@ %.3fs taken for {%s}\n" % (time.time() - t0, func.__name__)  )
        return back  
    return newFunc 

def pri(string):
    if len(string)%2 != 0:
        string = string + ' '
    print string

def clearStr(string):
    # 清理字符串中的回车、空格等
    string = string.replace('<br/>','').replace('\r','').replace(' ','').replace('\n','').strip()
    string = string.replace(u'\xa0','')             #去除&nbsp;
    return string

def ShowInvalideData(each_data):
    # temp = {}
    if each_data:
        if not each_data.has_key('total_floor'):                    #2016.6.1搜房网老是出现无效数据，进行判断，发现是别墅没有记载楼层信息造成的
            if u"别墅" in each_data['title']:
                each_data['total_floor'] = 4
                each_data['floor_index'] = 1
                each_data['spatial_arrangement'] = each_data['spatial_arrangement'] + u"别墅"
                # page_datas.append(each_data)
                print "没有总楼层,按照别墅填充！！！".encode("gbk")
                for key,value in each_data.items():print(" %s : %s"%(key,value))
                print "="*35
                return True
            else:
                print "！！！没有总楼层！！！".encode("gbk")
        elif not each_data.has_key('total_price'):
            print "！！！没有总价！！！".encode("gbk")
        elif not each_data.has_key('area'):
            print "！！！没有面积！！！".encode("gbk")
        elif not each_data.has_key('community_name'):
            print "！！！小区名！！！".encode("gbk")                 
        # for item in list(house.stripped_strings):print(item)
        # print "-"*25
        # for key,value in each_data.items():print(" %s : %s"%(key,value))
        printDic(each_data)
        print "="*35
    return False

def confir(str):
    for i in range(0,32):
        str = str.replace(chr(i),'')
    return str

def printDic(data):
    if isinstance(data,dict):
        # for key,value in data.items():
        #     print('%20s : %s' %(key,value))
        for key in data:
            print('%20s : %s' %(key,data[key]))
    else:
        print('Not a dict!')