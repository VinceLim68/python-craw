<?php if (!defined('THINK_PATH')) exit(); /*a:1:{s:67:"C:\wamp64\www\tp5\public/../application/index\view\index\index.html";i:1495974848;}*/ ?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="__CSS__/mycss.css"/>
<title>大叔报价</title>
</head>
<body>
<form action="autovaluate.php" method="post">
	<div class="searchbg" >
		<input type="text" class="inputstyle_out" value="输入小区名搜索" name="fname" onfocus="script:if(this.value=='输入小区名搜索')this.value='';">
		<input type="submit" class="button" value="查房价" >
		<div id="goto"><a href="./comm_manager/index.html" >小区名称管理</a></div>
	</div>
</form>
</body>
</html>