<?php
	$dir = dirname(__FILE__);
	require $dir."./class/DB.php";
	header("Content-type:text/html;charset=utf-8");
	if(empty($db)){$db = new DB($dbconfig);};
	$where = '';
	//$sql="SELECT COUNT(*) AS count FROM comm where 1=1".$where;
	//$sql="UPDATE comm SET comm_addr='000' WHERE Id=4455";
	$sql = "SELECT distinct block FROM comm WHERE region = '思明'";
	$rows = $db->getResult($sql);
	
	print_r($rows);
	//print(gettype($rows)=="boolean");
	//print($rows[0]['count'] );
	
	
	
?>