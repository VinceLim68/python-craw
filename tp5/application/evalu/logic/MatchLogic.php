<?php
namespace app\evalu\logic;

use app\evalu\model\Comm;

class MatchLogic {
	/*
	 * 这是通过小区名称来匹配出小区id的对象,使用单例设计
	 */
	
	// 	存放所有小区名称的列表,$comms[0]是小区名称,$comms[1]是道路名称
	public static $comms = [];		
	// 	存放所有以路名为区块的版块列表
	//public static $roads = [];
	
	//静态变量保存全局实例
	private static $_instance = null;
	
	//私有构造函数，防止外界实例化对象
	private function __construct() {
		self::$comms = Comm::getCommsArr();
	}
	
	//私有克隆函数，防止外办克隆对象
	private function __clone() {
	}
	
	//静态方法，单例统一访问入口
	static public function getInstance() {
		if (is_null ( self::$_instance ) || isset ( self::$_instance )) {
			self::$_instance = new self ();
		}
		return self::$_instance;
	}
	
	static public function getId($commName,$title='',$type = 'comms'){
		$find = array(".","。","．");
		$replace = array("");
		$commName = strtoupper(str_replace($find,$replace,$commName));
		
		// 		 储存匹配出来的id列表，可能不止匹配一个id值，每个元素包含（开始位置，关键字，id)
		$matchId = array();		

		foreach (self::$comms[$type] as $commItem){

			// 			$commItem['keyword']中可能通过'/'带着辅助字，先拆分开来，真正的key是它的第一个元素
			$key = explode ( "/", $commItem ['keyword'] );

			// 			在小区名称中查找关键字
			$start = stripos($commName,$key[0]);
			// 			必须使用 !== false 的方式，否则会把位置0 当成没找到
			if($start !== FALSE) {
				$len = count($key);
// 				echo $len;
				if($len>1){
					$temp = $commName . $title;
					for( $j = 1; $j < $len; $j++ ) {
						if (stripos($temp, strtoupper($key[$j])) !== FALSE ){
							$t = array($start,$key[0],$commItem['id']);
							
							$matchId[] = $t;
							break;
						}
					}
				}else{
					$t = array($start,$key[0],$commItem['id']);
						
					$matchId[] = $t;
// 					$matchId[] = array($start,$key[0],$commItem['id']);
				}
			}
		}
		return $matchId;
		
	}


}