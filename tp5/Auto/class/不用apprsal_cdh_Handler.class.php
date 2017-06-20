<?php 
date_default_timezone_set('PRC'); //设置中国时区 
header("Content-type:text/html;charset=utf-8");
$t0 = $_POST["t_comm"];
$t1 = $_POST["t_add"];
$t2 = $_POST["t_collateral_value"];
$t3 = $_POST["t_memo"];
$t4 = $_POST["t_usage"];
$t5 = $_POST["t_avg_total_floor"];
$t6 = $_POST["t_avg_floor_index"];
$t7 = date('Y-m-d',strtotime($_POST["t_avg_builded_year"]));;
$t8 = $_POST["t_elevator"];
$t9 = $_POST["t_structure"];
$t10 = $_POST["t_xjr"];
$t11 = $_POST["t_offer"];
$t12 = date('Y-m-d',strtotime($_POST["t_offerday"]));
$t13 = $_POST["offer_class"];
$t_dayago = date("Y-m-d", strtotime("-30 day"));

/*foreach($t as $item){
	echo $item.'<br/>';
}*/	

$mysqli = new mysqli('localhost', 'root', 'root', 'apprsal_cdh');
if ($mysqli->connect_error) {
		die('Connect Error (' . $mysqli->connect_errno . ') '
            . $mysqli->connect_error);
	}
$sql_count = "SELECT COUNT(Enquiry_CellName) FROM t_enquiry WHERE Enquiry_CellName = '$t0' AND Enquiry_Date > '$t_dayago' AND OfferPeople = '$t11'";
//$sql_count = "SELECT COUNT(Enquiry_CellName) FROM t_enquiry WHERE Enquiry_CellName = '$t0' ";
//$sql_count = "select * from t_enquiry where Enquiry_CellName = '$t0'";
if (!$mysqli->query($sql_count)){
	die('Error: ' . $mysqli->error);
}
$res_count = $mysqli->query($sql_count);
$res = $res_count->fetch_all();
if($res[0][0]>0){
	echo '<script language="JavaScript">;alert("这是";location.href="index.htm";</script>;';
}else{
	$sql = "insert into t_enquiry (Enquiry_CellName,PA_Located,PA_Level,Apprsal_Use,".
	"Enquiry_PmName,OfferPeople,Apprsal_Up,Enquiry_Source,Remark,Enquiry_Layout,PA_YearBuilt,PA_Structure,".
	"Enquiry_Date,PA_Elevator) values('$t0','$t1','$t6','$t4','$t10','$t11','$t2','$t13','$t3','$t5','$t7','$t9','$t12','$t8')";
	if (!$mysqli->query($sql)){
		die('Error: ' . $mysqli->error);
}
}


$mysqli->close();

/*	foreach($res_count as $item){
	print_r($item);
	echo "<br/>";
}		

echo "添加一条记录";
//关闭连接
$mysqli->close();
*/
/*
$sql = "select * from t_enquiry where Enquiry_CellName like '%".$t_comm."%'";
$res = $mysqli->query($sql);
$res_arrays = $res->fetch_all(MYSQLI_ASSOC);
$res->close();
$mysqli->close();
foreach ($res_arrays as $item){
	print_r($item);
	echo "<br/>";
	}  	*/
?>