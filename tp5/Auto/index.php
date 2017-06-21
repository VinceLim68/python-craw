<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" type="text/css" href="./css/mycss.css">
<title>诚德行自动询价系统（林晓）</title>
<?php
	session_start();
	define('ROOT_PATH',dirname(__FILE__));
	require_once ROOT_PATH.'/class/Data_View.class.php';
	//require_once ROOT_PATH.'/class/apprsal_cdh_Handler.class.php';
	$isNotValid = false;
	$isShow = false;
	if(isset($_GET["show"])){
	    if($_GET["show"]==0){
	        $isShow = 0;
        }elseif($_GET["show"]==1){
	        $isShow = 1;
        }elseif ($_GET["show"]==2){
            $isShow = 2;
        }
        elseif ($_GET["show"]==3){
            $isShow = 3;
        }elseif ($_GET["show"]==5){			//返回是否生成excel表格
            $isShow = 5;
			$isSuc = $_GET["succ"];
        }elseif ($_GET["show"]==6){
            $isShow = 6;
        }elseif ($_GET["show"]==7){
            $isShow = 7;
			$isSuc = $_GET["success"];
        }elseif ($_GET["show"]==8){			//为8时什么都不显示，只出现一个查询条
            $isShow = 8;
			
        }
	}
	//if(isset($_SESSION["flag"])||$isShow){
	if(isset($_SESSION["flag"])){
	    //echo "true";
		$flag = $_SESSION["flag"];
		if($flag == 1){
			$data = $_SESSION['dataResult'];
		}
		//$_SESSION["flag"] = 0;
		if(!empty($data['median'] )){
			$isNotValid = (round($data['std']/$data['average']*100,2)>13 or $data['len']<50);
		}
	}
?>
</head>
<body>

<form action="autovaluate.php" method="post">
	<div class="searchbg">
		<input type="text" class="inputstyle_out" value="输入小区名搜索" name="fname" onfocus="script:if(this.value=='输入小区名搜索')this.value='';">
		<input type="submit" class="button" value="查房价" >
		<div id="goto"><a href="./comm_manager/index.html" >小区名称管理</a></div>
		<!-- <span class="fontS" style="color: white;margin-bottom:0;">专家型估价系统：展示数据细节，独有风险评估</span> -->
	</div>
</form>


