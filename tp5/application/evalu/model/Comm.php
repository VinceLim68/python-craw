<?php
namespace app\evalu\model;
use think\Model;

class Comm extends Model {
    /**
     * 操作表：小区信息
     */
    protected $pk = 'Id';
    protected $table = 'comm';
    protected $resultSetType = 'collection';		//这个设置可以很快把返回数据集转成array
    protected $field = true;						//忽略非数据表字段而不报错
    
    public function getPriLevelAttr($value)
    {
        $pri_level = [0=>'小区级',1=>'区块级'];
        return $pri_level[$value];
    }
    
/*     public function setPriLevelAttr($value)
    {
    	$pri_level = array('小区级'=>0,'区块级'=>1);
    	return $pri_level[$value];
    } */
    
    public static function _getCommsArr(){
        /**
         * 这个要删除了，把小区名按关键字拆分后形成一个数组
         */
        $comms = self::field("comm_id,comm_name,pri_level,keywords")->select();
        $comms_arr = array();
        foreach ($comms as $comm){
            $kws = explode(",", $comm['keywords']);
            foreach ($kws as $kw){
                $temp = array();
                $temp[] = $comm['comm_id'];
                $temp[] = $kw;
                $comms_arr[] = $temp;
            }
        }
        return $comms_arr;        
    
    }
    
    public static function getAll(){
        $comms = self::field("comm_id,comm_name,pri_level,keywords")->select();
        return $comms;
    }
    
    public static function getRegions(){
    	$regions = self::field('region')->distinct(true)->select()->toArray();
    	return $regions;
    }
    
    public static function getBlockByRegion($reg){
    	$blocks = self::field('block')->distinct(true)->where('region',$reg)->select()->toArray();
    	return $blocks;
    }
    
   


}