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
    
    public function matchid(){
/*         $comm = $this->db->select();
        halt($comm); */
        $this->db->getCommsArr();
    }
}