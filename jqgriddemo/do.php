<?php
$dir = dirname(__FILE__);
require $dir."./class/DB.php";
header("Content-type:text/html;charset=utf-8");
if(empty($db)){$db = new DB($dbconfig);};


header("Content-Type: text/html; charset=utf-8");
$action = $_GET['action'];

switch ($action) {
	case 'list' : //列表
		$page = $_GET['page'];
		$limit = $_GET['rows'];
		$sidx = $_GET['sidx'];
		$sord = $_GET['sord'];

		if (!$sidx)
			$sidx = 1;

        $where = '';
        
        if(!empty($_GET['keywords'])){				
            $keywords = $_GET['keywords'];
			$where .= " and (keywords like '%".$keywords."%' or comm_name like '%".$keywords."%')";
		};
		if(!empty($_GET['region'])){				
            $region = $_GET['region'];
			$where .= " and region like '%".$region."%'";};
		if(!empty($_GET['block'])){
			$block = $_GET['block'];
			$where .= " and block like '%".$block."%'";
		};
		 if(!empty($_GET['address'])){				
            $address = $_GET['address'];
			$where .= " and comm_addr like '%".$address."%'";};

        
		$sql="SELECT COUNT(*) AS count FROM comm where 1=1".$where;
		//print($sql);
		$rows = $db->getResult($sql);
		$count = $rows[0]['count'];
			

		if ($count > 0) {
			$total_pages = ceil($count / $limit);
		} else {
			$total_pages = 0;
		}
		if ($page > $total_pages)
			$page = $total_pages;
		$start = $limit * $page - $limit;
		if ($start<0) $start = 0;
		
		$SQL = "SELECT * FROM comm WHERE 1=1 ".$where." ORDER BY $sidx $sord LIMIT $start , $limit";
		$rows = $db->getResult($SQL);

		$outputs = array();  
		$cells = array();  
		$outputs['total']= $total_pages;						 
		$outputs['page'] = $page ;						
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
		//$result->close();
		echo json_encode($outputs);  
		break;
	case 'edi' : //编辑
		$id = trim($_GET['id']);
		$comm_id = trim($_GET['comm_id']);
		$sql="SELECT COUNT(*) AS count FROM comm where comm_id=$comm_id";
		$rows = $db->getResult($sql);
		$count = $rows[0]['count'];
		if($count>1){
			echo "该id已被使用，修改失败";
			break;
		};
		$block = trim($_GET['block']);
		$block_id = trim($_GET['block_id']);
		$comm_addr = trim($_GET['comm_addr']);
		
		$comm_name = trim($_GET['comm_name']);
		
		$keywords = trim($_GET['keywords']);
		$pri_level = trim($_GET['pri_level']);
		$region = trim($_GET['region']);
		$sql = "UPDATE comm SET comm_addr='".$comm_addr."',block='".$block."',block_id='".$block_id."',comm_id='".$comm_id.
				"',comm_name='".$comm_name."',keywords='".$keywords."',pri_level='".$pri_level."',region='".$region."' WHERE Id=$id";
		$rows = $db->getResult($sql);
		echo $rows;
		break;
	case 'del' : //删除
		$id = trim($_GET['id']);
		$sql = "delete from comm where Id= $id";
		$rows = $db->getResult($sql);
		echo $rows;
		break;
	case '' :
		echo 'Bad request.';
		break;
}

//批量删除操作
// function delAllSelect($ids, $link) {
	// if (empty ($ids))
		// die("0");
	// mysql_query("update products set deleted=1 where id in($ids)");
	// if (mysql_affected_rows($link)) {
		// echo $ids;
	// } else {
		// die("0");
	// }
// }

// //处理接收jqGrid提交查询的中文字符串
// function uniDecode($str, $charcode) {
	// $text = preg_replace_callback("/%u[0-9A-Za-z]{4}/", toUtf8, $str);
	// return mb_convert_encoding($text, $charcode, 'utf-8');
// }
// function toUtf8($ar) {
	// $c = "";
	// foreach ($ar as $val) {
		// $val = intval(substr($val, 2), 16);
		// if ($val < 0x7F) { // 0000-007F
			// $c .= chr($val);
		// }
		// elseif ($val < 0x800) { // 0080-0800
			// $c .= chr(0xC0 | ($val / 64));
			// $c .= chr(0x80 | ($val % 64));
		// } else { // 0800-FFFF
			// $c .= chr(0xE0 | (($val / 64) / 64));
			// $c .= chr(0x80 | (($val / 64) % 64));
			// $c .= chr(0x80 | ($val % 64));
		// }
	// }
	// return $c;
// }
?>