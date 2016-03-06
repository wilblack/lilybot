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

            $scope.fetchValues = function(){
                $ardyh.fetchValues($scope.botName)
                    .then(function(data, status){
                        var results = data.results;
                        $scope.loadValues(results);
                        $scope.numValues = results.length;
                        $scope.start = results[0][0] * 1000;
                        $scope.end = results[$scope.numValues-1][0] * 1000;

                        if (!$scope.onMessageListener){
                            $scope.onMessageListener = $rootScope.$on('ardyh-onmessage', $scope.onMessageCallback);
                        }
                    }, function(data, status){
                        console.log("fail");
                    });
            };
            if ($scope.botName === 'ardyh/bots/rpi1') {
                $scope.fetchValues();
            }

            
            $scope.loadValues = function(values){
                angular.forEach(values, function(row){
                    if (row[1] === null) return;
                    out = {
                        temp:row[1],
                        humidity: null,
                        light: null,
                        timestamp: row[0] * 1000 // Need to multi by 1000 to get milliseconds
                    }
                    $scope.newValueCallback(self.botName, out);
                });
                //console.table($scope.wtf.multiChart[0].values);
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
                    'type':'line',
                    'yAxis':2,
                    'values': []
                }
            ];

            scope.multiChartOptions = {
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
                    'xAxis': {
                        tickFormat: function(d){
                            return scope.xAxisTickFormatFunction()(d);
                        }
                    },
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
