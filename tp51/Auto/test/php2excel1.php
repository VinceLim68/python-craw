<?php
	$dir = dirname(__FILE__);
	require $dir."./PHPExcel/PHPExcel.php";
	$objPHPExcel = new PHPExcel();			//实例化PHPExcel类
	//print_r($objPHPExcel);
	$objSheet = $objPHPExcel->getActiveSheet();			//	获取活动sheet
	$objSheet->setTitle("Demo");						//设置sheet名称
	$arr = array(
		array('姓名','分数'),
		array('张三','60'),
	);
	$arr1 = array(
		array('李四','80')
	);
	$objSheet->fromArray($arr);
	$objSheet->fromArray($arr1);
	$objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel,"Excel2007");			//指定格式生成excel
	$objWriter->save($dir."/demo.xlsx");
	//   echo $dir."demo.xlsx";

?>
