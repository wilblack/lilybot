
function _log(text){
    console.log(text);

    // $(".log").append("<div>"+text+"</div>");
    $(".log").append(text+"\n");
    var textarea = $('.log')[0];
    textarea.scrollTop = textarea.scrollHeight;

}

Robot = function(){
    
    var self = this;
    self.eventType = ""; // The event taht takes place, bump or timed
    self.eventType = ""; // The event taht takes place, bump or timed
    self.path = []; // The path of the robot
    self.map = []; // The robots internal map of the maze

    self.noneCount = 0;
    self.pause = false;
    self.bump = false;
    self.last_bump_counter = 0;
    self.DT = 250;
    self.SHORT = 2;
    self.TIMED_DT = 5;
    self.LOG_POSITION = false;

    // Initial starting coordinates amnd heading
    self.i = 28;
    self.j = 41;
    self.h = 0;
    self.lastPath = {"eventType":"start", 
                     "headingNew":self.h, 
                     "distance":0, 
                     "headingChange":0, 
                     "featureType":"",
                     "coords": [self.i, self.j]
                   };

    self.run = function(){
        self.count=0;
        var event=null;

        // Plot inital location of robot on maze and add initail event to path
        maze.add_dot(self.i,self.j);
        self.logEvent(self.lastPath);

        window.looper = setInterval(function(){
            
            // Check to see if we made it.
            if (self.j === 0) {
                clearInterval(looper);
                _log("GOAL!!!");
                _log(self.path.length+" events");
                _log(self.count+" steps");

            }
            
            if (self.pause === false){
                event = null;
                self.count++;
                self.eventType = "none";

                // Determine event
                self.bump = self.checkBump();
                if (self.bump) self.eventType = 'bump';

                if (self.eventType === 'none'){
                    if (self.noneCount > self.TIMED_DT){
                        // Set heading
                        self.eventType = 'timed';
                    } else {
                        self.noneCount++;
                    }
                }

                if (self.eventType === 'bump'){
                    
                    self.noneCount = 0;
                    
                    // Compute path length
                    self.path_length = self.count - self.last_bump_counter;
                    self.last_bump_counter = self.count; 
                    
                    // Decide direction
                    delta_h = self.getHeadingChange('bump');
                    var old_h = self.h;
                    self.h = (self.h+delta_h)%360;

                    var delta_x = 0//Math.round(Math.sin(self.h*Math.PI/180));
                    var delta_y = 0//-Math.round(Math.cos(self.h*Math.PI/180));
                    
                }


                if (self.eventType === 'timed'){
                    
                    // Decide direction
                    delta_h = self.getHeadingChange('timed');
                    var old_h = self.h;
                    self.h = (self.h+delta_h)%360;

                    var is_wall = self.checkBump();
                    if (is_wall){
                        self.h = old_h;
                    } else {
                        self.noneCount = 0;
                    }

                    var delta_x = Math.round(Math.sin(self.h*Math.PI/180));
                    var delta_y = -Math.round(Math.cos(self.h*Math.PI/180));
                } 

                if (self.eventType === 'none'){
                                    // Update location
                    var delta_x = Math.round(Math.sin(self.h*Math.PI/180));
                    var delta_y = -Math.round(Math.cos(self.h*Math.PI/180));
                }

                
                maze.add_dot(self.i, self.j, maze.TRACK_COLOR);
                self.i = self.i + delta_x;
                self.j = self.j + delta_y;


                // Plot location
                maze.add_dot(self.i, self.j);
                if (self.eventType != 'none') {
                    // Create Event obj
                    self.lastPath = {"eventType":self.eventType, 
                                     "headingNew":self.h,
                                     "headingOld":old_h,
                                     "distance":self.path_length, 
                                     "headingChange":delta_h, 
                                     "coords": [self.i, self.j]
                    };
                    self.logEvent(self.lastPath);
                }
                if (self.LOG_POSITION) _log(self.i +", "+self.j+ " h "+self.h );
            } // end is not Pause
        }, self.DT);

    };

    self.logEvent = function(){

        self.path.push(self.lastPath);
        if (self.lastPath.eventType==='bump'){
            var text = self.lastPath.eventType+" - "
                   +self.lastPath.headingChange+"&deg; - "
                   +self.lastPath.distance+' old h '
                   +self.lastPath.headingOld + "&deg;"
                   +' new h '
                   +self.lastPath.headingNew + "&deg;"; 

            _log(text);    
        }
        
    };

    self.setPause = function(val){
        self.pause = val;
    };

    self.updateMap = function(){

    };

    self.checkBump = function(I, J, h){
        if(typeof(I) === 'undefined'){
            I = self.i;
            J = self.j;
            h = self.h

        }
        // Try to continue on existing path
        var bump = null;

        var delta_x = Math.round(Math.sin(h*Math.PI/180));
        var delta_y = -Math.round(Math.cos(h*Math.PI/180));

        var i = I + delta_x;
        var j = J + delta_y;
        

        // Check for boundary
        if (i===-1 || j===-1 || i===maze.SIZE || j===maze.SIZE ){
            bump = true;
        } else if (maze.board[i][j] === 1){
            bump = true;
        }

        if (bump) self.update_map(i,j,'dot');

        return bump;


    };

    self.getHeadingChange = function(eventType){
        var out;
        
        if (eventType === 'bump'){
            if (self.lastPath.eventType == 'timed') return -self.lastPath.headingChange;

            var featureType = self.getFeatureType();
            if (featureType === 'left-corner'){
                if (self.h === 0){
                    out = 90;
                } else {
                    out = 180;
                }

            } else if (featureType === 'right-corner'){
                if (self.h === 0){
                    out = -90;
                } else {
                    out = 180;
                }
                
            
            } else if (featureType === 'left-u'){
                if (self.h === 270 || self.h === -90){
                    out = -90;
                } else {
                    out = 180;
                }

                     
            } else if (featureType === 'right-u'){
                if (self.h === 270 || self.h === -90){
                    out = 90;
                } else {
                    out = 180;
                }

            } else if (featureType === 'unknown') {
                // Going west, so turn to the left
                if ( (self.lastPath.headingNew+360)%360 === 90) {
                    out = -90;
                } else if ( (self.lastPath.headingNew+360)%360 === 0 || (self.lastPath.headingNew+360)%360 === 180 ){
                    if (Math.random() > 0.5){
                        out = 90;
                    } else {
                        out = -90;
                    }
                } else  {
                    out = 90;
                }
                
            }

            
        } else if (eventType === 'timed'){
            // if going west, turn north (+90)
            // if going south, turn 

            if ( (self.lastPath.headingNew+360)%360 === 90) {
                // if going east turn north, +90
                out = -90;
            } else if ( (self.lastPath.headingNew+360)%360 === 0) {
                out = 0;
            } else if ( (self.lastPath.headingNew+360)%360 === 270) {
                // Going west turn north
                out = 90;
            } else {
                if (Math.random() > 0.5){
                    out = 90;
                } else {
                    out = -90;
                }
            }



        }
        return out;
    };

    self.getFeatureType = function(){
        var out = "unknown";
        var last5 = self.getLastBumps(5);
        if (last5.length < 3) return out;

        // If path is between 2 and 4 entries, just look for corners. 
        if (last5.length < 4){
            rs = self.isCorner(self.getLastBumps(3));
            if (rs) out = rs;
            return out;
        }
        
        // Check for a U
        rs = self.isCorner( [last5[2], last5[3], last5[4]] );
        if (rs) out = rs;

        // UPDATE MAP
        if (out == 'left-corner'){
            self.update_map(self.i-1, self.j-1, out);
        } else if (out == 'right-corner') {
            self.update_map(self.i+1, self.j-1, out);
        }

        if (out){
            // Check for previous corner
            var previousCorner = self.isCorner( [last5[0], last5[1], last5[2]] )
            if (previousCorner && out==='left-corner') {
                out = 'left-u';
                self.update_map(self.i-1, self.j-1, out);
            }
            else if (previousCorner && out==='right-corner') {
                out = 'right-u';
                self.update_map(self.i+1, self.j-1, out);
            }

        } 
        _log("featureType: "+out);
        return out;
        // If it's a corner, check for u
    };


    self.getLastBumps = function(num){
        if (typeof(num) === 'undefined') num=4;
        var endI = self.path.length-1;

        var count = 0;
        var out = [];
        while (out.length < num && (endI > count)){

            var temp = self.path[endI-count];
            if (typeof(temp) != 'undefined'){
                if (temp.eventType === 'bump') out.push(temp);
            }
            count++;
        }
        return out.reverse();
    }


    self.isCorner = function(last3){
        var out = false;
        // Check if it's a left 
        if (self.path_length < self.SHORT 
            && last3[1].eventType === 'bump' 
            && last3[2].eventType === 'bump' 
            ) {
            

            // Was going west, bumped and turned north, and bump immediately
            if ( (last3[2].headingOld === -90 || last3[2].headingOld === 270) 
                  && last3[2].headingNew === 0){
                out = "left-corner";
            
            // Was going north, bumped and turned west, and bump immediately
            } else if (last3[2].headingOld === 0 
                  && (last3[2].headingNew === 270 || last3[2].headingOld === -90)){
                out = "left-corner";
           

            // Was going north, bumped and turned east, and bump immediately            
            } else if (last3[2].headingOld === 0 
                  && last3[2].headingNew === 90 ){
                out = "right-corner";
            

            // Was going east, bumped and turned north, and bump immediately                        
            } else if (last3[2].headingOld === 90 
                  && last3[2].headingNew === 0 ){
                out = "right-corner";
            }
        }// End if bumps
        return out;
    };


    self.update_map = function(x,y,featureType){
        self.map.push({'coords':[x,y], 'feature':featureType});
        _log("Updating map: "+x+", "+y+" - "+featureType);
        maze.map_add(x, y, featureType);
    };

} // End Robot



