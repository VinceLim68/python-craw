import MassController,WbPage

class WB(MassController.MassController):
    def __init__(self, parseClass):
        super(WB, self).__init__(parseClass)
        self.comm_count = 1                         #计数：抓取小区的数量

    def CommsController(self,url):
        self.craw_controller(url)
        while self.comms.has_new_url():
            comm = self.comms.get_new_url()
            c1,c2 = self.comms.get_quantity()
            comm_url = "http://xm.58.com/ershoufang/?key=" + (comm)
            print('*******{0}/{1}:{2}*********'.format(self.comm_count,c1+c2,comm))
            url_list = []
            url_list.append(comm_url)
            self.craw_controller(url_list)
            self.comm_count += 1

        self.total = self.total + self.outputer.out_mysql()

if __name__=="__main__":
    url = ['http://xm.58.com/ershoufang/pn2/']
    wb = WB(WbPage.WbPage)
    wb.CommsController(url)
