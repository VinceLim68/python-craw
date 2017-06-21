<?php

	header("Content-type:application/vnd.ms-excel");

	header("Content-Disposition:attachment;filename=users.xls");

	$string = "公司名称"."\t";

	$string .= "用户名" . "\t";

	$string .= "密码" . "\t";

	$string .= "二级域名" . "\t";

	$string .= "\n";       

	

	for($i=0;$i<4;$i++)

	{

		for($j=0;$j<4;$j++)

		{

			$string .=  "第".$i."行 第".$j."列"."\t";

		}

		$string .= "\n";

	}

	echo iconv("UTF-8","GB2312",$string);

?>

