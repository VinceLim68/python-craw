<?php 
header("Content-type:text/html;charset=utf-8");
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>google分页</title>
<meta name="keywords" content="仿google php分页程序 " />
<meta name="description" content="仿google php分页程序" />
<style type="text/css">
<!--
body { font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; padding: 0px; }
div { height: auto; width: 800px; margin: 10px auto; line-height:20px; }

/*CSS manu style pagination*/

.manu {
 PADDING-RIGHT: 3px; PADDING-LEFT: 3px; PADDING-BOTTOM: 3px; MARGIN: 3px; PADDING-TOP: 3px; TEXT-ALIGN: center
}
.manu A {
 BORDER-RIGHT: #eee 1px solid; PADDING-RIGHT: 5px; BORDER-TOP: #eee 1px solid; PADDING-LEFT: 5px; PADDING-BOTTOM: 2px; MARGIN: 2px; BORDER-LEFT: #eee 1px solid; COLOR: #036cb4; PADDING-TOP: 2px; BORDER-BOTTOM: #eee 1px solid; TEXT-DECORATION: none
}
.manu A:hover {
 BORDER-RIGHT: #999 1px solid; BORDER-TOP: #999 1px solid; BORDER-LEFT: #999 1px solid; COLOR: #666; BORDER-BOTTOM: #999 1px solid
}
.manu A:active {
 BORDER-RIGHT: #999 1px solid; BORDER-TOP: #999 1px solid; BORDER-LEFT: #999 1px solid; COLOR: #666; BORDER-BOTTOM: #999 1px solid
}
.manu .current {
 BORDER-RIGHT: #036cb4 1px solid; PADDING-RIGHT: 5px; BORDER-TOP: #036cb4 1px solid; PADDING-LEFT: 5px; FONT-WEIGHT: bold; PADDING-BOTTOM: 2px; MARGIN: 2px; BORDER-LEFT: #036cb4 1px solid; COLOR: #fff; PADDING-TOP: 2px; BORDER-BOTTOM: #036cb4 1px solid; BACKGROUND-COLOR: #036cb4
}
.manu .disabled {
 BORDER-RIGHT: #eee 1px solid; PADDING-RIGHT: 5px; BORDER-TOP: #eee 1px solid; PADDING-LEFT: 5px; PADDING-BOTTOM: 2px; MARGIN: 2px; BORDER-LEFT: #eee 1px solid; COLOR: #ddd; PADDING-TOP: 2px; BORDER-BOTTOM: #eee 1px solid;
}

-->
</style>
</head>

<body>
<?php

require('web_page.php'); //包含分页程序


//数据库配置
$mysql_host = 'localhost'; //数据库服务器
$mysql_user = 'root'; //数据库用户名
$mysql_pass = ''; //数据库密码
$mysql_db = 'property_info'; //数据库名


//连接mysql数据库
$mysqli = new mysqli($mysql_host,$mysql_user,$mysql_pass,$mysql_db);
// $link = mysql_connect($mysql_host,$mysql_user,$mysql_pass) or die ('连接MYSQL服务器出错');
  // mysql_select_db($mysql_db,$link) or die ('连接MYSQL数据库出错');


//分页开始

//$sql_page = "SELECT * FROM for_sale_property";
$sql_page = "SELECT COUNT(*) AS totalrows FROM for_sale_property";
$sql = $mysqli->query($sql_page) or die($mysqli->error);

$row1 = $sql->fetch_assoc();
$num = $row1['totalrows'];  //
//$num = $sql->num_rows;  //总条数
$max =20;  //每页条数
$pagenum = ceil($num/$max);  //可分页数
if(!isset($_GET['page']) or !intval($_GET['page']) or !is_numeric($_GET['page']) or $_GET['page'] > $pagenum){
 $page = 1; //当页数不存在 不为十进制数 不是数字 大于可分页数 为1
}else{
 $page = $_GET['page'];  //当前页数
}
$min = ($page-1)*$max;  //当前页从$min条开始

$sql = "SELECT * FROM for_sale_property limit $min,$max";


echo '<div>';
if($num){
 $sql =  $mysqli->query($sql);
 for(;$row = $sql->fetch_array();){
  echo '<li><a href="show.php?id='.$row['id'].'">'.$row['title'].'</a></li>';
 }
}else{
 echo '<li>暂无</li>';
}
echo '</div>';

//mysql_free_result($sql); //释放资源

?>

<div class="manu"><?php web_page(""); //调用输出分页,引用你的页面其他参数 如：web_page("&class=2&news=6") ?></div>

<?php
//分页结束
$mysqli->close();
//mysql_close();
?>

</body>
</html>