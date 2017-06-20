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
//$action = $_GET['action'];

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
} else {
	$total_pages = 0;
}


?>