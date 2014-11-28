window.bot_colormap = {
    'rp1.solalla.ardyh':'#FF0000',
    'rp2.solalla.ardyh':'#00FF00',
    'rpi3.solalla.ardyh':'#3366FF',
    'monitor.solalla.ardyh':'#FFFF00',
    'ctenophore.solalla.ardyh':'#FF00FFf',
    'default':'#FFFFFF'
}
window.LOG_PAUSED=false;

function updateSensorValues(sensor_values){
    /*
    Input
    sensor_values - A list of lists with each inner of the from [PORTNAME, VALUE]
                    PORTNAME in 'PORT_1',..., 'PORT_4'

    */

    var sensor_package = sensor_values.bot_package // This needs to be fixed.
    
    $el = $("#sensor-values");
    for (var key in sensor_values){
       var val = sensor_values[key]
       $el.find("."+key).html(val);
    }

    if (sensor_package === 'grovebot') {


        var acc_xyz_verbose  = "NaN"; 
        if(sensor_values.acc_xyz && sensor_values.acc_xyz.length>0) {
            acc_xyz_verbose= sensor_values.acc_xyz.join(", ");
        }
        
        $(".grovebot-temp").html(sensor_values.temp+"&deg;C");
        $(".grovebot-humidity").html(sensor_values.humidity);
        $(".grovebot-light").html(sensor_values.light);
        $(".grovebot-sound").html(sensor_values.sound);
        $(".grovebot-touch").html(sensor_values.touch);
        $(".grovebot-slider").html(sensor_values.slider);
        $(".grovebot-dist").html(sensor_values.dist);
        $(".grovebot-acc_xyz").html(acc_xyz_verbose);
        $(".grovebot-pir").html(sensor_values.pir);
        
        // $(".grovebot-button").html(sensor_values.button);
    
    }

}


Lilybot = function(){
    /*
    This object handles all commands for the raspberry pi lilybot.
    There needs to be a seperate one for ctenophore. 

    */
    var self = this;
        
    this.startCamera = function(){
        var message = {
            command:"start-camera-1",
            kwargs:{}
        }
        this.send(message);
    };

    this.stopCamera = function(){
        var message = {
            command:"stop-camera-1",
            kwargs:{}
        }
        this.send(message);
    };

    this.shutdown = function(){
        var message = {
            command:"shutdown",
            kwargs:{}
        }
        this.send(message);
    };

    this.restart = function(){
        var message = {
            command:"restart",
            kwargs:{}
        }
        this.send(message);
    };

    this.target = function(index){
        var message = {
            command:"target",
            kwargs:{index:index}
        }
        this.send(message);
    };

    this.clearTarget = function(){
        var message = {
            command:"clearTarget",
            kwargs:{}
        }
        this.send(message);
    };

    this.forward = function(){
        var message = {
            command:"forward",
            kwargs:{}
        }
        this.send(message);
    };

    this.reverse = function(){
        var message = {
            command:"reverse",
            kwargs:{}
        }
        this.send(message);
    };

    this.steer_left = function(){
        var message = {
            command:"steer_left",
            kwargs:{}
        }
        this.send(message);
    }

    this.steer_right = function(){
        var message = {
            command:"steer_right",
            kwargs:{}
        }
        this.send(message);
    }

    this.nudge_left = function(){
        var message = {
            command:"nudge_left",
            kwargs:{}
        }
        this.send(message);
    }

    this.nudge_right = function(){
        var message = {
            command:"nudge_right",
            kwargs:{}
        }
        this.send(message);
    }

    this.stop = function(){
        var message = {
            command:"stop",
            kwargs:{}
        }
        this.send(message);
    }   


    this.look_up = function(){
        var message = {
            command:"look_up",
            kwargs:{}
        }
        this.send(message);
    };

    this.look_down = function(){
        var message = {
            command:"look_down",
            kwargs:{}
        }
        this.send(message);
    }

    this.send = function(message){
        var out = JSON.stringify(message);
        ardyh.socket.send(out);
    };

};  // End lilybot



