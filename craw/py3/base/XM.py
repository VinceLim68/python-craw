import MassController,XmhousePage,LejvPage,GanjiPage,MaitianPage

url=['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html']
XM = MassController.MassController(XmhousePage.XmhousePage)
XM.craw_controller(url)
XM.outputer.out_mysql()

url = ['http://xm.esf.leju.com/house']
LEJV = MassController.MassController(LejvPage.LejvPage)
LEJV.delay = 3
LEJV.headers = dict(Host="xm.esf.leju.com", Origin="http://xm.esf.leju.com", Referer="http://xm.esf.leju.com/house/")
LEJV.craw_controller(url)
LEJV.outputer.out_mysql()

url = ['http://xm.ganji.com/fang5/o2/']
GJ = MassController.MassController(GanjiPage.GanjiPage)
GJ.delay = 3
GJ.headers = dict(Host="xm.ganji.com",  Referer="http://xm.ganji.com/fang5/o2/")
GJ.craw_controller(url)
GJ.outputer.out_mysql()

url = ['http://xm.maitian.cn/esfall/PG2']
MT = MassController.MassController(MaitianPage.MaitianPage)
MT.headers = dict(Host="xm.maitian.cn")
MT.craw_controller(url)
MT.outputer.out_mysql()