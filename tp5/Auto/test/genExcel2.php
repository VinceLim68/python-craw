<?php
	//date_default_timezone_set('PRC'); //设置中国时区 
	//header("Content-type:text/html;charset=utf-8");
	session_start();
	$comm = $_SESSION['dataResult']['comm'];
	if($comm == ""){		//如果没有小区名称，直接返回
		header("Location: index.php?show=5&succ=2"); 
		exit();
	}
	define('ROOT_PATH',dirname(__FILE__));
	require_once ROOT_PATH.'/class/Excel.class.php';
	require_once ROOT_PATH.'/class/Data_Handler.class.php';
	
	$mydata = new Data_Handler;
	
	$res_array = $mydata->getDataFromDatabase($comm);
	$filename = $comm.date('YmdHis',time()).'.xls';
	//$filename = $comm.date('YmdHis',time()).'.xlsx';
	header("Content-type:application/vnd.ms-excel");
	header("Content-Disposition:attachment;filename=$filename");
	echo "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
			<html xmlns='http://www.w3.org/1999/xhtml'>
			<head>
			<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
			<title>林晓生成excel</title>
			<style>
			td{
				text-align:center;
				font-size:12px;
				font-family:Arial, Helvetica, sans-serif;
				border:#1C7A80 1px solid;
				color:#152122;
				width:100px;
			}
			table,tr{
				border-style:none;
			}
			.title{
				background:#7DDCF0;
				color:#FFFFFF;
				font-weight:bold;
			}
			</style>
			</head>";
	
	echo "<body>
			<table  border='1'>
			  <tr>
				<td class='title'>摘要</td>
				<td class='title'>小区</td>
				<td class='title'>单价</td>
				<td class='title'>面积</td>
				<td class='title'>总价</td>
				<td class='title'>户型</td>
				<td class='title'>楼层</td>
				<td class='title'>总层</td>
				<td class='title'>建成年份</td>
				<td class='title'>其他优势</td>
				<td class='title'>链接</td>
			  </tr>";
	
	foreach($res_array as $row){
		echo "<tr>";
		foreach($row as $col){
			echo "<td>".$col."</td>";
		}
		//echo "<td><a href='".$col."'></a></td>"
		echo "</tr>";
	}
	
	echo "</table>
			</body>
			</html>";
		
	//header("Content-type:text/html;charset=utf-8");
	header("Location: index.php?show=5&succ=1"); 
	
	
	
?>