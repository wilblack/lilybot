'use strict';

/**
 * @ngdoc directive
 * @name homeMonitor.directive:grovebotPanel
 * @description
 * # grovebotPanel
 */
angular.module('homeMonitor')
.directive('grovebotPanel', [ '$rootScope', function ($rootScope) {
    return {
        templateUrl: 'views/directives/grovebot-panel.html',
        restrict: 'EA',
        scope: {
            botName: "=",
            values: "="
        },
        link: function postLink(scope, element, attrs) {
            scope.units = {'temp': 'f'};
            $rootScope.$on('ardyh-onmessage', function(e, data){
                console.log("[ardyh-onmessage]", data);
                scope.$apply(function(){
                    scope.values = data;
                });
                console.log(scope.messages);
            });

            scope.celsius2fahrenheit = function(t){
                return t*(9/5) + 32;
            };
        }
    };
}]);
