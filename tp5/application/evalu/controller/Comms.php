<?php
namespace app\evalu\controller;

use think\Controller;
use app\evalu\model\Comm;

class Comms extends Controller
{
    protected $db;
    
    protected function _initialize()
    {
        parent::_initialize();
        $this->db = new Comm();    
    }
    
    /*
     * 展示小区列表
     */
    public function commsList()
    {
        return $this->fetch();
    }
    
    /**
     * 用jqgrid获取的小区列表
     */
    public function getComms()
    {
        echo 'I have come here';
    }
    
    
    /**
     * 小区列表
     */
    public function index(){
//         $list = Db::table('comm')->paginate(100);
        $list = $this->db->paginate(100);
        $this->assign('list', $list);
        return $this->fetch();
    }
    
    public function matchid(){
/*         $comm = $this->db->select();
        halt($comm); */
        $this->db->getCommsArr();
    }
}