Maze = function(){

    self = this;
    self.SIZE = 50;
    self.CHIP = 5;
    self.board = new Array();
    self.map_board = new Array();
    self.context = null;

    self.BACKGROUND_COLOR = "rgb(50,50,50)";
    self.WALL_COLOR = "rgb(255,0,0)";
    self.DOT_COLOR = "rgb(0,255,0)";
    self.TRACK_COLOR = "rgb(100,100,255)";
    self.BORDER_COLOR = "rgb(150,150,150)";
    self.MAP_WALL_COLOR = "rgb(255,255,255)";


    self.init = function() {
        // var canvas = document.getElementById("canvas");
        // canvas.width = self.CHIP*(self.SIZE+8);
        // canvas.height = self.CHIP*(self.SIZE+8);
        // if (canvas.getContext) {
        //     self.context = canvas.getContext("2d");
        //     self.context.fillStyle = self.BORDER_COLOR;
        //     self.context.fillRect(self.CHIP*2, self.CHIP*2, self.CHIP*(self.SIZE+4), self.CHIP*(self.SIZE+4));
        // }

        // INITAILIZE MAZE
        var maze = $("#maze");
        self.context = self.render(maze);
        drawStack = new Array();
        for(i=0; i< self.SIZE; i++) {
            self.board[i] = new Array();
            for(j=0; j<self.SIZE; j++) {
                self.board[i][j] = 0;
                self.context.fillStyle = self.BACKGROUND_COLOR;
                self.context.fillRect(self.CHIP*(4+i), self.CHIP*(4+j), self.CHIP, self.CHIP);
            }
        }

        // INITIALIZE MAP
        var map = $("#map");
        self.map_context = self.render(map);
        for(i=0; i< self.SIZE; i++) {
            self.map_board[i] = new Array();
            for(j=0; j<self.SIZE; j++) {
                self.map_board[i][j] = 0;
                self.map_context.fillStyle = self.BACKGROUND_COLOR;
                self.map_context.fillRect(self.CHIP*(4+i), self.CHIP*(4+j), self.CHIP, self.CHIP);
            }
        }        

    };

    self.render = function($el){
        var canvas = $el[0];
        canvas.width = self.CHIP*(self.SIZE+8);
        canvas.height = self.CHIP*(self.SIZE+8);
        if (canvas.getContext) {
            context = canvas.getContext("2d");
            context.fillStyle = self.BORDER_COLOR;
            context.fillRect(self.CHIP*2, self.CHIP*2, self.CHIP*(self.SIZE+4), self.CHIP*(self.SIZE+4));
        }
        return context
    };

    self.load_board_1 = function(canvas){
        
        // Initial U
        self.add_u(20,30,9,9,'down',canvas);
        self.add_u(18, 16, 7, 9, 'right',canvas);
        self.add_wall(18,16,3, 'v',canvas);
        self.add_wall(0,20,15,'h',canvas);


    };

    self.add_dot = function(i, j, color) {
        if (typeof(color) === 'undefined') color = self.DOT_COLOR;
        // Draws a white square at i,j
        // (0,0) is upper left
        self.context.fillStyle = color;
        self.context.fillRect(self.CHIP*(4+i), self.CHIP*(4+j), self.CHIP, self.CHIP);
    };

    self.map_add = function(i, j, featureType) {
        color = self.MAP_WALL_COLOR;
        // Draws a white square at i,j
        // (0,0) is upper left
        self.map_context.fillStyle = color;
        if (featureType == 'dot'){
            self.map_context.fillRect(self.CHIP*(4+i), self.CHIP*(4+j), self.CHIP, self.CHIP);
        }
        else if (featureType == 'right-corner') {
            self.add_wall(i-1,j,2, 'h', 'map');
            self.add_wall(i,j,2,'v','map');
        }

        else if (featureType == 'left-corner'){
            self.add_wall(i,j,2, 'h', 'map');
            self.add_wall(i,j,2,'v','map');
        }
        else if (featureType == 'left-u'){
            var width = robot.lastPath['distance'];
            self.add_u(i,j,width,1,'down', 'map');
        }
        
        else if (featureType == 'rigth-u'){
            var width = robot.lastPath['distance'];
            self.add_u(i-width,j,width,1,'down', 'map');
        }

    };

    self.add_u = function(I,J,width, height, orientation, canvas){
        /*
        PARAMS
        I, J - the coordinates of the upper left corner of the U
        width - width of the U
        height - height of the arms of the U
        orientation - 'up','left', 'right', 'down'
        */
        if (typeof(canvas) === 'undefined') canvas = 'maze';

        switch(orientation) {
            case 'up':
                self.add_wall(I,J,height,'v', canvas);
                self.add_wall(I+width+1,J,height,'v', canvas);
                self.add_wall(I+1,J+height-1,width,'h', canvas);
                break;
            case 'down':
                self.add_wall(I,J,height,'v', canvas);
                self.add_wall(I+width+1,J,height,'v', canvas);
                self.add_wall(I+1,J,width,'h', canvas);
                break;
            case 'left':
                self.add_wall(I,J,height,'h', canvas);
                self.add_wall(I,J+width+1,height,'h', canvas);
                self.add_wall(I,J+1,width,'v', canvas);
                break;
            case 'right':
                self.add_wall(I,J,height,'h', canvas);
                self.add_wall(I,J+width+1,height,'h', canvas);
                self.add_wall(I+height-1,J+1,width,'v', canvas);
                break;
        }

    }

    self.add_wall = function(I,J,length, orientation, canvas){
        /*
         Add a wall at with it's top or left end at i,j

         PARAMS
         i, j - the x,y coodinates of the top or left end of the wall
         length - length of the wall
         orientation - 'h', 'v' (horizontal or vertical)
         */

         if (typeof(canvas) === 'undefined' || canvas == 'maze'){
            var context = self.context;
            var board = self.board;
            var color = self.WALL_COLOR;
         } else {
            var context = self.map_context;
            var board = self.map_board;
            var color = self.MAP_WALL_COLOR;
         }


         if (orientation == 'h' && J >= 0 && I >= 0){
            var j = J;
            for (i=I; i<I+length; i++){
                board[i][j] = 1;
                context.fillStyle = color;
                context.fillRect(self.CHIP*(4+i), self.CHIP*(4+j), self.CHIP, self.CHIP);
            }
         
         } else if (orientation == 'v' && J>=0 && I >= 0){
            var i = I;
            for (j=J; j<J+length; j++){
                board[i][j] = 1;
                context.fillStyle = color;
                context.fillRect(self.CHIP*(4+i), self.CHIP*(4+j), self.CHIP, self.CHIP);
            }
         } // End if orientation
    };

};


