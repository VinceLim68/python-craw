<?php 
date_default_timezone_set('PRC'); //设置中国时区 
header("Content-type:text/html;charset=utf-8");
define('ROOT_PATH',dirname(__FILE__));
require_once ROOT_PATH.'/class/apprsal_Handle.class.php';
require_once ROOT_PATH.'/class/DBConfig.php';
//require_once ROOT_PATH.'/class/Arr_Handler.class.php';
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
$t12 = date('Y-m-d H:i:s');
$t13 = $_POST["offer_class"];
$t_dayago = date("Y-m-d", strtotime("-30 day"));

$AH = new ApprsalHandle($dbconfig);
$succ = $AH->insertQuery($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$t8,$t9,$t10,$t11,$t12,$t13,$t_dayago);
if($succ == 2){
	header("Location: index.php?show=7&success=2"); 
}elseif($succ == 1){
	header("Location: index.php?show=7&success=1"); 
}


?>