<?php 
header("Content-type:text/html;charset=utf-8");
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
<title></title> 
<style type="text/css"> 

.tableBox{ height:200px; width:800px; position:relative; overflow-x:auto; overflow-y:hidden;table-layout:fixed; } 
.tablehead{ position:absolute; width:800px; left:0;} 
.tablebody{ position:absolute; width:800px; height:200px; overflow-y:auto; overflow-x:hidden; top:20px; left:0;} 
td{ width:88px;white-space:normal;} 
table{border-collapse: collapse; border-spacing: 0;margin-left: 5px;margin-right: 5px;table-layout:fixed;} 
</style> 
</head> 
<body> 

<div class="tableBox" > 
<div class="tablehead"> 
<table border="1px"> 
<tr> 
<td>姓名</td><td>性别</td><td>年龄</td> 
</tr> 
</table> 
</div> 
<div class="tablebody"> 
<table class="body" border="1px" > 
<tr><td>小明的地地道道的地地道道的</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
<tr><td>小明</td><td>男</td><td>12</td></tr> 
</table> 

</div> 
</div> 
</body> 
</html> 

<!--其中有有三个div，最外侧一个，控制全局，一个控制表头，一个控制表身。有以下几点注意： 
td{ width:88px;white-space:normal;} 
table{border-collapse: collapse; border-spacing: 0;margin-left: 5px;margin-right: 5px;table-layout:fixed;} 

1.最外侧的div，需要用overflow-x来控制最横向滚动，因为overflow-x、y在IE中存在兼容性问题，
当overflow-x/overflow-y其中之一被设置成'scroll'、'auto'、'hidden'时，另一个还是'visible'，不会被设置为'auto' 
所以，最好使用 "overflow-x:scroll; overflow-y:auto",这时候，右边的在需要时才会显示。
如果希望右边的滚动条一直不显示，那么，可以使用："overflow-x:scroll; overflow-y:hidden;" 

2.表头和表体的各列需要对齐，所以可以用table-layout:fixed;来固定宽度 

3.当用table-layout:fixed;固定了列宽度，也就会有长的内容会显示不全，那么可以用white-space:normal;来进行换行-->