Ardyh = function(handshake_message){
    /*
    Object to handle websocket connections and message passing and logging. 
    
    Params
    handshake_message - [Object] The initial handshake message to use when connecting to ardyh. 

    */
    var self = this;
    this.handshake_message = handshake_message;
    this.DOMAIN = "162.243.146.219:9093"
    this.camera_url = "http://192.168.1.103:8081"
    this.lilybot = new Lilybot();
    this.host = "";
    this.socket = null;
    this.nlogs = 0;
    this.max_nlogs = 1000;

    this.setup = function(){
        // Creates the websocets connection{
        this.host =  'ws://'+ this.DOMAIN +'/ws?' + self.handshake_message.bot_name;      // combines the three string and creates a new string
        //self.host =  "ws://"+ self.DOMAIN +"/ws?jjbot.solalla.ardyh";      // combines the three string and creates a new string
        self.socket = new WebSocket(self.host);
              
        // event handlers for websocket
        if(self.socket){
            self.socket.onopen = function(){
                console.log("connection opened....");
                
                
                var out = JSON.stringify(handshake_message);
                self.socket.send(out);
            }

            self.socket.onmessage = function(msg) {
                /*
                Listens for

                - sensor_values
                - new - This should have a camera IP address un the keyword 'camera_url'. 
                */
                

                try {
                  var data = JSON.parse(msg.data);
                  message = data.message;
                  bot_name = data.bot_name
                  if ('sensor_values' === message.command) updateSensorValues(message.kwargs, message.sensor_package)
                  if ('new' in data) self.newConnection(data);

                } catch (e) {
                    self._log("[Ardyh.onmossage()] Message in the wrong format.")
                    self._log(msg.data)
                }
                

                if(!LOG_PAUSED){
                     self._log(msg.data,bot_name);
                }
            }

            self.socket.onclose = function(){
                //alert("connection closed....");
                self._log("The connection has been closed.");
                self.showReadyState("closed");
                this.socket = new WebSocket(self.host);
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
    this._log = function (txt, bot_name){
        $log = $("#log");
        if ($log.length === 0) return;
        if(typeof(bot_name)==='undefined'){
            bot_name = 'default'
        }
        var color = bot_colormap[bot_name]
        $newRow = $("<div style='color:"+color+";'>");
        $newRow.text(txt);
        $log.append($newRow);
        $log.scrollTop($log[0].scrollHeight);
        self.nlogs++;
        if (self.nlogs > self.max_nlogs){
            $log.find("div").eq(0).detach();
        }
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
    };

    this.startCamera = function(){
        /* 
        Powers up the camera and sends the stream to the #camera-1.
        */
        this.lilybot.startCamera();
    };

    this.refreshCamera = function(){
        $("#camera-1").html("");

        // This is the camera feed in the broswer. Should be moved to a view
        self.webcam = new Webcam($("#camera-1"), self.camera_url)
        self.webcam.createImageLayer();
        resize();
    };

    this.stopCamera = function(){
        /* Shutsdown the camera. */
        this.lilybot.stopCamera();
    };

    this.shutdown = function(){
        this.lilybot.shutdown();
    };

    this.restart = function(){
        this.lilybot.restart();
    };

    this.target = function(index){
        this.lilybot.target(index);
    };

    this.clearTarget = function(){
        this.lilybot.clearTarget();
    };


    this.pauseLog = function(){
        console.log("Not implemented");
          if(LOG_PAUSED===true){
            LOG_PAUSED = false;
            $('.pauseBtn').html('Pause');
          } else{
            LOG_PAUSED = true;
            $('.pauseBtn').html('Unpause');
          }     
    };

    this.getBotsList = function(callback){
        url = "http://" + this.DOMAIN + "/bots-list";
        $.get(url, function(res){
            console.log(res);
            callback(res);
        }, 'json');
    };

}; // End Ardyh



/*******************************************


/****************************************************
View Stuff
*****************************************************/


ControlsView = function($el){
    var self = this;

    this.lilybot = new Lilybot();

    if (typeof($el) === "undefined") this.$el = $(".controls");

    // Add listeners
    $(".startCameraBtn").click(function(e){ ardyh.startCamera(); });
    $(".refreshCameraBtn").click(function(e){ ardyh.refreshCamera(); });
    $(".stopCameraBtn").click(function(e){ ardyh.stopCamera(); });
    $(".lookupBtn").click(function(e){ self.lilybot.look_up(); });
    $(".lookdownBtn").click(function(e){ self.lilybot.look_down(); });
    
    $(".restartBtn").click(function(e){ ardyh.restart(); });
    $(".shutdownBtn").click(function(e){ ardyh.shutdown(); });
    
    $(".forwardBtn").click(function(e){ self.lilybot.forward(); });
    $(".stopBtn").click(function(e){ self.lilybot.stop(); });
    $(".reverseBtn").click(function(e){ self.lilybot.reverse(); });
    $(".nudgeLeftBtn").click(function(e){ self.lilybot.nudge_left(); });
    $(".nudgeRightBtn").click(function(e){ self.lilybot.nudge_right(); });
    $(".steerLeftBtn").click(function(e){ self.lilybot.steer_left(); });
    $(".steerRightBtn").click(function(e){ self.lilybot.steer_right(); });

    $(".pauseBtn").click(function(e){ ardyh.pauseLog(); });

    $(".refreshBotsBtn").click(function(){
        /*
        Refreshes the connected bots list.
        */
        ardyh.getBotsList(function(res){
            
            var html = '';
            for (i in res){
                var bot_name = res[i].bot_name;
                html +="<div><div class='circle' style='background-color:"+bot_colormap[bot_name]+";'></div>"+bot_name+'</div>';
                for (j in res[i].subscriptions) {
                    html += '<div><small>'+res[i].subscriptions[j]+'</small></div>';
                }
                html += '<hr>';
            }
            $("#bots-list").html(html);
        });
    });
    

    $(".targetBtn").click(function(e){ 
        target_index = $("[name=target_index]").val();
        ardyh.target(target_index); 
        $(".targetBtn").hide();
        $(".clearTargetBtn").show();
    });

    $(".clearTargetBtn").click(function(e){ 
        ardyh.clearTarget();
        $(".clearTargetBtn").hide();
        $(".targetBtn").show();
    });


    // Lilybot butotns listeners
    document.onkeyup = keyCheck;       
    function keyCheck(){
       var keyID = event.keyCode;
       switch(keyID)
        {
            // WoW style keyboard mappings
            case 81: // q
                self.lilybot.nudge_left();
            break; 
            case 69:
                self.lilybot.nudge_right();
            break;
            case 65:
                self.lilybot.steer_left();
            break;
            case 68:
                self.lilybot.steer_right();
            break;
            case 87:
                self.lilybot.forward();
            break;
            case 83:
                self.lilybot.stop();
            break;
            case 88:
                self.lilybot.reverse();
            break;

            case 38:
                self.lilybot.look_up();
            break;
            case 40:
                self.lilybot.look_down();
            break;

       }
    }  // end keyCheck()
};




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
    videoW = (0.7*W);
    videoH = videoW/aspect_ratio;

    $("#camera-1").width(videoW);
    $("#camera-1").height(videoH);

    //$("#camera-1").height(H - $(".top-bar").height() );
    
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
        var src = self.url + "/?action=snapshot&n=" + (++self.imageNr)
        console.log(src);
        img.src = src;
        
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
