<?php
	date_default_timezone_set('PRC'); //设置中国时区 
	set_time_limit(0);
	

	class DataView{
		public function showHistoryRecord($comm){
			// 传入小区名称，显示出历史的报价记录和成效案例
			// SELECT Enquiry_CellName AS Name,PA_Located AS Addr,Apprsal_Use AS ,Apprsal_Up AS Price,Enquiry_Date AS ,".
					// "PA_Level AS ,PA_YearBuilt AS ,PA_Structure AS ,PA_Elevator AS ,Remark AS ,".
					// "Enquiry_PmName AS ,OfferPeople AS  
			require_once 'apprsal_Handle.class.php';
			require_once "DBConfig.php";
			$AH = new ApprsalHandle($dbconfig) ;
			$arrs = $AH->getOfferedAndCase($comm);
			echo '<div class="tableBox" > ';
			echo '<div class="tablehead"> ';
				echo '<table class="tab_showHistoryRecord" >';
					echo '<tr>';
						echo '<td class="showRecord" style="width:70px;"><div align="center">小区名称</div></td>';
						echo '<td class="showRecord" style="width:195px;"><div align="center">地址</div></td>';
						echo '<td class="showRecord" style="width:37px;"><div align="center">用途</div></td>';
						echo '<td class="showRecord" style="width:65px;"><div align="center">价格</div></td>';
						echo '<td class="showRecord" style="width:80px;"><div align="center">日期</div></td>';
						echo '<td class="showRecord" style="width:37px;"><div align="center">楼层</div></td>';
						echo '<td class="showRecord" style="width:55px;"><div align="center">建成</div></td>';
						echo '<td class="showRecord" style="width:192px;"><div align="center">备注</div></td>';
						echo '<td class="showRecord" style="width:55px;"><div align="center">询价人</div></td>';
						echo '<td class="showRecord" style="width:55px;"><div align="center">报价人</div></td>';
					echo '</tr>';
				echo '</table>';
			echo '</div>';
			
			//if($totalRows1) {//记录集不为空显示
			echo '<div class="tablebody"> ';
			echo '<table class="tab_showHistoryRecord" >';
			foreach($arrs as $row){
				//对数字格式取整操作（否则会有4位小数
				if(is_numeric($row['Price'])){
						$row['Price']=round($row['Price'],0);
				}
				
				//对建成年份字段只取年，如果没有则取为''.
				if(!($row['Build']=="")){
					$row['Build']=date('Y',strtotime($row['Build']));
				}
				
				//从案例库里读出来的数据填写完整，方便统一展示
				if(!isset($row['Memo'])){
					$row['Memo'] = "成交案例";
					$row['Xjr'] = "";
				}
				echo '<tr class="tr">';
					echo '<td class="showRecord" style="width:70px;"><div align="center">'.$row['Name'].'</div></td>';
					echo '<td class="showRecord" style="width:195px;"><div align="center">'.$row['Addr'].'</div></td>';
					echo '<td class="showRecord" style="width:37px;"><div align="center">'.$row['Myuse'].'</div></td>';
					echo '<td class="showRecord" style="width:65px;"><div align="center">'.$row['Price'].'</div></td>';
					echo '<td class="showRecord" style="width:80px;"><div align="center">'.date('Y-m-d',strtotime($row['Myday'])).'</div></td>';
					echo '<td class="showRecord" style="width:37px;"><div align="center">'.$row['Level'].'</div></td>';
					echo '<td class="showRecord" style="width:55px;"><div align="center">'.$row['Build'].'</div></td>';
					echo '<td class="showRecord" style="width:192px;"><div align="center">'.$row['Memo'].'</div></td>';
					echo '<td class="showRecord" style="width:55px;"><div align="center">'.$row['Xjr'].'</div></td>';
					echo '<td class="showRecord" style="width:55px;"><div align="center">'.$row['Offer'].'</div></td>';
				echo '</tr>';
			}
			echo '</table>';
			echo '</div>';
			echo '</div>';
		}
		
		public function getHistogramArray($arrs,$n){
			//传入数组$arr，维度$n,
			//返回一个带直方图特征的二维数组（每个维度的数据占总量的百分比)
			$minOfArr = min($arrs);
			$eachScope = (max($arrs)-$minOfArr )/$n;
			$histogramArr = array();
			for ($i=0;$i<$n;$i++){
				$histogramArr[$i] = 0;	//给数组赋值0；
			}
			$total = 0;
			foreach ($arrs as $arr){
				//当前数据在哪个维度，从0开始
				$j = floor(($arr - $minOfArr )/$eachScope);
				if ($j == $n){
				    $j = $j-1;
				}		
				$histogramArr[$j] += 1;
				$total += 1;
			}

			return ($histogramArr);
		}
		
		public function showBoxWhiskerPlot($data,$L,$l0,$W,$w0){
			// 计算绘制箱线图所需要的相关参数
			// 传入参数：
			// $data:分析后数据结果集，数组
			// L：div 的长
			// l0:画图起点的X值，相当于padding-left
			// W：div的高
			// w0:相当于padding-top
			$Q0 = $l0;
			$Q1 = ($L-2*$l0)*($data['v25']-$data['min'])/($data['max']-$data['min'])+$l0;
			$Q2 = ($L-2*$l0)*($data['median']-$data['min'])/($data['max']-$data['min'])+$l0;
			$Q3 = ($L-2*$l0)*($data['v75']-$data['min'])/($data['max']-$data['min'])+$l0;
			$Q4 = $L-$l0;
			$Y1 = $w0;		//这是纵线上瑞的Y轴值
			$Y2 = ($W-3*$w0)/2+$w0;		//这是横线的Y轴值
			$Y3 = $W-2*$w0;	//这是纵线下瑞的Y轴值
			$Y4 = $W-$w0-5;	//刻度的Y轴
			
			
			$line1Str = "M ".$Q0." ".$Y2." L ".$Q1." ".$Y2;
			$line2Str = "M ".$Q3." ".$Y2." L ".$Q4." ".$Y2;
			$startlineStr = "M ".$Q0." ".$Y1." L ".$Q0." ".$Y3;
			$endlineStr = "M ".$Q4." ".$Y1." L ".$Q4." ".$Y3;
			$medlineStr = "M ".$Q2 ." ".$Y1." L ".$Q2 ." ".$Y3;

			echo '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="100%" height="100%" >';
				//在echo中计算式要用括号包起来
				echo '<rect x='.$Q1.' y='.$Y1.' width='.($Q3-$Q1).' height='.($Y3-$Y1).' style="fill:none;stroke:#36465D;stroke-width:3px;"/>';
				echo '<path fill="none" d="'.$medlineStr.'" stroke="#36465D" stroke-width="3px"></path>';
				//echo '<path fill="none" d="M '.$Q0.' '.$Y4.' L '.$Q4.' '.$Y4.'" stroke="#36465D" stroke-width="2px" opacity="0.5"></path>';		//这是下面的标轴线
				if($Q1-1.5*($Q3-$Q1)>$Q0){		//前瑞数据有异常值
					$beforelineStr1 = "M ".($Q1-1.5*($Q3-$Q1)) ." ".$Y1." L ".($Q1-1.5*($Q3-$Q1)) ." ".$Y3;
					$beforelineStr2 = "M ".($Q1-1.5*($Q3-$Q1)) ." ".$Y2." L ".$Q0." ".$Y2;
					$beforelineStr3 = "M ".($Q1-1.5*($Q3-$Q1)) ." ".$Y2." L ".$Q1." ".$Y2;
					echo '<path fill="none" d="'.$beforelineStr1.'" stroke="#36465D" stroke-width="3px"></path>';
					echo '<path fill="none" d="'.$beforelineStr3.'" stroke="#36465D" stroke-width="3px"></path>';
					echo '<path fill="none" d="'.$startlineStr.'" stroke="#A0A0A0" stroke-width="2px" stroke-dasharray="10,5"></path>';
					echo '<path fill="none" d="'.$beforelineStr2.'" stroke="#A0A0A0" stroke-width="2px" stroke-dasharray="10,5"></path>';
				}else{
					echo '<path fill="none" d="'.$startlineStr.'" stroke="#36465D" stroke-width="3px"></path>';
					echo '<path fill="none" d="'.$line1Str.'" stroke="#36465D" stroke-width="3px"></path>';
				}
				if($Q3+1.5*($Q3-$Q1)<$Q4){		//后瑞数据有异常值
					$afterlineStr1 = "M ".($Q3+1.5*($Q3-$Q1)) ." ".$Y1." L ".($Q3+1.5*($Q3-$Q1)) ." ".$Y3;
					$afterlineStr2 = "M ".($Q3+1.5*($Q3-$Q1)) ." ".$Y2." L ".$Q4." ".$Y2;
					$afterlineStr3 = "M ".($Q3+1.5*($Q3-$Q1)) ." ".$Y2." L ".$Q3." ".$Y2;
					echo '<path fill="none" d="'.$afterlineStr1.'" stroke="#36465D" stroke-width="3px"></path>';
					echo '<path fill="none" d="'.$afterlineStr3.'" stroke="#36465D" stroke-width="3px"></path>';
					echo '<path fill="none" d="'.$endlineStr.'" stroke="#A0A0A0" stroke-width="2px" stroke-dasharray="10,5"></path>';
					echo '<path fill="none" d="'.$afterlineStr2.'" stroke="#A0A0A0" stroke-width="2px" stroke-dasharray="10,5"></path>';
				}else{
					echo '<path fill="none" d="'.$line2Str.'" stroke="#36465D" stroke-width="3px"></path>';
					echo '<path fill="none" d="'.$endlineStr.'" stroke="#36465D" stroke-width="3px"></path>';
				}
				echo '<g zIndex="7">';
					echo '<text x='.$Q1.' y="'.($W-25).'" style="font-family: Arial, SimSun;font-size:15px;width:354px;color:#36465D;line-height:14px;fill:#36465D;" text-anchor=" middle">';
						echo '<tspan x="'.$Q0.'">'.$data['min'].'元</tspan>';
						echo '<tspan x="'.$Q1.'">'.$data['v25'].'元</tspan>';
						echo '<tspan x="'.$Q2.'">'.$data['median'].'元</tspan>';
						echo '<tspan x="'.$Q3.'">'.$data['v75'].'元</tspan>';
						echo '<tspan x="'.$Q4.'">'.$data['max'].'元</tspan>';
						if($Q1-1.5*($Q3-$Q1)>$Q0){
							echo '<tspan x="'.($Q1-1.5*($Q3-$Q1)).'">'.round($data['v25']-1.5*($data['v75']-$data['v25']),0).'元</tspan>';
						}
						if($Q3+1.5*($Q3-$Q1)<$Q4){
						
							echo '<tspan x="'.($Q3+1.5*($Q3-$Q1)).'">'.round($data['v75']+1.5*($data['v75']-$data['v25']),0).'元</tspan>';

						}
					echo '</text>';				
				echo '</g>';
			echo '</svg>';
			
		}
		
		public function showQueryTable($data){
              /*  把$data数组传入，生成询价记录 */
		    $xjr = array("廖亚香","黄燕翔","王亿彬","金忠","泉州银行","招商银行","云估价","陈锦钦","陈丽华","吴木兰","项争","陈志艳","贾琴","陈玉炜","王梓瀛","陈幼梅","吴洁","陈军勇","朱黎英","邱宏达","伍雄","公司外部");
		    echo '<datalist id="xjr">';
		    foreach ($xjr as $value){
		        echo '<option>'.$value.'</option>';
		    }
		    echo '</datalist>';
			
			$usage = array("住宅","车位","写字楼","商业","酒店","独栋别墅","联排别墅","双拼别墅","叠加别墅","工业","土地","其他");
		    echo '<datalist id="usage">';
		    foreach ($usage as $value){
		        echo '<option>'.$value.'</option>';
		    }
		    echo '</datalist>';
			
		    if($data['avg_total_floor']>8){
				$elevator = "带电梯";
			}else{
				$elevator = "无电梯";
			}
			echo '<datalist id="elevator">';
		        echo '<option>带电梯</option>';
				echo '<option>无电梯</option>';
		    echo '</datalist>';
			
			if($data['avg_total_floor']>7){
				$structure = "钢混";
			}else{
				$structure = "砖混";
			}
			
			echo '<table style="padding-top:15px;padding-bottom:15px;">';
		        echo '<tr class="querytable_tr">';
		             echo '<td class="tdcol">小区名称:</td>';
		             echo '<td class="tdcontent"><input type="text" class="tdinput" name="t_comm" value="'.$data['comm'].'"></input></td>';
		             echo '<td class="tdcol">地址:</td>';
		             echo '<td class="tdcontent" colspan="3"><input type="text" class="tdinput" name="t_add" value="二手房可以评估'.$data['v20'].'"></input></td>';
		             
		        echo '</tr>';
		        echo '<tr class="querytable_tr">';
    		        echo '<td class="tdcol">报价:</td>';
    		        echo '<td class="tdcontent"><input type="text" class="tdinput" style="width:50%;" name="t_collateral_value" value="'.$data['collateral_value'].'"></input>&nbsp;&nbsp;元/平方米</td>';
    		        echo '<td class="tdcol">备注:</td>';
    		        echo '<td class="tdcontent" colspan="3"><input type="text" class="tdinput" name="t_memo" value="'.$data['len'].'个数据，挂牌价格'.$data['min'].'-'.$data['max'].'"></input></td>';
		        echo '</tr>';
		        echo '<tr class="querytable_tr">';
    		        echo '<td class="tdcol">用途:</td>';
    		        echo '<td class="tdcontent"><input list="usage" class="tdinput" name="t_usage" value="住宅" style="width:50%;"></input></td>';
    		        echo '<td class="tdcol">总层数:</td>';
    		        echo '<td class="tdcontent"><input type="text" class="tdinput" style="width:50%;" name="t_avg_total_floor" value="'.$data['avg_total_floor'].'"></input>&nbsp;&nbsp;层</td>';
    		        echo '<td class="tdcol">所在楼层:</td>';
    		        echo '<td class="tdcontent"><input type="text" class="tdinput" style="width:50%;" name="t_avg_floor_index" value="'.$data['avg_floor_index'].'"></input>&nbsp;&nbsp;层</td>';
    		        
		        echo '</tr>';
		        echo '<tr class="querytable_tr">';
    		        echo '<td class="tdcol">建成年份:</td>';
    		        echo '<td class="tdcontent"><input type="text" class="tdinput" style="width:50%;" name="t_avg_builded_year" value="'.$data['avg_builded_year'].'"></input>&nbsp;&nbsp;年</td>';
    		        echo '<td class="tdcol">电梯:</td>';
    		        echo '<td class="tdcontent"><input list="elevator" class="tdinput" style="width:50%;" name="t_elevator" value="'.$elevator.'"></input></td>';
    		        echo '<td class="tdcol">结构:</td>';
    		        echo '<td class="tdcontent"><input type="text" class="tdinput" style="width:50%;" name="t_structure" value="'.$structure.'"></input></td>';
		        echo '</tr>';
		        echo '<tr class="querytable_tr">';
    		        echo '<td class="tdcol">询价人:</td>';
    		        echo '<td class="tdcontent"><input list="xjr" name="t_xjr" style="width:50%;" class="tdinput" value="公司外部"></input></td>';
    		        echo '<td class="tdcol">应价人:</td>';
    		        echo '<td class="tdcontent"><input type="text" name="t_offer" style="width:50%;" class="tdinput" value="林晓"></input></td>';
					echo '<td class="tdcontent" colspan="2" style="text-align: center"><input type="submit" class="submitbutton" value="提交报价" width="100%"></input></td>';
		        echo '</tr>';
				echo '<INPUT TYPE=hidden NAME="offer_class" VALUE="估价师报价">';
		    echo '</table>';
		}
	}
?>