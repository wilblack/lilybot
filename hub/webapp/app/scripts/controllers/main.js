'use strict';

/**
 * @ngdoc function
 * @name webappApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the webappApp
 */
angular.module('homeMonitor')
  .controller('MainCtrl', function ($scope, $ardyh) {
    $scope.page = 'main';
    $scope.messages = [];

    $scope.$on('ardyh-onmessage', function(e, data){
        console.log("[ardyh-onmessage]", data)
        $scope.$apply(function(){
            $scope.messages.push(data);
        })
        console.log($scope.messages)
        
    })


  });
