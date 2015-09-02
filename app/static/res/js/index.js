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
	
	var redis_info = {};
	redis_info['host'] = host;
	redis_info['port'] = port;
	redis_info['password'] = password;
	redis_info['email'] = email;
	redis_info['time'] = new Date().Format("yyyy-MM-dd hh:mm:ss");
	redis_info['timestamp'] = Date.parse(new Date());
	
	var key = 'redis_' + _redis_md5(redis_info);
	simpleStorage.set(key, redis_info, 0);
	redis_servers.push(redis_info);
	sort_redis_server();
	
	add_onerow_2_table(redis_info);
	$('form')[0].reset();
}

//删除redis
function del_redis_btn_click(redis_md5) {
	var redis_key = 'redis_' + redis_md5
	simpleStorage.deleteKey(redis_key);
	$('#' + redis_md5).remove();
} 


//清空table信息
function _flush_table() {
	$('#redis_table tbody td').remove();
}

//添加一行redis信息
function add_onerow_2_table(redis) {
	var table = $('#redis_table tbody tr:nth(0)');
	var md5_key = _redis_md5(redis);
	//删除已经存在的tr
	$('#' + md5_key).remove();
	var html = '<tr id="'+md5_key+'"><td bgcolor="#FFFFCC"><a href="/redis/'+ md5_key +'.html">' + redis['host'] + ':' + redis['port'] + '    alert to ' + (redis['email'] || 'nobody') + '</a></td><td bgcolor="#FFFFCC">'+redis['time']+'</td><td><input type="button" value="删除" onclick="del_redis_btn_click(\''+ md5_key +'\')" /></td></tr>';
	table.after(html);
}

//填充table信息
function fill_redis_table() {
	_flush_table();
	var redis = null;
	for (var i in redis_servers) {
		redis = redis_servers[i];
		add_onerow_2_table(redis);
	}
}
load_all_redis_from_storage();
fill_redis_table();