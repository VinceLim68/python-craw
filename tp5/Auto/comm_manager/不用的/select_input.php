<html> 
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> 
</head> 
<body> 
<?php 
echo ' 
<form name="DDForm" method="GET" action=""> 
<div style="position:relative;"> 
<span style="margin-left:100px;width:18px;overflow:hidden;"> 
<select style="width:180px;margin-left:-100px" onchange="this.parentNode.nextSibling.value=this.value" name="hh"> 
<option value="汽车">汽车 </option> 
<option value="火车"> 火车 </option> 
<option value="飞机"> 飞机 </option> 
</select> 
</span><input name="box" style="width:160px;position:absolute;left:0px;"> 
<input value="提交" name="submit" type="submit"/> 
</div> 
</form>'; 
$aa=$_GET['hh']."111"; // select 下拉菜单的值 
$bb=$_GET['box']."222"; // 输入框的值 
echo $aa; 
echo "</br>"; 
echo $bb; 
// 要获得可输入下拉菜单的值，只要获得输入框的值即可。 
?> 
</body> 
</html>