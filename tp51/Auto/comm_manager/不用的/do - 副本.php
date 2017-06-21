<?php
// $dir = dirname(__FILE__);
// require $dir."./class/DB.php";
// header("Content-type:text/html;charset=utf-8");
// if(empty($db)){$db = new DB($dbconfig);};
$host = "localhost";
$db_user = "root";
$db_pass = "root";
$db_name = "property_info";
$timezone = "Asia/Shanghai";

$mysqli = new mysqli($host, $db_user, $db_pass,$db_name);

/* check connection */
if ($mysqli->connect_errno) {
    printf("Connect failed: %s\n", $mysqli->connect_error);
    exit();
}

$mysqli->query("SET names UTF8");
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
        
        if(!empty($_GET['title'])){				//$title
            $title = uniDecode($_GET['title'],'utf-8');
			$where .= " and title like '%".$title."%'";};
        
        if(!empty($sn)){
			$sn = uniDecode($_GET['sn'],'utf-8');
			$where .= " and sn='$sn'";
		};
        
		// $sql="SELECT COUNT(*) AS count FROM comm where 1=1".$where;
		// $rows = $db->getResult($sql);
		// $count = $rows['count'];
			// $regi = "";
			// foreach($regions as $region){
				// foreach($region as $key=>$value){
					//$regi.='<option>'.$value.'</option>';
					// $regi.='<option value="'.$value.'">'.$value.'</option>';
				// };
			// };		
		$result = $mysqli->query("SELECT COUNT(*) AS count FROM comm where 1=1".$where);
		$row = $result->fetch_assoc();
		$count = $row['count'];


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
		$result = $mysqli->query($SQL);
		
		$outputs = array();  
		$cells = array();  
		$outputs['total']= $total_pages;						//round(count($params['summany'])/$_POST['rows']);  
		$outputs['page'] = $page ;						//$_POST['page'];  
		$outputs['records'] = $count;     //count($params['summany']);  
		//while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
		while ($row = $result->fetch_assoc()) {
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
		$result->close();
		echo json_encode($outputs);  
		break;
	case 'add' : //新增
		$pro_title = htmlspecialchars(stripslashes(trim($_POST['pro_title'])));
		$pro_sn = htmlspecialchars(stripslashes(trim($_POST['pro_sn'])));
		$size = htmlspecialchars(stripslashes(trim($_POST['size'])));
		$os = htmlspecialchars(stripslashes(trim($_POST['os'])));
		$charge = htmlspecialchars(stripslashes(trim($_POST['charge'])));
		$price = htmlspecialchars(stripslashes(trim($_POST['price'])));
		if (mb_strlen($pro_title) < 1)
			die("产品名称不能为空");
		$addtime = date('Y-m-d H:i:s');
		$query = mysql_query("insert into products(sn,title,size,os,charge,price,addtime)values('$pro_sn','$pro_title','$size','$os','$charge','$price','$addtime')");
		if (mysql_affected_rows($link) != 1) {
			die("操作失败");
		} else {
			echo '1';
		}

		break;
	case 'edi' : //编辑
		$block = trim($_GET['block']);
		$block_id = trim($_GET['block_id']);
		$comm_addr = trim($_GET['comm_addr']);
		$comm_id = trim($_GET['comm_id']);
		$comm_name = trim($_GET['comm_name']);
		$id = trim($_GET['id']);
		$keywords = trim($_GET['keywords']);
		$pri_level = trim($_GET['pri_level']);
		$region = trim($_GET['region']);
		
	case 'del' : //删除
		$ids = $_POST['ids'];
		delAllSelect($ids, $link);
		break;
	case '' :
		echo 'Bad request.';
		break;
}

//批量删除操作
function delAllSelect($ids, $link) {
	if (empty ($ids))
		die("0");
	mysql_query("update products set deleted=1 where id in($ids)");
	if (mysql_affected_rows($link)) {
		echo $ids;
	} else {
		die("0");
	}
}

//处理接收jqGrid提交查询的中文字符串
function uniDecode($str, $charcode) {
	$text = preg_replace_callback("/%u[0-9A-Za-z]{4}/", toUtf8, $str);
	return mb_convert_encoding($text, $charcode, 'utf-8');
}
function toUtf8($ar) {
	foreach ($ar as $val) {
		$val = intval(substr($val, 2), 16);
		if ($val < 0x7F) { // 0000-007F
			$c .= chr($val);
		}
		elseif ($val < 0x800) { // 0080-0800
			$c .= chr(0xC0 | ($val / 64));
			$c .= chr(0x80 | ($val % 64));
		} else { // 0800-FFFF
			$c .= chr(0xE0 | (($val / 64) / 64));
			$c .= chr(0x80 | (($val / 64) % 64));
			$c .= chr(0x80 | ($val % 64));
		}
	}
	return $c;
}
?>