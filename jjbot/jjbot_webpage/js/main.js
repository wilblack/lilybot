// These are updates on button clicks
var up;
var down;
var left;
var right;
var brakes;

function accelerate()       // defines a variable that controls the forward movement
{
    up = "u";               // when up == u the bot moves forward 
    down = "aaa";left = "aaa";right = "aaa";brakes = "aaa";       // When up button is pressed other buttons(variables) should be turned off.
    ardyh.socket.send("u");   
}  

function reverse(){
    down = "d";
    up = "aaa";left = "aaa";right = "aaa";brakes = "aaa";
    ardyh.socket.send("d");  
}

function steer_left(){
    left = "l";
    up = "aaa";down = "aaa";right = "aaa";brakes = "aaa";
    ardyh.socket.send("l");  
}

function steer_right(){
    right = "r";
    up = "aaa";down = "aaa";left = "aaa";brakes = "aaa";
    ardyh.socket.send("r");
}

function nudge_left(){
    ardyh.socket.send("nl");  
}

function nudge_right(){
    ardyh.socket.send("nr");
}



function stop(){
    up = "aaa";down = "aaa";left = "aaa";right = "aaa";brakes = "b";
    ardyh.socket.send("b");
}        


function shutdown(){
    ardyh.socket.send("x");
} 


function restart(){
    ardyh.socket.send("y");
} 


function lookLeft(){
  ardyh.socket.send("ll");
}

function lookLeft(){
  ardyh.socket.send("lr");
}

function connectBtnCallback(){
  /*
   * This should establish a new connection
   */

   setup2()

}

function showReadyState(state){
  $el =  $("#ready-state");
  $el.find("span").hide();
  $("#ready-state ."+state).show();
}


function setup2(){
    // Creates the websocets connection{
    var $txt = $("#hostname");      // assigns the hostname(hostname/ip address) entered in the text box
    var name = $txt.val();
    var host =  "ws://"+name+":9093/ws";      // combines the three string and creates a new string
    window.socket = new WebSocket(host);
    
    var $btnSend = $("#sendtext");
    $btnSend.on('click',function(){
      var text = $txt.val();
        if(text == ""){
         return;
        }
        $txt.val("");
      }); 
      $txt.keypress(function(evt){
          if(evt.which == 13) $btnSend.click();
      });

    // event handlers for websocket
    if(socket){
        var count =1;
        socket.onopen = function(){
            count = 0;
            console.log("connection opened....");
            arrows();     // function for detecting keyboard presses
            buttons();    // function for detecting the button press on webpage
            showReadyState("open");
    }


     socket.onmessage = function(msg) {
        try {
          var data = JSON.parse(msg.data);
          if ('sensor_values' in data) updateSensorValues(data.sensor_values)
        } catch (e) {
          showServerResponse(msg.data);
        }
     }

     socket.onclose = function(){
        //alert("connection closed....");
        showServerResponse("The connection has been closed.");
        showReadyState("closed");
     }

     socket.onerror = function(){
        //alert("connection closed....");
        showServerResponse("The was an error.");
        showReadyState("error");
     }

    }
    
    else
    {
      console.log("invalid socket");
    }

    function showServerResponse(txt){
        $log = $("#log");
        $newRow = $("<div>");
        $newRow.text(txt);
        $log.append($newRow);
        $log.scrollTop($log[0].scrollHeight);
    }   
        
}   

function updateSensorValues(sensor_values){
    /*
    Input
    sensor_values - A list of lists with each inner of the from [PORTNAME, VALUE]
                    PORTNAME in 'PORT_1',..., 'PORT_4'

    */
    
    $el = $("#sensor-values");
    for (var i in sensor_values){
       var port = sensor_values[i][0]
       $el.find("."+port).html(sensor_values[i][1]);
    }

    }   

function buttons() { 
    if(up== "u") {
      ardyh.socket.send("u");
    }   
    
    if(down== "d") {
      ardyh.socket.send("d");
    }
    
    if(left== "l") {
      ardyh.socket.send("l");
    }   
    
    if(right== "r") {
      ardyh.socket.send("r");
    }   
    
    if(brakes == "b") {
      ardyh.socket.send("b");
    }
}


function arrows() {
    document.onkeyup = KeyCheck;       
    function KeyCheck(){
       var KeyID = event.keyCode;
       switch(KeyID)
       {
            case 16:
            ardyh.socket.send("b");
            break; 
            case 17:
            ardyh.socket.send("b");
            break;
            case 37:
            ardyh.socket.send("l");
            break;
            case 38:
            ardyh.socket.send("u");
            break;
            case 39:
            ardyh.socket.send("r");
            break;
            case 40:
            ardyh.socket.send("d");
            break;

            // WoW Style
            case 32: // x
            ardyh.socket.send("b");
            break; 
            case 88: // x
            ardyh.socket.send("d");
            break; 
            case 65: // a
            ardyh.socket.send("l");
            break;
            case 87: // w
            ardyh.socket.send("u");
            break;
            case 68: // d
            ardyh.socket.send("r");
            break;
            case 83: // s
            ardyh.socket.send("b");
            break;

            case 81: // q
            ardyh.socket.send("nl");
            break;
            case 69: // e
            ardyh.socket.send("nr");
            break;



       }
    }
}



Ardyh = function(){
    /*
    Object to handle websocket connections and message passing and logging. 

    */
    var self = this;
    this.DOMAIN = "173.255.213.55:9093"



    this.setup = function(){
    // Creates the websocets connection{

        this.host =  "ws://"+ this.DOMAIN +"/ws";      // combines the three string and creates a new string
        this.socket = new WebSocket(this.host);
              
        // event handlers for websocket
        if(self.socket){
            self.socket.onopen = function(){
                console.log("connection opened....");
                arrows();     // function for detecting keyboard presses
                buttons();    // function for detecting the button press on webpage
                self.showReadyState("open");
            }

            self.socket.onmessage = function(msg) {
                try {
                  var data = JSON.parse(msg.data);
                  if ('sensor_values' in data) updateSensorValues(data.sensor_values)
                } catch (e) {
                  self._log(msg.data);
                }
            }

            self.socket.onclose = function(){
                //alert("connection closed....");
                self._log("The connection has been closed.");
                self.showReadyState("closed");
             }

            self.socket.onerror = function(){
                //alert("connection closed....");
                self._log("The was an error.");
                self.showReadyState("error");
             }
        } else {
            self.self._log("invalid socket");
        }

        } // End setup()

    this._log = function (txt){
        $log = $("#log");
        $newRow = $("<div>");
        $newRow.text(txt);
        $log.append($newRow);
        $log.scrollTop($log[0].scrollHeight);
    };

    this.showReadyState = function(state){
       $el =  $("#ready-state");
       $el.find("span").hide();
       $("#ready-state ."+state).show();
    };

}; // End Ardyh

$(document).ready(function(){
    ardyh = new Ardyh();
    ardyh.setup();
});






function resize(){
    var H = $(window).height();
    var primaryH = $("#primary").height();
    var footerH = $("#footer").height();    
    var secondaryH = H - primaryH - footerH;

    console.log("window height "+H);
    console.log("primary height "+primaryH);
    console.log("secondary height "+secondaryH);

    $("#secondary").height(secondaryH);
}