//我想自己写一个

jQuery(function($) {
	var grid_selector = "#grid-table";
	var pager_selector = "#grid-pager";
	
	var parent_column = $(grid_selector).closest('[class*="col-"]');
	// resize to fit page size窗口变化时，重新渲染jgrid
	$(window).on('resize.jqGrid', function () {
		$(grid_selector).jqGrid( 'setGridWidth', parent_column.width() );
    })
	
	// resize on sidebar collapse/expand侧边栏收放时，重新渲染jgrid
    $(document).on('settings.ace.jqGrid' , function(ev, event_name, collapsed) {
		if( event_name === 'sidebar_collapsed' || event_name === 'main_container_fixed' ) {
			// setTimeout is for webkit only to give time for DOM changes and
			// then redraw!!!
			setTimeout(function() {
				$(grid_selector).jqGrid( 'setGridWidth', parent_column.width() );
			}, 20);
		}
    })
    
	jQuery(grid_selector).jqGrid({

		url : 'getSales', 
		mtype : 'POST',
		datatype : "json", // 请求的数据类型
		
		height: 250,
		colModel: [{
			name: 'id',
			index: 'id',
			hidden: true,
			sorttype: "int",
			edittype:'text',
			editrules:{edithidden:true,required:true},
			formoptions:{ rowpos:1,colpos:1},
			editable: true,
			width: 60,
		}, {
			label: '标题',
			name: 'title',
			index: 'title',
			editable: true,
			edittype:'text',
			width: 350,
			formoptions:{ rowpos:2},
			sortable: true,
			sorttype: "int",
		}, {
			label: '小区id',
			name: 'community_id',
			hidden: true,
			index: 'community_id',
			editable: true,
			editrules:{edithidden:true,required:true},
			edittype:'text',
			formoptions:{ rowpos:3, colpos:2},
			width: 60,
			sortable: true,
			sorttype: "int",
		}, {
			label: '小区',
			name: 'community_name',
			align: 'center',
			edittype:'text',
			formoptions:{ rowpos:3, colpos:1},
			index: 'community_name',
			width: 100,
			editable: true,
		}, {
			label: '户型',
			name: 'spatial_arrangement',
			align: 'center',
			edittype:'text',
			index: 'spatial_arrangement',
			formoptions:{ rowpos:5, colpos:1},
			width: 50,
			editable: true,
		}, {
			label: '层次',
			name: 'floor_index',
			index: 'floor_index',
			align: 'center',
			width: 40,
			edittype:'text',
			editable: true,
			formoptions:{ rowpos:4, colpos:1},
			sortable: true,
			sorttype: "int",
		}, {
			label: '总层',
			name: 'total_floor',
			index: 'total_floor',
			align: 'center',
			width: 40,
			edittype:'text',
			editable: true,
			formoptions:{ rowpos:4, colpos:2},
			sortable: true,
			sorttype: "int",
		}, {
			label: '单价',
			name: 'price',
			formoptions:{ rowpos:6, colpos:1},
			index: 'price',
			editable: true,
			align: 'center',
			edittype:'text',
			sortable: true,
			width: 60,
			sorttype: "int",
		}, {
			label: '建成',
			name: 'builded_year',
			index: 'builded_year',
			align: 'center',
			formoptions:{ label:'建成年份',rowpos:6, colpos:2},
			editable: true,
			edittype:'text',
			width: 40,
			sortable: true,
			sorttype: "int",
		}, {
			label: '面积',
			name: 'area',
			index: 'area',
			editable: true,
			formoptions:{ rowpos:5, colpos:2},
			edittype:'text',
			align: 'center',
			sortable: true,
			width: 40,
			sorttype: "int",
		}, {
			label: '总价',
			name: 'total_price',
			index: 'total_price',
			align: 'center',
			editable: true,
			formoptions:{ rowpos:7, colpos:1},
			edittype:'text',
			width: 40,
			sortable: true,
			sorttype: "int",
		}, {
			label: '优势',
			name: 'advantage',
			index: 'advantage',
			formoptions:{ rowpos:7, colpos:2},
			width: 60,
			editable: true,
			edittype:'text',
		},
	],
		// width :960,
		shrinkToFit:true,
		autowidth : true,
		viewrecords : true,
		rowNum:500,
		rowList:[100,500,1000],
		altRows: true,
		
		pager : pager_selector,
		toppager: true,
		pginput:true,
		
		multiselect: true,
		// multikey: "ctrlKey",
        multiboxonly: true,



		editurl: "./dummy.php",// nothing is saved
		// caption: "jqGrid with inline editing"
		loadtext: "数据加载中...",
		emptyrecords: "没有符合条件的数据",
		
		loadComplete : function() {
			var table = this;
			setTimeout(function() {
				// styleCheckbox(table);
				// updateActionIcons(table);
				updatePagerIcons(table);
				// enableTooltips(table);
			}, 0);
		},	
		
		onPaging:function(){
			var rowNum = jQuery(grid_selector).jqGrid('getGridParam','records');
//			alert(rowNum);
			jQuery(grid_selector).jqGrid('setGridParam', {
				postData: {
					'dontCount': true, 
					'records':rowNum,
					}, 
			});
			//alert('onpaging');
		},



	});
	
	function beforeDeleteCallback(e) {
		var form = $(e[0]);
		if(form.data('styled')) return false;
		
		form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />')
		style_delete_form(form);
		
		form.data('styled', true);
	}
	
	// enable datepicker
	function pickDate( cellvalue, options, cell ) {
		setTimeout(function(){
			$(cell) .find('input[type=text]')
				.datepicker({format:'yyyy-mm-dd' , autoclose:true}); 
		}, 0);
	}
	
	// switch element when editing inline
	function aceSwitch( cellvalue, options, cell ) {
		setTimeout(function(){
			$(cell) .find('input[type=checkbox]')
				.addClass('ace ace-switch ace-switch-5')
				.after('<span class="lbl"></span>');
		}, 0);
	}
	
	// replace icons with FontAwesome icons like above更换翻页图标，不加的话，原来的图标看不见
	function updatePagerIcons(table) {
		var replacement = 
		{
			'ui-icon-seek-first' : 'ace-icon fa fa-angle-double-left bigger-140',
			'ui-icon-seek-prev' : 'ace-icon fa fa-angle-left bigger-140',
			'ui-icon-seek-next' : 'ace-icon fa fa-angle-right bigger-140',
			'ui-icon-seek-end' : 'ace-icon fa fa-angle-double-right bigger-140'
		};
		$('.ui-pg-table:not(.navtable) > tbody > tr > .ui-pg-button > .ui-icon').each(function(){
			var icon = $(this);
			var $class = $.trim(icon.attr('class').replace('ui-icon', ''));
			
			if($class in replacement) icon.attr('class', 'ui-icon '+replacement[$class]);
		})
	}
	
	jQuery(grid_selector).jqGrid('navGrid',pager_selector,
			{ 	// navbar options
				cloneToTop: true,
				edit: true,
				editicon : 'ace-icon fa fa-pencil blue',
				add: true,
				addicon : 'ace-icon fa fa-plus-circle purple',
				del: true,
				delicon : 'ace-icon fa fa-trash-o red',
				search: false,
				searchicon : 'ace-icon fa fa-search orange',
				refresh: true,
				refreshicon : 'ace-icon fa fa-refresh green',
				view: true,
				viewicon : 'ace-icon fa fa-search-plus grey',
			},{
				//edit record form
				closeAfterEdit: true,
				//width: 700,
				recreateForm: true,
				beforeShowForm : function(e) {
					var form = $(e[0]);
					form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />')
					style_edit_form(form);
				}
			},{},{},{},{},{},
	)
	
	function style_edit_form(form) {
		//enable datepicker on "sdate" field and switches for "stock" field
		form.find('input[name=sdate]').datepicker({format:'yyyy-mm-dd' , autoclose:true})
		
		form.find('input[name=stock]').addClass('ace ace-switch ace-switch-5').after('<span class="lbl"></span>');
				   //don't wrap inside a label element, the checkbox value won't be submitted (POST'ed)
				  //.addClass('ace ace-switch ace-switch-5').wrap('<label class="inline" />').after('<span class="lbl"></span>');

				
		//update buttons classes
		var buttons = form.next().find('.EditButton .fm-button');
		buttons.addClass('btn btn-sm').find('[class*="-icon"]').hide();//ui-icon, s-icon
		buttons.eq(0).addClass('btn-primary').prepend('<i class="ace-icon fa fa-check"></i>');
		buttons.eq(1).prepend('<i class="ace-icon fa fa-times"></i>')
		
		buttons = form.next().find('.navButton a');
		buttons.find('.ui-icon').hide();
		buttons.eq(0).append('<i class="ace-icon fa fa-chevron-left"></i>');
		buttons.eq(1).append('<i class="ace-icon fa fa-chevron-right"></i>');		
	}
	
	jQuery("#salesheadsearch").on('submit',function(){
		var myinput = $('#nav-search-input').val();

		alert(myinput);
	});

		
     
})
	