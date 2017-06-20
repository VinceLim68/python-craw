<?php
	session_start();
	$comm = $_SESSION['dataResult']['comm'];
	if($comm == ""){		//如果没有小区名称，直接返回
		header("Location: index.php?show=5&succ=2"); 
		exit();
	}  
	
	date_default_timezone_set('PRC'); //设置中国时区 ,如果没设置会生成失败
	header("Content-type:text/html;charset=utf-8");
	
	//$comm = '瑞景新村';
	$dir = dirname(__FILE__);
	require $dir."./PHPExcel/PHPExcel.php";
	// require $dir."./class/DB.php";
	require_once $dir.'/class/Data_Handler.class.php';
	require_once $dir.'/class/DBConfig.php';
	
	// $db = new DB($dbconfig);
	$db = new Data_Handler($dbconfig);
	$objPHPExcel = new PHPExcel();			//实例化PHPExcel类

	$objSheet = $objPHPExcel->getActiveSheet();			//	获取活动sheet
	$objSheet->setTitle($comm);						//设置sheet名称
	// $data = $db->getDataByComm($comm);				//获取数据库中的数据
	$data = $db->getDataFromDatabase($comm);				//获取数据库中的数据
	$objSheet->setCellValue("A1","摘要")->setCellValue("B1","小区")->setCellValue("C1","单价")->setCellValue("D1","面积")->setCellValue("E1","总价")
		->setCellValue("F1","户型")->setCellValue("G1","楼层")->setCellValue("H1","总层")->setCellValue("I1","建成")
		->setCellValue("J1","优势")->setCellValue("K1","链接");						//设置标题 
	
	$objSheet->getDefaultStyle()->getFont()->setName("楷体")->setSize(11);		//设置默认格式：10号楷体
	
	$objSheet->freezePane("B2");				//冻结窗格
	$objSheet->getColumnDimension('A')->setWidth(60);			//设置列宽
	$objSheet->getColumnDimension('B')->setWidth(15);
	$objSheet->getColumnDimension('F')->setWidth(10);
	$objSheet->getColumnDimension('G')->setWidth(6);
	$objSheet->getColumnDimension('H')->setWidth(6);
	$objSheet->getColumnDimension('K')->setWidth(10);
	$objSheet->getStyle('B')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);		//设置居中
	$objSheet->getStyle('A1:K1')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	$objSheet->getStyle('C')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	$objSheet->getStyle('D')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	$objSheet->getStyle('E')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	$objSheet->getStyle('F')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	$objSheet->getStyle('G')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	$objSheet->getStyle('H')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	$objSheet->getStyle('I')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	$objSheet->getStyle('K')->getAlignment()->setHorizontal(PHPExcel_Style_Alignment::HORIZONTAL_CENTER);
	//$objSheet->getStyle('A1:K1')->getFont()->setBold(true);				//标题加粗
	$styleArray = array(					//设置标题样式
		'font' => array(
			'bold' => true,
			'size' => 14,
			'name' => '仿宋',
			'color'=>array(
			  'rgb' => 'ffffff',
			),
		),
	);
	
	$objSheet->getStyle('A1:K1')->applyFromArray($styleArray);
	$titleBorderStyle = getBorderSytle('FFFFff');		//设置标题的边框样式
	$objSheet->getStyle('A1:K1')->applyFromArray($titleBorderStyle);
	$objSheet->getStyle('A1:K1')->getFill()->setFillType(PHPExcel_Style_Fill::FILL_SOLID)->getStartColor()->setRGB('4C6284');//标题背景色



	$j = 2;
	
	foreach($data as $key=>$val){
		$objSheet->setCellValue("A".$j,$val['title'])->setCellValue("B".$j,$val['community_name'])->setCellValue("C".$j,$val['price'])->setCellValue("D".$j,$val['area'])->setCellValue("E".$j,$val['total_price'])
		->setCellValue("F".$j,$val['spatial_arrangement'])->setCellValue("G".$j,$val['floor_index'])->setCellValue("H".$j,$val['total_floor'])->setCellValue("I".$j,$val['builded_year'])
		->setCellValue("J".$j,$val['advantage'])->setCellValue("K".$j,'点击链接');			
		$objSheet->getCell("K".$j)->getHyperlink()->setUrl($val['details_url']);			//设置超链接
		$j++;
	}
	//$objSheet->fromArray($arr);
	$bodyBorderStyle = getBorderSytle('4C6284');			//取得报表主体的边框样式
	$objSheet->getStyle("A2:K".($j-1))->applyFromArray($bodyBorderStyle);
	$objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel,"Excel2007");			//指定格式生成excel
	$filename = $comm.date('YmdHis',time()).'.xlsx';									//拼成文件名
	//echo $filename;
	browser_export('Excel2007',$filename);
	$objWriter->save('php://output');
	//$objWriter->save($filename);
	//echo $dir."demo.xlsx";
	
	//从浏览器下载文件
	function browser_export($type,$filename){
		ob_end_clean();						//清除缓存，解决乱码
		if($type == 'Excel5'){
			header('Content-Type: application/vnd.ms-excel');			//按excel2003输出
		}else{
			header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');		//按excel2007输出
		}
		header('Content-Disposition: attachment;filename="'.$filename.'"');
		header('Cache-Control: max-age=0');		//禁止缓存
	}
	
	//获取不同颜色的边框样式
	function getBorderSytle($color){
		$defaultArray = array(
			'borders' =>array(
				'allborders' => array(
					'style' => PHPExcel_Style_Border::BORDER_THIN,
					'color' => array('rgb' => $color),
				)
			),
		);
		return $defaultArray;
	}

?>
