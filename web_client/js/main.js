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

function lookRight(){
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



Lilybot = function(){
    var self = this;
        
    this.startCamera = function(){
        ardyh.socket.send("start-camera-1");
    };

    this.stopCamera = function(){
        ardyh.socket.send("stop-camera-1");
    };

};  // End lilybot



Ardyh = function(){
    /*
    Object to handle websocket connections and message passing and logging. 

    */
    var self = this;
    this.DOMAIN = "173.255.213.55:9093"
    this.camera_url = "http://192.168.1.140:8080"
    this.lilybot = new Lilybot();
    this.host = "";
    this.socket = null;


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
                /*
                Listens for

                - sensor_values
                - new - This should have a camera IP address un the keyword 'camera_url'. 
                */

                try {
                  var data = JSON.parse(msg.data);
                  if ('sensor_values' in data) updateSensorValues(data.sensor_values)
                  if ('new' in data) self.newConnection(data);

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

    this.newConnection = function(data){
        /*
        data should have keywrod 'camera_url'
        */
        self.camera_url = data.camera_url;
    }

    this.startCamera = function(){
        /* 
        Powers up the camera and sends the stream to the #camera-1.
        */
        this.lilybot.startCamera();

    }

    this.refreshCamera = function(){
        $("#camera-1").html("");

        // This is the camera feed in the broswer. Should be moved to a view
        self.webcam = new Webcam($("#camera-1"), self.camera_url)
        self.webcam.createImageLayer();
        resize();
    }

    this.stopCamera = function(){
        /* Shutsdown the camera. */
        this.lilybot.stopCamera();
    }

}; // End Ardyh



/*******************************************


/****************************************************
View Stuff
*****************************************************/


ControlsView = function($el){
    var self = this;

    if (typeof($el) === "undefined") this.$el = $(".controls");

    // Add listeners
    this.$el.find(".startCameraBtn").click(function(e){ ardyh.startCamera(); });
    this.$el.find(".refreshCameraBtn").click(function(e){ ardyh.refreshCamera(); });
    this.$el.find(".stopCameraBtn").click(function(e){ ardyh.stopCamera(); });

}




function toggleAbout(){
    $el = $("#about");
    if ($el.hasClass("hide") === true){
        $el.removeClass("hide");
    } else {
        $el.addClass("hide");
    }

}

function resize(){
    var H = $(window).height();
    var W = $(window).width();
    $("#controls .button").height(.12*H);

    var primaryH = $("#primary").height();
    var footerH = $("#footer").height();    
    
    var secondaryH = H - primaryH;

    console.log("window height "+H);
    console.log("primary height "+primaryH);
    console.log("secondary height "+secondaryH);

    $("#secondary").height(secondaryH);
    


    // camera-content stuff.
    var W = $("#content").outerWidth();
    aspect_ratio = 640/480;

    $("#camera-1").width(0.7*W);
    $("#camera-1").height(H - $(".top-bar").height() );
    
    $("#log-wrapper").css("top", $(".top-bar").height() + $("#sensor-values").height());
    $("#log-wrapper, #sensor-values").width(0.7*W);

    var lmt = $("#camera-1").height() - $("#left-panel .controls.top").height() - $("#left-panel .controls.bottom").height()
    $("#left-panel .controls.bottom").css("margin-top",lmt);

    var rmt = $("#camera-1").height() - $("#right-panel .controls.top").height() - $("#right-panel .controls.bottom").height()
    $("#right-panel .controls.bottom").css("margin-top",rmt);
    

}

/****************************************************
Camera Stuff
*****************************************************/

/* Copyright (C) 2007 Richard Atterer, richardÂ©atterer.net
 This program is free software; you can redistribute it and/or modify it
 under the terms of the GNU General Public License, version 2. See the file
 COPYING for details. */


Webcam = function($el, url){
    var self = this;
    this.imageNr = 0; // Serial number of current image
    this.finished = new Array(); // References to img objects which have self.finished downloading
    this.paused = false;

    this.$el = $el;
    this.url = url;

    this.createImageLayer = function() {
        var img = new Image();
        img.style.position = "absolute";
        img.style.zIndex = -1;
        img.onload = self.imageOnload;
        img.onclick = self.imageOnclick;
        img.height = $("#camera-1").height();
        img.src = self.url + "/?action=snapshot&n=" + (++self.imageNr);
        
        var webcam = self.$el[0];
        webcam.insertBefore(img, webcam.firstChild);
    }

    // Two layers are always present (except at the very beginning), to avoid flicker
    this.imageOnload = function() {
        this.style.zIndex = self.imageNr; // Image self.finished, bring to front!

        // Resize the image to fit display
        var H = $("#camera-1").height();
        var W = $("#camera-1").width();
        if (W/H > 1.333333333){
            $("#camera-1 img").height( $("#camera-1").height() );    
        } else {
            $("#camera-1 img").width( $("#camera-1").width() );    
        }
        
        

        while (1 < self.finished.length) {
              var del = self.finished.shift(); // Delete old image(s) from document
              del.parentNode.removeChild(del);
        }
        self.finished.push(this);
            if (!self.paused) self.createImageLayer();
    }

    this.imageOnclick = function() { // Clicking on the image will pause the stream
        self.paused = !self.paused;
        if (!self.paused) self.createImageLayer();
    }

}



$(document).ready(function(){
    ardyh = new Ardyh();
    ardyh.setup();

    controls = new ControlsView();


    resize();
    $(window).resize(function(){
        resize();
    });
});
