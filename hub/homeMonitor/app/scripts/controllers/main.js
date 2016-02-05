'use strict';

/**
 * @ngdoc function
 * @name webappApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the webappApp
 */
angular.module('homeMonitor')
  .controller('MainCtrl', function ($scope, $mockArdyh) {
    $scope.page = 'main';
    $scope.messages = [];
    $scope.wtf = {'data': null};




  });
