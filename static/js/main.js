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
					var json_data = this.responseText;
					var json_obj = JSON.parse(json_data);
					document.getElementById("TempHum_id").innerHTML = json_obj.tempHum
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

function sendEvent(value)
{
	var request = new XMLHttpRequest();
	request.onreadystatechange = function()
	{
		if(this.readystate === 4)
		{
			if(this.status === 200)
			{
				if(this.responseText !== null)
				{
				}
			}
		}
	};
	request.open("POST", "status=" + value, true);
	request.send(null);
}



function handleClick(cb)
{
	if(cb.checked){
		value = "ON";
	}
	else{
		value = "OFF";
	}
	sendEvent(cb.id + "-" + value);
}
