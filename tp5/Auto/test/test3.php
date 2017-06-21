<?php
require_once 'apprsal_Handle.class.php';
$comm = '中航城';
$AH = new ApprsalHandle;
$arrs = $AH->getOfferedAndCase($comm);
print_r(key($arrs));


// foreach($arrs as $arr){
	// print_r($arr);

// }
// echo "<br/>";
// print_r(count($arrs));
?>
