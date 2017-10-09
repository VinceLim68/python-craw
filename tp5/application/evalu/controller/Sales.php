<?php

namespace app\evalu\controller;

use think\Controller;
use think\Db;
use app\evalu\model\SalesModel;

class Sales extends Controller {
	protected $db;
	protected function _initialize() {
		parent::_initialize ();
		$this->db = new SalesModel();
	}
	
	/*
	 * 开始使用的直接用bootstrap展示挂牌信息
	 */
	public function index() {
		// 取没有小区id的记录，用empty('community')就好，但不知如何用
// 		$list = Db::table ( 'for_sale_property' )->where ( 'community_id', NULL )
// 			->whereor ( 'community_id', 0 )->paginate ( 100 );
		//测试一下速度
		$list = $this->db->field('details_url',true)->where ( '1=1' )
			->order ( ['id' => 'asc' ] )->paginate(500);
// 		var_dump($list);
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
		
		if (! $sidx) {
			$sidx = 1;
		}
		$where = '1=1';
		$outputs = array ();
		
		$list = $this->db->field('details_url',true)->limit ( $limit )->page ( $page )->where ( $where )
			->order ( ['id' => $sord ] )->select ()->toArray ();
		/*
		 * 返回值：total总页数,page当前页码,records总记录数,
		 * rows数据集,id每条记录的唯一id,cell具体每条记录的内容
		 */
		if(input('dontCount') and input('records')){
// 			echo '不去读数据库';
			$outputs['readfrommysql'] = 'false';
			$outputs['records'] = input('records');
		}else{
			$outputs['readfrommysql'] = 'true';
			$outputs ['records'] = $this->db->count();
		}
// 		$total = ceil ( $records / $limit );
		$outputs ['page'] = $page;
		$outputs ['total'] = ceil ( $outputs ['records'] / $limit );
		$outputs ['rows'] = $list;
		
		return $outputs;
	}
}