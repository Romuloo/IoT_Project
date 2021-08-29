
var alive_second = 0;
var heartbeat_rate = 5000;

var myChannel = "SD3a";

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

function handleClick(cb)
{
	if(cb.checked){
		value = true;
	}
	else{
		value = false;
	}
	var btnStatus = new Object();
	btnStatus[cb.id] = value;
	var event = new Object();
	event.event = btnStatus;
	console.log("Calling publishUpdate from handleClick");
	publishUpdate(event, myChannel);
}

pubnub = new PubNub({
	publishKey: "pub-c-213e5f7e-5e67-4544-8cac-70904aea009c",
	subscribeKey: "sub-c-6919a660-226c-11eb-90e0-26982d4915be",
	uuid: "48f860ca-07f3-11ec-9a03-0242ac130003"
});

pubnub.addListener({
        status: function(statusEvent) {
            if (statusEvent.category === "PNConnectedCategory") {
            //    publishSampleMessage();
            }
        },
        message: function(msg) {
          var msg = msg.message;
          console.log(msg);
          document.getElementById("TempHum_id").innerHTML = msg["tempHum"];
        },
        presence: function(presenceEvent) {
            // This is where you handle presence. Not important for now :)
        }
    })

pubnub.subscribe({
        channels: [myChannel]
    });

function  publishUpdate(data, channel){
	pubnub.publish({
		channel: channel,
		message: data
	},
		function (status, response) {
			if (status.error) {
				console.log(status)
			} else {
				console.log("Message published with timetoken", response.timetoken)
			}
		}
	);
}

function logout(){
	console.log("Logging out and unsubscribing");
	pubnub.unsubscribe({
		channel: [myChannel]
	})
	location.replace("/logout")
}
