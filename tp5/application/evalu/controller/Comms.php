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
    
    /**
     * 用jqgrid获取的小区列表
     */
    public function getList()
    {
        $page = $_GET['page'];
        $limit = $_GET['rows'];
        $sidx = $_GET['sidx'];
        $sord = $_GET['sord'];
        
        if (!$sidx)
            $sidx = 1;
        
            $where = '';
        
            if(!empty($_GET['keywords'])){
                $keywords = $_GET['keywords'];
                $where .= " and (keywords like '%".$keywords."%' or comm_name like '%".$keywords."%')";
            };
            if(!empty($_GET['region'])){
                $region = $_GET['region'];
                $where .= " and region like '%".$region."%'";};
                if(!empty($_GET['block'])){
                    $block = $_GET['block'];
                    $where .= " and block like '%".$block."%'";
                };
                if(!empty($_GET['address'])){
                    $address = $_GET['address'];
                    $where .= " and comm_addr like '%".$address."%'";};
        
        
                    $sql="SELECT COUNT(*) AS count FROM comm where 1=1".$where;
                    //print($sql);
                    $rows = $db->getResult($sql);
                    $count = $rows[0]['count'];
                    	
        
                    if ($count > 0) {
                        $total_pages = ceil($count / $limit);
                    } else {
                        $total_pages = 0;
                    }
                    if ($page > $total_pages)
                        $page = $total_pages;
                        $start = $limit * $page - $limit;
                        if ($start<0) $start = 0;
        
                        $SQL = "SELECT * FROM comm WHERE 1=1 ".$where." ORDER BY $sidx $sord LIMIT $start , $limit";
                        $rows = $db->getResult($SQL);
        
                        $outputs = array();
                        $cells = array();
                        $outputs['total']= $total_pages;
                        $outputs['page'] = $page ;
                        $outputs['records'] = $count;
                        foreach($rows as $row){
                            $cells[]=array('ID'=>$row['Id'],
                                'cell'=>array(
                                    $row['Id'],
                                    $row['comm_name'],
                                    $row['region'],
                                    $row['block'],
                                    $row['comm_id'],
                                    $row['block_id'],
                                    $row['keywords'],
                                    $row['comm_addr'],
                                    $row['pri_level']));
                        }
                        $outputs['rows'] = $cells;
                        //$result->close();
                        echo json_encode($outputs);
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