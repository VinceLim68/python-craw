<?php
$dir = dirname(__FILE__);
require $dir."./class/DB.php";
header("Content-type:text/html;charset=utf-8");
if(empty($db)){$db = new DB($dbconfig);};
header("Content-Type: text/html; charset=utf-8");
//$action = $_GET['action'];

function get_newblockid($region,$arrs){
	/*根据指定的region，取出新的id值*/
	//1、先把指定region的所有block的id取出放到一个数组中去
	$new_blocks_id = array();
	foreach($arrs as $arr){
		if($arr['region'] == $region){
			$new_blocks_id[] = $arr['block_id' ];
		};
	};
	//2、取出block_id的前两位，代表region的id
	$head = substr($new_blocks_id[0],0,2)*100;
	//var_dump($new_blocks_id);
	//3、循环生成新的id
	$i = 1;
	while(1){
		$newid = $head + $i;		//$head+后两位，待验证是否未被使用
		if(!in_array($newid,$new_blocks_id) ){
			break;			//如果没被占用，则返回，这就是新的block_id
		};
		++ $i ;
	};
	return $newid;
};

function get_newcommkid($block_id,$arrs){
	/*根据block_id生成新的comm_id,$arrs是传入的从数据库中查询的含block_id的记录*/
	//先把指定block的所有comm的id取出放到一个数组中去
	$new_comms_id = array();
	foreach($arrs as $arr){
		$new_comms_id[] = $arr['comm_id' ];
	};
	
	//循环生成新的id
	$i = 1;
	while(1){
		$newid = $block_id*1000 + $i;		//$head+后两位，待验证是否未被使用
		if(!in_array($newid,$new_comms_id) ){
			break;			//如果没被占用，则返回，这就是新的block_id
		};
		++ $i ;
	};
	return $newid;
};


/*先可将数据库中是否已经有重复的小区名称了*/
$where = '';
if(!empty($_GET['add_comm_name'])){				
	$add_comm_name = trim($_GET['add_comm_name']);
	$where .= " and (keywords like '%".$add_comm_name."%' or comm_name like '%".$add_comm_name."%')";
};
$sql="SELECT * FROM comm where 1=1".$where;
$rows = $db->getResult($sql);
$count = count($rows,0);
	

if ($count > 0) {		//发现小区名已经存在
	$outputs = array();  
	$cells = array();  
	$outputs['total']= 1;						 
	$outputs['page'] = 1 ;						
	$outputs['records'] = $count;    
	foreach($rows as $row){
		$cells[]=array('ID'=>$row['Id'],
						'cell'=>array(
							$row['Id'],
							$row['comm_name'],
							$row['region'],
							$row['block'],
							$row['comm_id'],
							$row['block_id'],
							$row['keywords'],
							$row['comm_addr'],
							$row['pri_level']));
	}
	$outputs['rows'] = $cells;  
	echo json_encode($outputs); 
	// echo '3';
} else {		//小区名称是新的，开始添加
	//先把数据赋值过来
	$add_block = trim($_GET['add_block']);
	$add_region = trim($_GET['add_region']);
	$add_comm_addr = trim($_GET['add_comm_addr']);
	//$add_comm_name = trim($_GET['add_comm_name']);		//前面已经赋值了
	$add_keywords = trim($_GET['add_keywords']);
	$add_pri_level = trim($_GET['add_pri_level']);
	
	//查询出一个”区域-片区-block_id“的数组
	$sql = "SELECT region,GROUP_CONCAT( DISTINCT block ) AS NAME ,block_id FROM comm GROUP BY block ORDER BY block_id";
	$rows = $db->getResult($sql);
	//$count = count($rows,0);
	//var_dump ($rows);
	// $add_region = "漳州";
	// $add_block = "龙池";

	//查找片区是否存在
	$block_exit = False;
	foreach($rows as $row){
		if($add_block == $row['NAME'] ){
			$block_exit = True;
			//var_dump($row);
			break;
		};
	}


	if($block_exit){		//如果片区存在
		//检查区域与片区是否同时存在，
		$block_id = "";
		$region_block_exit = False;
		foreach($rows as $row){
			 if($add_block == $row['NAME'] &&  $add_region == $row['region']){
				 $region_block_exit = True;
				 $block_id = $row['block_id'];		//如果存在返回block_id
				 //var_dump($row);
				 break;
			 };
		};
		if(!$region_block_exit){		//如果虽然存在block,但与现有的region不一致
			$block_id = get_newblockid($add_region,$rows);
			/*最好在这里加入把所有数据库里的小区id按新生成的block_id修改*/
		};
	}else{		//如果片区不存在，需要生成一个新block_id
		$block_id = get_newblockid($add_region,$rows);
	};

	//var_dump($block_id);
	//根据指定的block，取出新的comm_id值
	$sql = "SELECT comm_id FROM comm WHERE block_id= ".$block_id;
	$arrs = $db->getResult($sql);
	//var_dump($arrs);

	$comm_id = get_newcommkid($block_id,$arrs);
	$sql = "insert into comm(comm_name,comm_id,region,block,comm_addr,pri_level,block_id,keywords) values('$add_comm_name','$comm_id','$add_region','$add_block','$add_comm_addr','$add_pri_level','$block_id','$add_keywords')";
	$rows = $db->getResult($sql);
	echo $rows;
	
	
}


?>