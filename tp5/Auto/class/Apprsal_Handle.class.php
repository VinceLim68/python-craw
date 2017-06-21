<?php
date_default_timezone_set('PRC'); //设置中国时区 
header("Content-type:text/html;charset=utf-8");
// require dirname(__FILE__)."/DBConfig.php";		//引入配置文件

		
class ApprsalHandle{
	// private $mysql_host = 'localhost';//数据库服务器
	// private $mysql_user = 'root'; //数据库用户名
	// private $mysql_pass = 'root'; //数据库密码
	// private $mysql_db = 'apprsal_cdh'; //数据库名
	public $mysqli = null;
		
		//构造函数
	public function __construct($dbconfig){
		$this->mysqli = new mysqli($dbconfig['host'], $dbconfig['user'], $dbconfig['pass'], $dbconfig['db2']);
		if ($this->mysqli->connect_error) {  
			die('Connect Error (' . $this->mysqli->connect_errno . ') '. $this->mysqli->connect_error);  
		}  
		$sql_charset = "SET NAMES ".$dbconfig['charset'];
		$this->mysqli->query($sql_charset);
	}
	
	//查询函数，根据传入sql语句，返回结果集
	public function getResult($sql){
		$res = $this->mysqli->query($sql) or die($this->mysqli->error);
		$res_array = $res->fetch_all(MYSQLI_ASSOC);
		$res->close();
		return $res_array;
	}
	public function getOfferedAndCase($comm){
		 
		$t_dayago = date("Y-m-d", strtotime("-180 day"));			//查询半年内的记录
		// $mysqli = new mysqli($this->mysql_host, $this->mysql_user, $this->mysql_pass, $this->mysql_db);
		$query1 = "SELECT Enquiry_CellName AS Name,PA_Located AS Addr,Apprsal_Use AS Myuse,Apprsal_Up AS Price,Enquiry_Date AS Myday,".
					"PA_Level AS Level,PA_YearBuilt AS Build,PA_Structure AS Stru,PA_Elevator AS Elev,Remark AS Memo,".
					"Enquiry_PmName AS Xjr,OfferPeople AS Offer FROM t_enquiry where Enquiry_CellName like '%".
					$comm."%' and Enquiry_Date > '$t_dayago' order by Myday DESC";
		
		// $result1 = $mysqli->query($query1) or die($mysqli->error);
		// $row1 = $result1->fetch_all(MYSQLI_ASSOC);
		$row1 = self::getResult($query1);
		
		// $result1->close();
		$query2 = "SELECT Case_Name AS Name,Case_Located AS Addr,Case_Type AS Myuse,Case_TrxPrice AS Price,Case_TrxDate AS Myday,".
					"Case_Level AS Level,Case_Cmpl_Years AS Build,Case_Structure AS Stru,Case_Elevator AS Elev ,Opertor AS Offer".
					" FROM t_case_cfg where Case_Name like '%".$comm."%' and Case_TrxDate > '$t_dayago' order by Myday DESC";
		// $result2 = $mysqli->query($query2) or die($mysqli->error); 
		// $row2 = $result2->fetch_all(MYSQLI_ASSOC); 
		$row2 = self::getResult($query2);
		$row1 = array_merge($row1,$row2); 

		// $result2->close();
		// $mysqli->close();
		return $row1;
	}
	
	public function insertQuery($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$t8,$t9,$t10,$t11,$t12,$t13,$t_dayago){
		//往询价表里插入报价记录
		// $mysqli = new mysqli($this->mysql_host, $this->mysql_user, $this->mysql_pass, $this->mysql_db);
		// if ($mysqli->connect_error) {
				// die('Connect Error (' . $mysqli->connect_errno . ') '
					// . $mysqli->connect_error);
			// }
		$sql_count = "SELECT COUNT(Enquiry_CellName) FROM t_enquiry WHERE Enquiry_CellName = '$t0' AND Enquiry_Date > '$t_dayago' AND OfferPeople = '$t11' AND Apprsal_Use = '$t4'";

		if (!$this->mysqli->query($sql_count)){
			die('Error: ' . $this->mysqli->error);
		}
		$res_count = $this->mysqli->query($sql_count);
		$res = $res_count->fetch_all();
		if($res[0][0]>0){
			$suc = 2;
		}else{
			$sql = "insert into t_enquiry (Enquiry_CellName,PA_Located,PA_Level,Apprsal_Use,".
			"Enquiry_PmName,OfferPeople,Apprsal_Up,Enquiry_Source,Remark,Enquiry_Layout,PA_YearBuilt,PA_Structure,".
			"Enquiry_Date,PA_Elevator) values('$t0','$t1','$t6','$t4','$t10','$t11','$t2','$t13','$t3','$t5','$t7','$t9','$t12','$t8')";
			if (!$this->mysqli->query($sql)){
				die('Error: ' . $this->mysqli->error);
			}
			$suc = 1;
		}
		// $this->mysqli->close();
		return $suc;

	}
	
}
?>
