<?php
namespace app\evalu\controller;
use think\Controller;
use think\Db;
class Sales extends Controller {
    
    public function index() {
        $list = Db::table('for_sale_property')->paginate(100);
        // 把分页数据赋值给模板变量list
        $this->assign('list', $list);
        // 渲染模板输出
//         halt($list);
        return $this->fetch();
    }
}