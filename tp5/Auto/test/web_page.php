<?php

 

function web_page($pageurl="", $pageselect = true){

 global $page,$num,$pagenum; //当前页数 总页数 可分页数

 echo "共 $num 条记录，";

 $uppage = $page - 1;  //上一页
 $downpage = $page + 1;  //下一页
 $lr = 5;  //显示多少个页数连接
 $left = floor(($lr-1)/2);  //左显示多少个页数连接
 $right = floor($lr/2);  //右显示多少个页数连接

 //下面求开始页和结束页
 if($page <= $left){  //如果当前页左不足以显示页数
  $leftpage = 1;
  $rightpage = (($lr<$pagenum)?$lr:$pagenum);
 }elseif(($pagenum-$page) < $right){  //如果当前页右不足以显示页数
  $leftpage = (($pagenum<$lr)?1:($pagenum-$lr+1));
  $rightpage = $pagenum;
 }else{  //左右可以显示页数
  $leftpage = $page - $left;
  $rightpage = $page + $right;
 }

 //前$lr页和后$lr页
 $qianpage = (($page-$lr) < 1?1:($page-$lr));
 $houpage = (($page+$lr) > $pagenum?$pagenum:($page+$lr));

 //输出分页
 if($page != 1){
  echo "<a title='首页' href='".$_SERVER['PHP_SELF']."?$pageurl'><<</a> <a title='上一页' href='".$_SERVER['PHP_SELF']."?page=$uppage$pageurl'><</a> ";
 }else{
  echo "<span class='disabled'><<</span><span class='disabled'><</span> ";
 }

 for($pages = $leftpage; $pages <= $rightpage; $pages++){
  if($pages == $page){
   echo "<span class='current'>$pages</span> ";
  }else{
   echo "<a href='?page=$pages$pageurl'>$pages</a> ";
  }
 }

 if($page != $pagenum){
  echo "<a title='下一页' href='".$_SERVER['PHP_SELF']."?page=$downpage$pageurl'>></a> <a title='末页' href='".$_SERVER['PHP_SELF']."?page=$pagenum$pageurl'>>></a>";
 }else{
  echo "<span class='disabled'>></span><span class='disabled'> >></span> ";
 }

 //跳转
 $javapage = <<<EOM
<script language="javascript">
function web_page(targ,selObj,restore){
 eval("self"+".location='"+selObj.options[selObj.selectedIndex].value+"'");
 if (restore) selObj.selectedIndex=0;
}
</script>
EOM;
 echo $javapage;
 if ($pageselect){
	 $str1= "parent";
  echo "跳转至 <select onchange='web_page($str1,this,0)' name='menu1'>";
  for($pages = 1; $pages <= $pagenum; $pages++){
   $selected = ($pages == $page)?" selected='selected'":"";
   echo '<option value="'.$_SERVER['PHP_SELF'].'?page=$pages$pageurl"$selected> $pages</option>';
  }
  echo "</select> 页";
 }

}
?>