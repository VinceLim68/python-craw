<?php
//先判断是否有重复的小区名
//取出片区id列表：SELECT region,GROUP_CONCAT( DISTINCT block ) AS NAME ,block_id FROM comm GROUP BY block ORDER BY block_id
//（能保存在一个文件中吗？每次都需要去操作一次数据库，效率低）
// 如果片区存在：
	// 如果区域与现有的一致：
		// 取出block_id;
	// 如果区域与现有的不一致（说明已经把修改了片区所属的区域）：
		// 取出新区域的所有片区
		// 遍历得到一个新的block_id(取出的片区前两位+不存在的编号);
// 如果片区不存在（新片区）：
	// 遍历现有区域所属片区，找到一个新block_id

// 根据block_id,找出新的comm_id

$dir = dirname(__FILE__);
require $dir."./class/DB.php";
header("Content-type:text/html;charset=utf-8");
if(empty($db)){$db = new DB($dbconfig);};
header("Content-Type: text/html; charset=utf-8");

function get_newblockid($region,$arrs){
	//根据指定的region，取出新的id值
	
	//先把指定region的所有block的id取出放到一个数组中去
	$new_blocks_id = array();
	foreach($arrs as $arr){
		if($arr['region'] == $region){
			$new_blocks_id[] = $arr['block_id' ];
		};
	};
	
	//取出block_id的前两位，代表region的id
	$head = substr($new_blocks_id[0],0,2)*100;
	//var_dump($new_blocks_id);
	
	//循环生成新的id
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



$sql = "SELECT region,GROUP_CONCAT( DISTINCT block ) AS NAME ,block_id FROM comm GROUP BY block ORDER BY block_id";
$rows = $db->getResult($sql);
$count = count($rows,0);
//var_dump ($rows);

$add_block = trim($_GET['add_block']);
$add_region = trim($_GET['add_region']);
$add_comm_addr = trim($_GET['add_comm_addr']);
$add_comm_name = trim($_GET['add_comm_name']);
$add_keywords = trim($_GET['add_keywords']);
$add_pri_level = trim($_GET['add_pri_level']);

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
//var_dump($comm_id);
$sql = "insert into comm(comm_name,comm_id,region,block,comm_addr,pri_level,block_id,keywords) values('$add_comm_name','$comm_id','$add_region','$add_block','$add_comm_addr','$add_pri_level','$block_id','$add_keywords')";
echo $sql;

?>