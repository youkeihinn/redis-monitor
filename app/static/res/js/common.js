var redis_servers = []; //storeage中所有redis信息

function sort_redis_server() {
	redis_servers = redis_servers.sort(function (a, b) {
        return a['timestamp'] - b['timestamp'];
    });
}


//md5，用于key值
function _redis_md5(redis) {
	return hex_md5(redis['host'] + redis['port']);
}

function _valid_redis_storage(redis_info) {
	if (redis_info.hasOwnProperty('host') && 
			redis_info.hasOwnProperty('port') && 
			redis_info.hasOwnProperty('password')) {
		return true;
	}
	return false;
}

function load_all_redis_from_storage() {
	var keys = simpleStorage.index();
	var len = keys.length;
	for(var i = 0; i < len; i ++) {
		var key = keys[i];
		if (key.startWith('redis_')) {
			var redis_info = get_redis(key);
			if (redis_info) {
				redis_servers.push(redis_info);
			}
		}
	}
	sort_redis_server();
}

function get_redis(key) {
	try {
		var redis_info = simpleStorage.get(key);
	    if (_valid_redis_storage(redis_info)) {
	    	return redis_info;
	    }
	} catch(E) {
        console.log(E);
    }
	//不合法的跳过，并且从storeage中删除
    simpleStorage.deleteKey(key);
    return false;
}


String.prototype.trim = function() {　　
	return this.replace(/(^\s*)|(\s*$)/g, "");　　
}　　
String.prototype.ltrim = function() {　　
	return this.replace(/(^\s*)/g, "");　　
}　　
String.prototype.rtrim = function() {　　
	return this.replace(/(\s*$)/g, "");　　
}
String.prototype.endWith = function(str) {
	if (str == null || str == "" || this.length == 0 || str.length > this.length)
		return false;
	if (this.substring(this.length - str.length) == str)
		return true;
	else
		return false;
	return true;
}
String.prototype.startWith = function(str) {
	if (str == null || str == "" || this.length == 0 || str.length > this.length)
		return false;
	if (this.substr(0, str.length) == str)
		return true;
	else
		return false;
	return true;
}

Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}