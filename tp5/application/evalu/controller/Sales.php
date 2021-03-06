<?php

namespace app\evalu\controller;

use think\Controller;
use think\Db;
use app\evalu\model\SalesModel;
use app\evalu\logic\MatchLogic;

class Sales extends Controller {
	protected $db;
	protected $mch;
	protected function _initialize() {
		parent::_initialize ();
		$this->db = new SalesModel ();
		$this->mch = MatchLogic::getInstance();
	}
	
	/*
	 * 开始使用的直接用bootstrap展示挂牌信息
	 */
	public function index() {
		// 取没有小区id的记录，用empty('community')就好，但不知如何用
		// $list = Db::table ( 'for_sale_property' )->where ( 'community_id', NULL )
		// ->whereor ( 'community_id', 0 )->paginate ( 100 );
		// 测试一下速度
		$list = $this->db->field ( 'details_url', true )->where ( '1=1' )->order ( [ 
				'id' => 'asc' 
		] )->paginate ( 500 );
		// var_dump($list);
		$this->assign ( 'list', $list );
		return $this->fetch ();
	}
	
	/*
	 * 使用JGrid展示挂牌信息
	 */
	public function salesList() {
		return $this->fetch ();
	}
	
	/*
	 * 给jqgrid提供的挂牌信息
	 */
	public function getSales() {
		$page = input ( 'page' ); // 第几页
		$limit = input ( 'rows' ); // 每页几条记录
		$sidx = input ( 'sidx' ); // 排序字段
		$sord = input ( 'sord' ); // 正序还是倒序
		$action = input('action');//决定要取出什么数据
		
		if (! $sidx) {
			$sidx = 1;
		}
		$where = '1=1';
		$outputs = array ();
		
		if (!$action or $action=='all'){
			$list = $this->db->field ( 'details_url', true )->limit ( $limit )->page ( $page )
				->where ( $where )->order ( [ 'id' => $sord ] )->select ()->toArray ();
		}elseif ($action == 'nomatch'){
			$list = $this->db->field ( 'details_url', true )->limit ( $limit )->page ( $page )
				->where ( $where )->where ( 'community_id', NULL )->whereor ( 'community_id', 0 )
				->order ( [ 'id' => $sord ] )->select ()->toArray ();
		}elseif ($action == 'mulmatch'){
			$list = $this->db->field ( 'details_url', true )->limit ( $limit )->page ( $page )
				->where ( $where )->where ( 'community_id', '>' ,0)->where ( 'community_id', '<' ,100)
				->order ( [ 'id' => $sord ] )->select ()->toArray ();
		}
	
		/*
		 * 返回值：total总页数,page当前页码,records总记录数,
		 * rows数据集,id每条记录的唯一id,cell具体每条记录的内容
		 */
		if (input ( 'dontCount' ) and input ( 'records' )) {
			// echo '不去读数据库';
			$outputs ['readfrommysql'] = 'false';
			$outputs ['records'] = input ( 'records' );
		} else {
			$outputs ['readfrommysql'] = 'true';
			if (!$action or $action=='all'){
				$outputs ['records'] = $this->db->count('id');
			}elseif ($action == 'nomatch'){
				$outputs ['records'] = $this->db->where ( $where )->where ( 'community_id', NULL )
					->whereor ( 'community_id', 0 )->count();
			}elseif ($action == 'mulmatch'){
				$outputs ['records'] = $this->db->where ( $where )->where ( 'community_id', '>' ,0)
				->where ( 'community_id', '<' ,100)->count();
			}
		}
		// $total = ceil ( $records / $limit );
		$outputs ['page'] = $page;
		$outputs ['total'] = ceil ( $outputs ['records'] / $limit );
		$outputs ['rows'] = $list;
		
		return $outputs;
	}
	
	public function getUrlById(){
		/*
		 * 通过传入的id查询相应的details_url
		 */
		$byId = input('ID');
		$url = $this->db->field('details_url')->where('id',$byId)->find();
		//echo $url;
		return $url['details_url'];
	}
	
	public function match(){
		//$arr = MatchLogic::getCommsArr();
		$arr = MatchLogic::$comms;
		//dump($arr);
		return $arr;
	}
	
	public function text_len(){
		$arr = MatchLogic::$comms;
		$len = count($arr['comms']);
		//dump($arr);
		return $len;
	}
	
	public function matchComm(){
		/*
		 * 通过传入的id来匹配小区id
		 */
		$byId = input('id');
		$commName = input('commName');
		$title = input('title');
		$idArr = MatchLogic::getId($commName,$title );
		return ($idArr);
		
	}
}