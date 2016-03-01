'user strict';

angular.module('homeMonitor')
.directive('botGraphs', function($rootScope){
    return{
        scope:{
            botName: "=",
            values: "=",
            showFilters: "=?"
        },
        controller: function($scope){
            $scope.dtFormat = 'hh:mm:ss tt, ddd MMM dd, yyyy';

            $rootScope.$on('ardyh-onmessage', function(e, data){
                console.log("[botGraphs controller ardyh-onmessage]", data);
                if (data.topic !== $scope.botName) return;
                //$rootScope.$apply(function(){
                    //obj.bots.rpi.values.push(data.payload);
                //});
                $scope.newValueCallback('rpi1', data.payload);
            });

            $scope.newValueCallback = function(bot, values){
               // This cleans the data and pushes it to the list.
               var current = {};
               current.temp = values.temp;
               current.humidity = values.humidity;
               current.light = values.light;
               current.timestamp = new Date(values.timestamp);//.toString($scope.dtFormat);

               // Process temp
               if (current.temp !== null) {
                    var temp = parseFloat(current.temp, 10);
                    if (isNaN(temp)) console.log("NaN",val);
                    $scope.wtf.multiChart[0].values.push({x:current.timestamp, y:temp});
               };

                // Process humidity
                if (current.humidity !== null) $scope.wtf.multiChart[1].values.push({x:current.timestamp, y:current.humidity});


                // Process light
                if (current.light !== null) $scope.wtf.multiChart[2].values.push({x:current.timestamp, y:current.light});

               //$scope.api.refresh();

               //obj.bots[bot].values.push(entity);
               console.log("newValueCallback: ", bot);
               console.log($scope.wtf.multiChart[0]);

                //$sensorValues.updateGraphs(entity);
            }

        },
        templateUrl: 'views/directives/bot-graphs.html',
        restrict: 'EA',
        link: function(scope, elem, attrs){

            var emptyGraphs = {
                'temp':[{
                    'key':'Temp (&deg;F)',
                    'values': []
                }],
                'humidity':[{
                    'key':'Humidity',
                    'values': []
                }],
                'light':[{
                    'key':'Light',
                    'values': []
                }]
            };

            var emptyMultiChart = [
                {
                    'key':'Temp (F)',
                    'type': 'line',
                    'yAxis':1,
                    'values': []
                },
                {
                    'key':'Humidity',
                    'type': 'line',
                    'yAxis':1,
                    'values': []
                },
                {
                    'key':'Light',
                    'type':'area',
                    'yAxis':2,
                    'values': []
                }
            ];

            scope.multiChartOptions = {
                chart: {
                    type: 'multiChart',
                    height: 350,
                    margin : {
                        top: 30,
                        right: 40,
                        bottom: 50,
                        left: 40
                    },
                    color: d3.scale.category10().range(),
                    //useInteractiveGuideline: true,
                    transitionDuration: 500,
                    xAxis: {
                        tickFormat: function(d){

                            return scope.xAxisTickFormatFunction()(d);
                        }
                    },
                    yAxis1: {
                        tickFormat: function(d){
                            return d3.format(',.1f')(d);
                        }
                    },
                    yDomain1: [0, 100],
                    yAxis2: {
                        tickFormat: function(d){
                            return d3.format(',.1f')(d);
                        }
                    }
                }
            };


            scope.graphs = emptyGraphs;
            scope.wtf = {multiChart: emptyMultiChart};
            //Grab archived data

            scope.tempColor = function(){
                return function(d, i) {
                    var color = "#408E2F";
                    return color;
                }
            };


            scope.xAxisTickFormatFunction = function(){
                return function(d){
                    return new Date(d).toString("ddd hh:mmt");
                };
            };






            scope.timeFilterCallback = function(value) {
                scope.timestampFilter = value;
                var now = new Date();
                var days = value.split("-")[1];
                var then = now.addDays(-parseInt(days, 10)).addHours(-7);
                console.log("then: ", then.toISOString());
                var filters = {
                    "timestamp_gte":then.toISOString()
                };

                //$sensorValues.fetch(filters)
                //.then(function(data, status){
                //    console.log("successly fetch sensorValues: ", $sensorValues.graphs.temp[0].values.length);
                //    scope.graphs = emptyGraphs;
                //    scope.graphs = $sensorValues.graphs;
                //
                //    scope.wtf.multiChart[0].values = [];
                //    scope.wtf.multiChart[1].values = [];
                //    scope.wtf.multiChart[2].values = [];
                //
                //    _.each($sensorValues.graphs.temp[0].values, function(val){
                //        if (val[1] !== null) {
                //            var y = parseFloat(val[1], 10);
                //            if (isNaN(y)) console.log("NaN",val)
                //            scope.wtf.multiChart[0].values.push({x:val[0], y:val[1]});
                //        }
                //    })
                //    _.each($sensorValues.graphs.humidity[0].values, function(val){
                //        if (val[1] !== null) scope.wtf.multiChart[1].values.push({x:val[0], y:val[1]});
                //    })
                //    _.each($sensorValues.graphs.light[0].values, function(val){
                //        if (val[1] !== null) scope.wtf.multiChart[2].values.push({x:val[0], y:val[1]});
                //    })
                //    $rootScope.$broadcast('sensorvalues-updated');
                //    // scope.MultiGraphs[2].value = scope.graphs.light.values;
                //},function(data, status) {
                //    console.log("failed to fetch sensorValues");
                //});
            };

            scope.timeFilterCallback('last-3-days');
        }
    };
})

.directive('changeDirection', function($sensorValues){
    return{
        scope:{
            previous: "=",
            current: "="
            },
        templateUrl: 'views/partials/change-direction.html',
        restrict: 'EA',
        link: function(scope, elem, attrs){


        }
    };
});
