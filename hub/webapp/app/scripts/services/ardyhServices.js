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

        var data = JSON.parse(msg.data);
        console.log("['onmessage'] ", data);
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


  });
