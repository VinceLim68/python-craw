<?php
	//���±�д�������ļ������ݿ�����ļ����Ա����ά��
	require dirname(__FILE__)."/DBConfig.php";		//���������ļ�
	class DB{
		public $mysqli = null;
		
		//���캯��
		public function __construct($dbconfig){
			$this->mysqli = new mysqli($dbconfig['host'], $dbconfig['user'], $dbconfig['pass'], $dbconfig['db']);
			if ($this->mysqli->connect_error) {  
				die('Connect Error (' . $this->mysqli->connect_errno . ') '. $this->mysqli->connect_error);  
			}  
			$this->mysqli->query("SET names ".$dbconfig['charset']);
		}
		
		//��ѯ���������ݴ���sql��䣬���ؽ����(��ѯ)�����߽��(��ɾ��)
		public function getResult($sql){
			$res = $this->mysqli->query($sql) or die($this->mysqli->error);
			if(gettype($res)=="boolean"){
				//$res->close();
				if(!$res){
					return 0; //��ɾ��ʧ��
				}else{
					if($this->mysqli->affected_rows>0){
						return 1;//��ʾ�ɹ�
					}
					else{
						return 2;//��ʾû��Ӱ������
					}
				}
			}else{
				$res_array = $res->fetch_all(MYSQLI_ASSOC);
				$res->close();
				return $res_array;		//������һ����ά����
			}
		}
		
		//����С������comm��ѯ����
		public function getDataByComm($comm){
			$sql = "select title,community_name,price,area,total_price,spatial_arrangement,floor_index,total_floor,builded_year,advantage,".
				"details_url FROM for_sale_property AS a JOIN (SELECT id FROM for_sale_property FORCE INDEX".
				" (date_index) ORDER BY first_acquisition_time DESC LIMIT 0,300000) AS b WHERE a.id=b.id AND a.community_name like '%".$comm."%'";
			$res = self::getResult($sql);
			return $res;
		}
		
		//�ر����ݿ�
		public function closeDB(){
			$this->mysqli->close();
		}
	}
?>