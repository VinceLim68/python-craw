import MassController,XmhousePage

url=['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html']
MC = MassController.MassController(XmhousePage.XmhousePage)
MC.craw_controller(url)

