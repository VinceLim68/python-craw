<?php
	require_once 'Arr_Handler.class.php';
	// require dirname(__FILE__)."/DBConfig.php";		//引入配置文件
	class Data_Handler extends Arr_Handler{
		// private $mysql_host = 'localhost';//数据库服务器
		// private $mysql_user = 'root'; //数据库用户名
		// private $mysql_pass = 'root'; //数据库密码
		// private $mysql_db = 'property_info'; //数据库名
		public $mysqli = null;
		
		//构造函数
		public function __construct($dbconfig){
			$this->mysqli = new mysqli($dbconfig['host'], $dbconfig['user'], $dbconfig['pass'], $dbconfig['db']);
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
		
		
		function assessRisk(){
			/*风险评价函数*/
			
		}
		function getDataFromDatabase($comm){
			/*从数据库里查询出数据*/
			// $mysqli = new mysqli($this->mysql_host, $this->mysql_user, $this->mysql_pass, $this->mysql_db);
			// if ($mysqli->connect_error) {
				// die('Connect Error (' . $mysqli->connect_errno . ') '. $mysqli->connect_error);
			// }

			$sql = "select title,community_name,price,area,total_price,spatial_arrangement,floor_index,total_floor,builded_year,advantage,".
				"details_url FROM for_sale_property AS a JOIN (SELECT id FROM for_sale_property FORCE INDEX".
				" (date_index) ORDER BY first_acquisition_time DESC LIMIT 0,300000) AS b WHERE a.id=b.id AND a.community_name like '%".$comm."%'";
			// $res = $mysqli->query($sql) or die($mysqli->error);
			$res_array = self::getResult($sql);

			// $res_array = $res->fetch_all(MYSQLI_ASSOC);
			if(count($res_array)<300){		//如果数据偏少，需要扩大查询
				$sql = "select title,community_name,price,area,total_price,spatial_arrangement,floor_index,total_floor,builded_year,advantage,".
					"details_url FROM for_sale_property AS a JOIN (SELECT id FROM for_sale_property FORCE INDEX".
					" (date_index) ORDER BY first_acquisition_time DESC LIMIT 300000,300000) AS b WHERE a.id=b.id AND a.community_name like '%".$comm."%'";
				// $res = $mysqli->query($sql) or die($mysqli->error);
				$res = self::getResult($sql);
				// $res_array = array_merge($res_array,$res->fetch_all(MYSQLI_ASSOC));
				$res_array = array_merge($res_array,$res);
			}
				
			// $res->close();
			// $mysqli->close();
			return $res_array;
		}
		
		function getResultOfAnalyse($arr){
		    /*传入二维数组，给出分析结果*/
		    $valid_full_arr = self::getValidFullArr($arr);                       //根据初步的统计结果，二次筛选，取出有效数据
		    $var1 = self::getDataInfo($valid_full_arr,'price');                              //有效信息中价格的基本信息
		    $var1 = array_merge($var1,self::getDataAnalysis($valid_full_arr,'price'));      //有效信息中价格的统计信息
		    
		    $var1['rowLen'] = count($arr);
			$var1['avg_area'] = self::getAvg($valid_full_arr, 'area');                        //分蚛平均面积、平均楼层、平均总楼层、平均建成年份写入数组
		    $var1['avg_total_floor'] = self::getAvg($valid_full_arr, 'total_floor');
		    $var1['avg_floor_index'] = self::getAvg($valid_full_arr, 'floor_index');
		    $var1['avg_builded_year'] = self::getAvg($valid_full_arr, 'builded_year');
			//$var1['collateral_value'] = round($var1['average']*0.82,0);									//这个以后再专门写计算抵押价值的函数
		    $var1['collateral_value'] = self::getCollateral_value($var1['average']);
			return $var1;
		}
		
		function getCollateral_value($avg){
			/*传入均价，根据这个值求出评估值*/
			$max1 = 63000;
			$max2 = 46000;
			$min1 = 8000;		
			$min2 = 7300;
			$ratio = $min2/$min1 - ($min2/$min1-$max2/$max1)/($max1-$min1)*($avg-$min1);
			$new_value = round($avg*$ratio,0);
			//$new_value = $ratio ;
			return $new_value;
		}
		
		function getV20Position($price){
			/*传入价格，根据这个价格的高低判断风险，来决定以哪个位置的价格为二手房评估价
			当8000元/平方时，取30%的位置，而63000时，取3%的位置*/
			$x1 = 63000;
			$x0 = 8000;
			$y1 = 3;
			$y0 = 30;
			$y = $y1 + ($price - $x1)/($x1 - $x0)*($y1 - $y0);
			$y = $y>0?$y:0;
			return round($y,0);
		}
		
		function getValidFullArr($arr){
		    /*传入二维数组，给出有效数据*/
		    $res_array = self::sortArr($arr,'price');                      //先排序
		    $clear_res_array = self::clearData($res_array,'price');	                  //去除最高最低
		    $valid_full_arr = self::getValidData($clear_res_array,'price');   //根据初步的统计结果，二次筛选，取出有效数据
		    return $valid_full_arr;
		} 
	    function getDataInfo($full_arr,$key){
			/*
			获取一个数组不用计算的信息：长度，中位数，最大，最小，及20%，40%，60%，80%的值
			传入的是二维数组
			*/
			$length = count($full_arr);  
			if ($length == 0) {  
				return array(0,0);  
			}  
			$arr = self::getColumn($full_arr,$key);
			$res['median'] = self::getElementFromArr($arr,50);
			$res['min'] = self::getElementFromArr($arr,0);
			$res['max'] = self::getElementFromArr($arr,100);
			//$res['v60'] = self::getElementFromArr($arr,60);
			$res['v75'] = self::getElementFromArr($arr,75);
			$res['v25'] = self::getElementFromArr($arr,25);
			$n = self::getV20Position($res['median']);
			//$res['v20'] = $n;
			$res['v20'] = self::getElementFromArr($arr,$n);			//2016.8.18增加根据风险来判断二手房评估价
			$res['len'] = $length;
			//$res['v20'] = self::getElementFromArr($arr,20);
			return $res;  

		}
		
		function getElementFromArr($arr,$position){
			/*
			从一个一维数组中取出指定位置的元素
			$position = 20，表示在20%位置上的数据
			*/
			$length = count($arr);  
			if ($length == 0) { 
				echo "传入的数组没有内容";
				return false;  
			}  
			
			//取指定位置的数，如果该位置存在于两个数之间，则取其平均值
			$var1 = (($length-1)*$position/10)%10 ;				//余数
			$var2 = (($length-1)*$position/10 - $var1)/10;		//第一位数的位置
			if ($var2 !== ($length -1)){
				$temp = array_slice($arr, $var2,2);
				//$getValue = $temp[0]*(1-$var1/10) + $temp[1]*$var1/10;
				$getValue = ($temp[0]+ $temp[1])/2;
				//$getValue = $temp[0];
			}else{
				$temp = array_slice($arr, $var2,1);
				$getValue = $temp[0];
			}

			return round($getValue,0);
			
		}
		
		function clearData($arr,$key){
			/*
			对传入数组去掉最高和最低的0.5%个值，一共去掉1%，但是不少于4个数
			$arr:待清理的数组
			2016.8.26 改成对二维数组处理 
			$key：用于计算的关键元素
			*/
			/*$length = count($arr);  
			if ($length >= 24) {
				$num_del = round($length / 200 , 0);			
				if ($num_del < 2) {
					$num_del = 2;
				}
				array_splice($arr, 0,$num_del);
				array_splice($arr, -$num_del,$num_del);
			}
			return $arr;*/
			/*2016.8.26改用使用盒须图原理去除偏离值*/
			$arr_key = self::getColumn($arr,$key);
			$clear['v75'] = self::getElementFromArr($arr_key,75);
			$clear['v25'] = self::getElementFromArr($arr_key,25);
			$clear_min = $clear['v25'] - ($clear['v75'] - $clear['v25'])*1.5;
			$clear_max = $clear['v75'] + ($clear['v75'] - $clear['v25'])*1.5;
			$new_arr = array();
			foreach($arr as $v){
				if ($v[$key]>=$clear_min and $v[$key]<=$clear_max){		//这是二维数组用的
				//if ($v>=$clear_min and $v<=$clear_max){
					$new_arr[]=$v;
				}
			}
			return $new_arr;
			
		}
		
		function getDataAnalysis($full_arr,$key){
			/*
			数组求其平均值、标准差
			*/
			$length = count($full_arr);  
			if ($length == 0) {  
				return array(0,0);  
			}  
			$arr = self::getColumn($full_arr,$key);
			$res['average'] = round(array_sum($arr)/$length,0);  
			$count = 0;
			foreach ($arr as $v) {  
				$count += pow($res['average']-$v, 2);  
			}  
			$res['std'] = round(sqrt($count/$length),0);
			if($length>1){
				$res['std'] = round(sqrt($count/($length-1)),0);	//2016.7.29修改一下标准差算法
			}else{
				$res['std'] = round(sqrt($count/($length)),0);		//2016.8.12防止只有一个数据出现除0错误
			}
			return $res;  

		}
	
		function getValidData($arr,$key){
			/*
			对原始数据进行清洗,2017.8.5修改成可以操作二维数组
			*/
			$SCOPE = 1.5;
			//$keyarr = self::getColumn($arr,$key);
			$res = self::getDataAnalysis($arr,$key);
			$new_arr = array();
			$max = $res['average'] + $SCOPE * $res['std'];
			$min = $res['average'] - $SCOPE * $res['std'];
			foreach($arr as $v){
				if ($v[$key]>=$min and $v[$key]<=$max){
					$new_arr[]=$v;
				}
			}
			return $new_arr;
		}
		function getAvg($arr,$key){
			/*
			根据一个二维数组求其平均值
			*/
	
			$length = count($arr);  
			if ($length == 0) {  
				return array(0,0);  
			}  
			$sum1 = 0;  
			$count = 0;
			foreach ($arr as $v) {  
				if($key=='builded_year'){
					if ($v[$key] > 1900){					
						$sum1 += $v[$key];
						$count += 1;
					}
				}else{
					if ($v[$key] > 0){					
						$sum1 += $v[$key];
						$count += 1;
					}
				} 
			}
			return round($sum1/$count,0);
			

		}
	}