<div class="detailcon" style="margin-left:10%;">
<?php if (!empty($data['std']) and $isShow>0 and $isShow!=8){ ?>			
	<!--给出评估价值-->
	<div class="villagedetail">
		
		
		<div class="villagename" id="pgy_C01_05">
			<div class="fontB2" id='comm' >
				<?php echo $data['comm'];?>
			</div>
			<div class="offerdetailfont">
			    <span >基价内涵</span><br/>
		     	<span >
				面积：<?php echo $data['avg_area'];?>平方米
				</span><br/>
				<span >
				总层：<?php echo $data['avg_total_floor'];?>层
				</span><br/>
				<span >
				楼层：<?php echo $data['avg_floor_index'];?>层
				</span><br/>
				<span >
				建成：<?php echo $data['avg_builded_year'];?>年
				</span>
			</div>
		</div>
		<div class="offer" >
		    <label class="fontS" style="color: white">抵押评估价 </label>
			<br/>
			<label class="fontB" <?php if($isNotValid){echo 'style="color:#FF6600;"';} ?> >
				<?php 	echo $data['collateral_value'];	 ?>
			</label>
			<br/>
			<label class="fontS" style="color: white">元/平方米</label>
		</div>
		<div class="offer">
			<label class="fontS" style="color: white">二手房评估价  </label>
			<br/>
			<label class="fontB" <?php if($isNotValid){echo 'style="color:#FF6600;"';} ?> >
				<?php echo $data['v20']; ?>
			</label>
			<br/>
			<label class="fontS" style="color: white">元/平方米</label>
		</div>
		<div class="warning">
			<p>
				<div class="span20">
					<span class="fontS">标准差系数：
						<?php	echo round($data['std']/$data['average']*100,2);?>
					</span>%
					<?php if (round($data['std']/$data['average']*100,2)>13){	?>
    					<span class="fontS" >
        					<span class="red">
        						<b>&nbsp&nbsp&nbsp数据离散性较大，请联系估价师再确认价格。</b>
        					</span>
    					</span>
					<?php }	?>
				</div>
			</p>
			<p>
				<div class="span20">
					<span class="fontS">数据量：
						<?php echo $data["rowLen"];	?>/
						<?php echo $data['len'];?>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp覆盖率：
				        <?php echo round($data['len']/$data["rowLen"]*100,2);?>	%
					</span> 
				</div>
				<?php if($data['len']<50){	?>
    				<div class="span20">
    					<span class="fontS" >
    						<span class="red">
    							<b>数据样本较少，评估价须联系估价师再确认。</b>		
    						</span>
    					</span>
    	            </div>
				<?php	}	?>
			</p>
		</div>

        <div class="link">
		      <a href="index.php?show=2" id="mylink1">数据分析&gt;&gt;</a>
		      <a href="index.php?show=3" id="mylink2" >优化报价&gt;&gt;</a>
		      <a href="index.php?show=4" id="mylink2">风险判断&gt;&gt;</a>
			  <a href="genExcel.php" id="mylink2">导出数据&gt;&gt;</a>
			  <a href="index.php?show=6" id="mylink2">报价/成交&gt;&gt;</a>
		</div>
		
	</div>
    
	<!-- 返回生成excel表格是否成功的信息-->
	<?php if($isShow==5){  ?>
		<div class = "BoxWhiskerPlot" >
			<?php
			if($isSuc == 2){
			?>		
			<div class="fontS" style="margin:45px;text-align:center;">
				<a href="index.php">没有小区名称，无法导出数据</a>
			</div>
			<?php 
			}else{
			?> 
			<div class="fontS" style="margin:45px;text-align:center;">
				<a href="index.php">生成</a>
			</div>
			<?php } ?>   
		</div>
	<?php } ?>  
	
	<!-- 查询出历史的报价记录和成交案例 -->
    <?php if($isShow==6){  ?>
		<div class="scrolldiv" >
			<?php
				if(empty($dv)){
					$dv = new DataView;
				}
				$dv->showHistoryRecord($data['comm']);
			?>
			
		</div>
	<?php } ?>    
	
    <!-- 生成询价记录 -->
    <?php if($isShow==3){  ?>
    <form action="insertQueryRecord.php" method="post">
		<div class = "BoxWhiskerPlot" style="background:#D6DADE;border:0;">
			<?php
				if(empty($dv)){
					$dv = new DataView;
				}
				$dv->showQueryTable($data);
			?>
			
		</div>
	</form>
	<?php } ?>    
	
	<!-- 询价返回结果 -->
    <?php if($isShow==7){  ?>
    
	<div class = "BoxWhiskerPlot" >
		<?php
		if($isSuc == 1){
		?>		
		<div class="fontS" style="margin:45px;text-align:center;">
			<a href="index.php?show=3">成功添加一条记录</a>
		</div>
		<?php 
		}elseif($isSuc == 2){
		?> 
		<div class="fontS" style="margin:45px;text-align:center;">
			<a href="index.php?show=3">这个小区最近您已经报过价了</a>
		</div>
		<?php } ?>   
	</div>

	<?php } ?>    
	
	<!-- 生成盒须图 -->
	<?php if($isShow==1||$isShow==2){  ?>
	<div class = "BoxWhiskerPlot" style="height: 100px">
		<?php
    		if(empty($dv)){
    		    $dv = new DataView;
    		}
			$dv->showBoxWhiskerPlot($data,890,45,100,25);
		?>
	</div>
	<?php } ?>  

	<!-- 生成数据分布直方图 -->
	<?php if($isShow==2 or $isShow==1){  ?>
	<script type="text/javascript">
    	function show_coords(evt){
			var event = evt || window.event;
			var x = event.offsetX;
			var say = document.all("coords");
			var value1 = ((x-45)/800*(<?php echo $data['max'];?>-<?php echo $data['min'];?>)+<?php echo $data['min'];?>);
			//var value = Math.round(((x-45)/800*(<?php echo $data['max'] ?>-<?php echo $data['min'] ?>)+<?php echo $data['min'] ?>)*0.82,2);
    		var value = Math.round(value1*0.82,2);
			var max1 = 63000;
			var max2 = 46000;
			var min1 = 8000;		
			var min2 = 7300;
			var ratio = min2/min1 - (min2/min1-max2/max1)/(max1-min1)*(value1-min1);
			var new_value = Math.round(value1*ratio,2);
    		// var say = document.all("coords");
    		//say.innerHTML = max1;
			say.innerHTML = "旧:" + value + ",新:" + new_value;

    	}
    	function clear_coords(){
    		var say = document.all("coords");
    		say.innerHTML = "";
    	}
	</script>
	<div onmousemove="show_coords(event)" onmouseout="clear_coords()" class="Histogram">
		<div id="coords" style="width: 25%"></div>
		<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="100%" height="100%" >
			<?php
				$histo = $_SESSION['histo']; 
			
    			/* if(empty($dv)){
    			    $dv = new DataView;
    			}
    			$dv->getHistogramArray($arrs, $n); */
			
				$len = count($histo);
				$h_max = max($histo);
				$width = 800/$len;
				$divheight = 200;
				for ($i=0;$i<$len;$i++){
					$s_x = 45 + $i*$width;
					$s_y = (1-$histo[$i]/$h_max)*$divheight+20;
			?>	
			<rect x=<?php echo $s_x?> y=<?php echo $s_y?> width=<?php echo $width ?> height=<?php echo $histo[$i]/$h_max*$divheight ?> style="fill:#36465D;;stroke:#1A2636;stroke-width:3px;opacity:0.2;"/>
			<text x=<?php echo $s_x+5?> y=<?php echo $s_y-6?> style="font-family: Arial, SimSun;font-size:15px;width:354px;color:#36465D;line-height:14px;fill:#36465D;" text-anchor="start";>
				<?php echo $histo[$i]?>
			</text>
			<?php	}	?>
		</svg>
	</div>   
    <?php } ?>  
	

<?php }else{	?> 
	<!--给出没找到信息的提示<?php $data['comm']?>-->
	<?php if($isShow==0 and !empty($_GET['fname'])){  ?>
		<div class = "BoxWhiskerPlot" >
			<div class="fontS" style="margin:45px;text-align:center;">
				<a href="index.php?show=8">似乎没有叫"<?php echo $_GET['fname']?>"的小区啊，要不您再确认一下？</a>
			</div>
		</div>
	<?php }?>
	
<?php }?>		
</div>

     
           
        
</body>
</html>