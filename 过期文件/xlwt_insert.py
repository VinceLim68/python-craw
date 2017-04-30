#coding:utf-8
import xlwt;
import xlrd;
from xlutils.copy import copy;
  
#styleBoldRed   = xlwt.easyxf('font: color-index red, bold on');
#headerStyle = styleBoldRed;
#wb = xlwt.Workbook();
#ws = wb.add_sheet('sheetName');
#ws.write(0, 0, "Col1",        headerStyle);
#ws.write(0, 1, "Col2", headerStyle);
#ws.write(0, 2, "Col3",    headerStyle);
#wb.save('fileName.xls');
 
#open existed xls file
oldWb = xlrd.open_workbook('lands.xls', formatting_info=True);
oldWbS = oldWb.sheet_by_index(0)
newWb = copy(oldWb);			#复制旧表所有记录
newWs = newWb.get_sheet(0);
inserRowNo = 1					#在第几行插入
newWs.write(inserRowNo, 0, "value11");
newWs.write(inserRowNo, 1, "value12");
newWs.write(inserRowNo, 2, "value13");
 
for rowIndex in range(inserRowNo, oldWbS.nrows):	#插入行以下的记录重新写一遍，oldWbS.nrows旧文档的总行数
    for colIndex in range(oldWbS.ncols):			#oldWbS.ncols旧文档的总列数
        newWs.write(rowIndex + 1, colIndex, oldWbS.cell(rowIndex, colIndex).value);
newWb.save('lands.xls');
print "save with same name ok";