Panel = function(){

    var self = this;
    
    self.init = function(){
       
        // Set initial values and show on map
        $("[name=x0]").val(robot.i);
        $("[name=y0]").val(robot.j);
        $("[name=h0]").val(robot.h);
        $("[name=logPosition]").val(robot.LOG_POSITION.toString());
        $("[name=timed_dt]").val(robot.TIMED_DT);

        maze.add_dot(robot.i, robot.j, maze.DOT_COLOR);

        $("[name=logPosition]").change(function(e){
            robot.LOG_POSITION = ($("[name=logPosition]").val() == 'true');
        });


        $("[name=timed_dt]").change(function(e){
            robot.TIMED_DT = parseInt($("[name=timed_dt]").val());
        });


        $(".clear-log").click(function(e){
            self.clearLog();
        });

        // Add listners to update map
        $("[name=x0], [name=y0] ").change(function(e){

            if (maze.board[robot.i][robot.j] === 0){
                maze.add_dot(robot.i, robot.j, maze.BACKGROUND_COLOR);
            }
             // Set inital values and show on map
            robot.i = parseInt($("[name=x0]").val());
            robot.j = parseInt($("[name=y0]").val());
            robot.h = parseInt($("[name=h0]").val());
            
            _log("Setting initial values");
            _log("x0 = "+robot.i + " y0 ="+robot.j+" h0 = "+robot.h);            

            if (maze.board[robot.i][robot.j] === 0){
                maze.add_dot(robot.i, robot.j, maze.DOT_COLOR);
            }
        });
    };


    self.clearLog = function(){
        $(".log").html("");
    }

};
