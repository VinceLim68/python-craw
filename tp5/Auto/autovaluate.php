<?php
	session_start();
	header("Content-type:text/html;charset=utf-8");
	define('ROOT_PATH',dirname(__FILE__));
	//require_once ROOT_PATH.'/class/Arr_Handler.class.php';
	require_once ROOT_PATH.'/class/Data_Handler.class.php';
	require_once ROOT_PATH.'/class/Data_View.class.php';
	require_once ROOT_PATH.'/class/DBConfig.php';
	$mydata = new Data_Handler($dbconfig);
	$comm = trim($_POST["fname"]);
	$res_array = $mydata->getDataFromDatabase($comm);
	echo count($res_array);
	if(count($res_array) <= 1 ){
		//echo "1111";
		header("Location: index.php?show=0&fname=".$comm); 
		exit();
	}
	$var1 = $mydata->getResultOfAnalyse($res_array);
	
	$var1['comm'] = $comm;
	//$_SESSION['dataResult'] = $var1;
	$_SESSION['dataResult'] = $var1;  
	$_SESSION['flag'] = 1;
	
	$dv = new DataView;
	$var2 = $mydata->getValidFullArr($res_array);
	$var3=$mydata->getColumn($var2, 'price');
	$histo = $dv->getHistogramArray($var3,30);
	$_SESSION['histo'] = $histo; 
	header("Location: index.php?show=6"); 
	
