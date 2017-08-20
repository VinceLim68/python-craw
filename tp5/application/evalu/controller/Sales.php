<?php
namespace app\evalu\controller;
use think\Controller;
use think\Db;
class Sales extends Controller {
    
    public function index() {
//         取没有小区id的记录，用empty('community')就好，但不知如何用
        $list = Db::table('for_sale_property')->where('community_id',NULL)->whereor('community_id',0)->paginate(100);
//         $list = Db::table('for_sale_property')->where('community_id',NULL)->limit(10)->select();
        // 把分页数据赋值给模板变量list
        $this->assign('list', $list);
        // 渲染模板输出
//         $var = 1;
//         halt(empty($var));
//         dump($list);
        return $this->fetch();
    }
}