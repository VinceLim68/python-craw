<?php
	$dir = dirname(__FILE__);
	require $dir."./class/DB.php";
	header("Content-type:text/html;charset=utf-8");
	if(empty($db)){$db = new DB($dbconfig);};
	
	$sql="SELECT DISTINCT comm.region FROM comm ";
	$regions = $db->getResult($sql);
	$data = "";					//存放片区数据
	//$regi = "<datalist name='区域'><option value=''></option>";		//存放区域数据
	foreach($regions as $region){
		foreach($region as $key=>$value){
			//$regi .='<option value="'.$value.'">'.$value.'</option>';
			$data .= "<datalist name='".$value."'>";
			$data .= "<option value=''></option>";		//每个区域都需要一个空白选项
			$sql="SELECT DISTINCT comm.block FROM comm WHERE comm.region = '".$value."'";
			$blocks = $db->getResult($sql);
			foreach($blocks as $block){
				foreach($block as $k=>$v){
					$data.='<option value="'.$v.'">'.$v.'</option>';
				};
			};
			$data .= "</datalist> ";
		};
	};
	//$regi .= "</datalist> ";
	//$data = $regi.$data;	
	echo $data; 
?>