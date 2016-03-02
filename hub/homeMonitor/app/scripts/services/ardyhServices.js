'use strict';

/**
 * @ngdoc service
 * @name webappApp.ardyhServices.js
 * @description
 * # ardyhServices.js
 * Service in the webappApp.
 */
angular.module('ardyhServices', [])
  .service('$ardyh', function ($rootScope) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    console.log('[ardyhServices]');

    var obj = this;
    var DOMAIN = "192.168.0.105:9093";
    var SOCKET_URL = "ws://" + DOMAIN + "/ws";
    obj.dtFormat = 'hh:mm:ss tt, ddd MMM dd, yyyy';

    console.log("opening socket connection to " + SOCKET_URL);

    obj.socket = new WebSocket(SOCKET_URL);


    obj.socket.onopen = function(){
        console.log("connection opened....");
        $rootScope.$broadcast('ardyh-onopen');
        var handshake = {"text": "Hello from the browser"};
        var out = JSON.stringify(handshake);
        obj.socket.send(out);
    };

    obj.socket.onmessage = function(msg) {
        /*
            msg should have a JSON string at msg.data.

            data should have keywords 'topic' and 'payload'
        */

        var data = JSON.parse(msg.data);
        console.log("['onmessage'] ", msg);
        $rootScope.$broadcast('ardyh-onmessage', data);
    };

    obj.socket.onclose = function(){
        //alert("connection closed....");
        console.log("The connection has been closed.");
        $rootScope.$broadcast('ardyh-onclose');
    };

    obj.socket.onerror = function(e){
        console.log("The was an error.", e);
        $rootScope.$broadcast('ardyh-onerror', e);

    };


    obj.send = function(messageObj) {
        if (obj.socket.readyState === 1){
            obj.socket.send(JSON.stringify( messageObj));
        } else {
            console.log("Could not send message, ready state = "+obj.socket.readyState);
            if (obj.socket.readyState === 3){
                // Web socket is closed so try to re-establish connection
                console.log("I should reconnect here.");
                $timeout(function(){
                    obj.init(obj.botName);
                }, 5*1000);
            }
        }
    };

    obj.sendCommand = function(command, kwargs){
        kwargs = kwargs || {};
        obj.send({'command':command, 'kwargs':kwargs});
    }







    obj.bots = {};

    obj.bots.rpi1 = {
        botName: "ardyh/bots/rpi1",
        values: [],
    };
    //$rootScope.$on('ardyh-onmessage', function(e, data){
    //
    //    if (data.topic !== obj.bots.rpi1.botName) return;
    //    //$rootScope.$apply(function(){
    //        //obj.bots.rpi.values.push(data.payload);
    //    //});
    //    obj.newValueCallback('rpi1', data.payload);
    //
    //});

   obj.newValueCallback = function(bot, values){
       // This cleans the data and pushes it to the list.
       var current = {};
       current.temp = values.temp;
       current.humidity = values.humidity;
       current.light = values.light || values.lux;

       current.timestamp = new Date(values.timestamp).toString(obj.dtFormat);

       var entity = {
           timestamp: current.timestamp,
           data: current
       };
       obj.bots[bot].values.push(entity);

    }

  });
