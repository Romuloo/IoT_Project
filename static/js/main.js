var alive_second = 0;
var heartbeat_rate = 5000;

function keep_alive()
{
	var request  = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if(this.readyState === 4){
			if(this.status === 200){
				if(this.responseText !== null){
					var date = new Date();
					alive_second = date.getTime();
					var keep_alive_data = this.responseText;
					console.log(keep_alive_data);
				}
			}
		}
	};
	request.open("GET", "keep_alive", true);
	request.send(null);
	setTimeout('keep_alive()', heartbeat_rate);
}

function time()
{
	var d = new Date();
	var current_sec = d.getTime();
	if(current_sec - alive_second > heartbeat_rate + 1000)
	{
		document.getElementById("Connection_id").innerHTML = " Dead";
	}
	else
	{
		document.getElementById("Connection_id").innerHTML = " Alive";
	}
	setTimeout('time()', 1000);
}
