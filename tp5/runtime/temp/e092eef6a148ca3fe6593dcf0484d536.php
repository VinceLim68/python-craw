<?php if (!defined('THINK_PATH')) exit(); /*a:2:{s:66:"C:\wamp64\www\tp5\public/../application/evalu\view\test\index.html";i:1496111199;s:65:"C:\wamp64\www\tp5\public/../application/evalu\view\evalubase.html";i:1496124292;}*/ ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>大叔报价</title>
    <link rel="stylesheet" type="text/css" href="__CSS__/bootstrap.min.css">
    <link href="//netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="__CSS__/evalu.css">
</head>
<body>

	<nav class="navbar navbar-inverse">
		<div class="container-fluid">
			<div class="navbar-header">
				<span class="navbar-brand"> <a
					href="<?php echo url('evalu/index/geturl'); ?>">大叔报价</a>
				</span>
				<ul class="nav navbar-nav">
					<li><a href="http://www.kancloud.cn/manual/thinkphp5/118003"
						target="_blank"> <i class="fa fa-w fa-file-code-o"></i> TP5文档
					</a></li>
					<li><a href="http://v3.bootcss.com/" target="_blank"> <i
							class="fa fa-w fa-pencil"></i> BS文档
					</a></li>
					<li><a href="http://fontawesome.dashgame.com/" target="_blank">
							<i class="fa fa-w fa-hand-o-right"></i> 图标库
					</a></li>

				</ul>
			</div>

			<form method="post" class="navbar-form navbar-left" action="">
				<div class="form-group has-feedback">
					<input type="text" class="form-control" placeholder="请输入小区名称"
						name="searchfor" style="width: 350px;">
					<span class="glyphicon glyphicon-search form-control-feedback"
						aria-hidden="true"></span>
				</div>
			</form>
		</div>
	</nav>

	
<form  class="form-horizontal" id="form" action="" method="post">
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">修改密码</h3>
        </div>
        <div class="panel-body">
            <div class="form-group">
                <label for="" class="col-sm-2 control-label">原始密码</label>
                <div class="col-sm-9">
                    <input  type="text" name="admin_password"  class="form-control" placeholder="请填写原始密码">
                </div>
            </div>
            <div class="form-group">
                <label for="" class="col-sm-2 control-label">新密码</label>
                <div class="col-sm-9">
                    <input  type="text" name="new_password"  class="form-control" placeholder="请填写新密码">
                </div>
            </div>
            <div class="form-group">
                <label for="" class="col-sm-2 control-label">确认密码</label>
                <div class="col-sm-9">
                    <input  type="text" name="confirm_password"  class="form-control" placeholder="请填写确认密码">
                </div>
            </div>
        </div>
    </div>
    <button class="btn btn-primary" type="submit">确定</button>
</form>


	<script src="__JS__/jquery.min.js"></script>
	<script src="__JS__/bootstrap.min.js"></script>
</body>
</html>