'user strict';

angular.module('homeMonitor')
.directive('botGraphs', function($rootScope, $ardyh){
    return{
        scope:{
            botName: "=",
            values: "=",
            showFilters: "=?"

        },
        controller: function($scope, $ardyh){
            $scope.dtFormat = 'hh:mm:ss tt, ddd MMM dd, yyyy';

            $scope.onMessageListner = null;
            $scope.onMessageCallback = function(e, data){
                console.log("[botGraphs controller ardyh-onmessage]", data);
                if (data.topic !== $scope.botName) return;
                //$rootScope.$apply(function(){
                    //obj.bots.rpi.values.push(data.payload);
                //});
                $scope.newValueCallback('rpi1', data.payload);
            }

            $scope.fetchValues = function(start){

                $ardyh.fetchValues($scope.botName, start)
                    .then(function(data, status){
                        if ($scope.onMessageListener) {
                            $scope.onMessageListener();
                            $scope.onMessageListerner = null;
                        }
                        var results = data.results;

                        $scope.numValues = results.length;
                        $scope.start = results[0][0] * 1000;
                        $scope.end = results[$scope.numValues-1][0] * 1000;
                        $scope.loadValues(results);
                        if (!$scope.onMessageListener){
                            $scope.onMessageListener = $rootScope.$on('ardyh-onmessage', $scope.onMessageCallback);
                        }
                    }, function(data, status){
                        console.log("fail");
                    });
            };


            $scope.loadValues = function(values){
                $scope.wtf.multiChart = angular.copy($scope.emptyMultiChart);
                angular.forEach(values, function(row){
                    if (row[1] === null) return;
                    out = {
                        temp:row[1],
                        humidity: row[2],
                        light: row[3],
                        lux: row[4],
                        timestamp: row[0] * 1000 // Need to multi by 1000 to get milliseconds
                    }
                    $scope.newValueCallback(self.botName, out);
                });
                $scope.wtf.multiChartOptions.chart.xDomain = [$scope.start, $scope.end];
                $scope.wtf.multiChartOptions.chart.forceX = [$scope.start, $scope.end];
                //$scope.api.updateWithData($scope.wtf.multiChart);
                //console.table($scope.wtf.multiChart[0].values);
                //$scope.api.clearElement();

            };

            $scope.newValueCallback = function(bot, values){
               // This cleans the data and pushes it to the list.
               var current = {};
               current.temp = !isNaN(values.temp) ? values.temp : null;
               current.humidity = !isNaN(values.humidity) ? values.humidity : null;
               current.light = !isNaN(values.light) ? values.light : null;
               current.lux = !isNaN(values.lux) ? values.lux : null;
               console.log("Converting from ", values.timestamp.toString());
               current.timestamp = new Date(values.timestamp);//.toString($scope.dtFormat);

               // Process temp
               if (current.temp !== null) {
                    var temp = parseFloat(current.temp, 10);
                    if (isNaN(temp)) console.log("NaN",current.temp);
                    $scope.wtf.multiChart[0].values.push({x:current.timestamp, y:temp});
               } else {
                   $scope.wtf.multiChart[0].values.push({x:current.timestamp, y:NaN});
               };

                // Process humidity
                if (current.humidity !== null) $scope.wtf.multiChart[1].values.push({x:current.timestamp, y:current.humidity});

                // Process light
                if ( current.light !== null ) {
                    console.log("[botGraphs] "+ $scope.botName +" we have light", current.light )
                    $scope.wtf.multiChart[2].values.push({x:current.timestamp, y:current.light});
                } else if (current.lux !== null) {
                    console.log("[botGraphs] "+ $scope.botName +" we have lux", current.lux )
                    $scope.wtf.multiChart[2].values.push({x:current.timestamp, y:current.lux});
                }
                //$scope.api.refresh();

                //obj.bots[bot].values.push(entity);
                console.log("newValueCallback: ", bot);
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

            scope.emptyMultiChart = [
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
                    'type':'line',
                    'yAxis':2,
                    'values': []
                }
            ];
            scope.wtf = {};
            scope.config = {
                refreshDataOnly: true, // default: true
                deepWatchOptions: true, // default: true
                deepWatchData: true, // default: true
              };
            scope.wtf.multiChartOptions = {
                chart: {
                    'type': 'multiChart',
                    'height': 350,
                    'margin' : {
                        top: 30,
                        right: 40,
                        bottom: 50,
                        left: 40
                    },
                    'color': d3.scale.category10().range(),
                    //useInteractiveGuideline: true,
                    'transitionDuration': 500,
                    'interpolate': 'linear',
                    'xScale' : d3.time.scale(),
                    'xDomain': [1456802842000, 1457321265000 ],
                    'forceX': [1456802842000, 1457321265000 ],
                    'xAxis': {
                        'showMaxMin': true,
                        'tickFormat': function(d){
                            return scope.xAxisTickFormatFunction()(d);
                        }
                    },
                    'xRange': null,
                    'yAxis1': {
                        tickFormat: function(d){
                            return d3.format(',.1f')(d);
                        }
                    },
                    'yDomain1': [0, 100],
                    'yAxis2': {
                        tickFormat: function(d){
                            return d3.format(',.1f')(d);
                        }
                    }
                }
            };


            scope.graphs = emptyGraphs;
            scope.wtf.multiChart = scope.emptyMultiChart;
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
                var start = -days * 24 * 60 * 60;
                //var then = now.addDays(-parseInt(days, 10)).addHours(-7);

                scope.fetchValues(start)

            };

            scope.timeFilterCallback('last-1-days');
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
