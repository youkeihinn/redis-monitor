function add_demo_redis_btn_click() {
	$('#new_host').val('10.246.13.189');
	$('#new_port').val(6379);
	$('#new_password').val('');
	$('#new_email').val('');
	add_redis_btn_click();
}

function ping_redis(host, port, password, email) {
//	loading.show();
	$('form input').attr("disabled","disabled");  
	var ajax = $.ajax({
		type: "POST",
		url: '/api/ping',
		data: {'host': host, 'port': port, 'password': password},
		success: function(data) {
			data.success = 1;
			if (data.success == 1) {
				add_redis(host, port, password, email);
			}
			else {
				$('form input').removeAttr("disabled");
				alert(data.data);
			}
		}, 
		dataType: 'json',
		async: true,
	});
}


//点击添加按钮
function add_redis_btn_click() {
	var host = $('#new_host').val() || '';
	var port = Number($('#new_port').val()) || 6379;
	var password = $('#new_password').val() || '';
	
	var email = $('#new_email').val() || '';
	
	if (host == '') {
		alert('redis 主机IP不能为空！');
		return ;
	}
	
	ping_redis(host, port, password, email);
}

function add_redis(host, port, password, email) {
	var ajax = $.ajax({
		type: "POST",
		url: '/api/add',
		data: {'host': host, 'port': port, 'password': password, 'email': email},
		success: function(data) {
			if (data.success == 1) {
				location.reload();
			}
			else {
				$('form input').removeAttr("disabled");
				alert(data.data);
			}
		}, 
		dataType: 'json',
		async: true,
	});
}

function del_redis(md5) {
	var ajax = $.ajax({
		type: "POST",
		url: '/api/del',
		data: {'md5': md5},
		success: function(data) {
			if (data.success == 1) {
				location.reload();
			}
			else {
				alert(data.data);
			}
		}, 
		dataType: 'json',
		async: true,
	});
}

//删除redis
function del_redis_btn_click(redis_md5) {
	del_redis(redis_md5);
} 