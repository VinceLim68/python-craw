<?php
$mysqli = new mysqli('localhost', 'root', '', 'property_info');
header("Content-type:text/html;charset=utf-8");
$maxnum = 50;  //每页记录条数
$query1 = "SELECT COUNT(*) AS totalrows FROM for_sale_property ";

$result1 = $mysqli->query($query1) or die($mysqli->error);
$row1 = $result1->fetch_assoc();
$totalRows1 = $row1['totalrows'];  //数据集总条数
$totalpages = ceil($totalRows1/$maxnum);//分页总数
if(!isset($_GET['page']) || !intval($_GET['page']) || $_GET['page'] > $totalpages) $page = 1;  //对3种出错进行处理 
//在url参数page不存在时，page不为10进制数时，page大于可分页数时，默认为1 
else $page = $_GET['page']; 
$startnum = ($page - 1)*$maxnum; //从数据集第$startnum条开始读取记录，这里的数据集是从0开始的 
$query = "SELECT * FROM for_sale_property LIMIT $startnum,$maxnum";//选择出符合要求的数据 从$startnum条数据开始，选出$maxnum行 
$result = $mysqli->query($query) or die($mysqli->error); 
$row = $result->fetch_assoc(); 
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=uft-8">
<title>分页示例</title>
<script language="JavaScript" type="text/JavaScript">
<!--
function MM_jumpMenu(targ,selObj,restore){ //v3.0
  eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'");
  if (restore) selObj.selectedIndex=0;
}
//-->
</script>
<style type="text/css">
a{text-decoration:none;}
a:hover{text-decoration:underline}
table{font-size:12px;}
.tb{background-color:#73BB95}
.tr{background-color:#FFFFFF}
.scrolldiv{height:200px;overflow-y:scroll;
}
</style>
</head>
<body>
<div class="scrolldiv">

<table width="90%"  border="0" align="center" cellpadding="0" cellspacing="1" class="tb">
  <tr>
    <td height="24"><div align="left">id</div></td>
	<td height="24"><div align="left">概述</div></td>
	<td height="24"><div align="left">单价</div></td>
  </tr>
  <?php if($totalRows1) {//记录集不为空显示
  do {
  ?>
  <tr class="tr">
    <td height="24"><div align="center"><?php echo $row['id'];?></div></td>
	<td height="24"><div align="center"><?php echo $row['title'];?></div></td>
	<td height="24"><div align="center"><?php echo $row['price'];?></div></td>
  </tr>
  <?php }while($row = $result->fetch_assoc());?>
</table>
</div>
<table width="95%"  border="0" align="center" cellpadding="10" cellspacing="0">
  <tr><form name="form1">
    
	<td height="27" align="center">
	
        <?php
         echo "共计<font color=\"#ff0000\">$totalRows1</font>条记录";
         echo "<font color=\"#ff0000\">".$page."</font>"."/".$totalpages."页 ";
        //实现 << < 1 2 3 4 5> >> 样式的分页链接<div >
        $pre = $page - 1;//上一页
        $next = $page + 1;//下一页
        $maxpages = 4;//处理分页时 << < 1 2 3 4 > >>显示4页
        $pagepre = 1;//如果当前页面是4，还要显示前$pagepre页，如<< < 3 /4/ 5 6 > >> 把第3页显示出来
        if($page != 1) { 
			echo "<a href='".$_SERVER['PHP_SELF']."'><<</a> ";
			echo "<a href='".$_SERVER['PHP_SELF'].'?page='.$pre."'><</a> ";
		}
        if($maxpages>=$totalpages){ //如果总记录不足以显示4页
			$pgstart = 1;$pgend = $totalpages;//就不所以的页面打印处理
        }elseif(($page-$pagepre-1+$maxpages)>$totalpages){//就好像总页数是6，当前是5，则要把之前的3 4页显示出来，而不仅仅是4
			$pgstart = $totalpages - $maxpages + 1;$pgend = $totalpages;
        }else{
			$pgstart=(($page<=$pagepre)?1:($page-$pagepre));//当前页面是1时，只会是1 2 3 4 > >>而不会是 0 1 2 3 > >>
			$pgend=(($pgstart==1)?$maxpages:($pgstart+$maxpages-1));
        }
        for($pg=$pgstart;$pg<=$pgend;$pg++){ //跳转菜单
			if($pg == $page){
				echo "<a href=\"".$_SERVER['PHP_SELF']."?page=$pg\"><font color=\"#ff0000\">$pg</font></a> ";
			} 
			else {
				echo "<a href=\"".$_SERVER['PHP_SELF']."?page=$pg\">$pg</a> ";
			} 
        }
        if($page != $totalpages){
			echo "<a href='".$_SERVER['PHP_SELF'].'?page='.$next."'>></a> ";
			echo "<a href='".$_SERVER['PHP_SELF'].'?page='.$totalpages."'>>></a> ";
			}
        ?>
		<select name="menu1" onChange="MM_jumpMenu('parent',this,0)">
			<option value="">选择</option>
			<?php for($pg1=1;$pg1<=$totalpages;$pg1++) {
				echo "<option value=\"".$_SERVER['PHP_SELF']."?page=$pg1\">".$pg1."</option>";
			}?>
		</select>
	
    </td></form>
  </tr>
</table>
<?php } else {//记录集为空时显示?>
<table>
	<tr class="tr">
		<td height="24"><div align="center">没有任何记录</div></td>
	</tr>
</table>
<?php }?>

</body>
</html>
<?php
$result1->free_result();
$result->free_result();
//mysql_free_result($result);
?>