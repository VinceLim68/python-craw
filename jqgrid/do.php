<?php
$dir = dirname(__FILE__);

require $dir."./class/DB.php";
header("Content-type:text/html;charset=utf-8");
if(empty($db)){$db = new DB($dbconfig);};

		$page = $_POST['page'];
		$limit = $_POST['rows'];
		$sidx = $_POST['sidx'];
		$sord = $_POST['sord'];

		if (!$sidx)
			$sidx = 1;

        $where = '';
        
        if(!empty($_POST['keywords'])){				
            $keywords = $_POST['keywords'];
			$where .= " and (keywords like '%".$keywords."%' or comm_name like '%".$keywords."%')";
		};
		if(!empty($_POST['region'])){				
            $region = $_POST['region'];
			$where .= " and region like '%".$region."%'";};
		if(!empty($_POST['block'])){
			$block = $_POST['block'];
			$where .= " and block like '%".$block."%'";
		};
		 if(!empty($_POST['address'])){				
            $address = $_POST['address'];
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
	