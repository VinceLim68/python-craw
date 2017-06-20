<?php
	class Arr_Handler{
		
		function sortArr($res_array,$str){
			/*
			根据某列的值给一个多维数组排序
			$res_array:传入待排序的数组
			$str:传入用来排序的关键字key_coloum
			*/
			array_multisort(self::getColumn($res_array,$str),$res_array);
			return $res_array;
		}
		
		function getColumn($res_array,$str){
			/*
			取出一个多维数组中的某列
			$res_array:传入的多维数组
			$str:待取出的列的key值
			*/
			$newArr=array();
			for($j=0;$j<count($res_array);$j++){
				$newArr[]=$res_array[$j][$str];
			}
			return $newArr;
		}
			
	}
	