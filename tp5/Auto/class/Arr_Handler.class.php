<?php
	class Arr_Handler{
		
		function sortArr($res_array,$str){
			/*
			����ĳ�е�ֵ��һ����ά��������
			$res_array:��������������
			$str:������������Ĺؼ���key_coloum
			*/
			array_multisort(self::getColumn($res_array,$str),$res_array);
			return $res_array;
		}
		
		function getColumn($res_array,$str){
			/*
			ȡ��һ����ά�����е�ĳ��
			$res_array:����Ķ�ά����
			$str:��ȡ�����е�keyֵ
			*/
			$newArr=array();
			for($j=0;$j<count($res_array);$j++){
				$newArr[]=$res_array[$j][$str];
			}
			return $newArr;
		}
			
	}
	