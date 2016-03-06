from time import sleep
from random import randint
from datetime import datetime as dt
from datetime import timedelta
import time
import subprocess
import math

class Db(object):
    
    conn = None;
    step = 30
    ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    filename = '/home/pi/projects/lilybot/hub/sensors.rrd'

    archive = [
            'DS:temp:GAUGE:30:0:100',
            'RRA:AVERAGE:0.5:2:1440',  # 1 minute average for 24 hours
            'RRA:AVERAGE:0.5:10:1440',  # 5 minute averge for 3 days
            'RRA:AVERAGE:0.5:10:1440',  # 10 minute averge for 7 days
            'RRA:AVERAGE:0.5:60:1488',  # 30 minute averge for 31 days
        ]

    # Archives hould be name with boit name in decimal form.
    bots = ['ardyh.bots.rpi1', 'ardyh.bots.rpi3']

    archive2 = [
            'DS:temp:GAUGE:30:0:100',
            'DS:humidity:GAUGE:30:0:100',
            'DS:light:GAUGE:30:0:1200',
            'DS:lux:GAUGE:30:0:1200',
            'RRA:AVERAGE:0.5:2:1440',  # 1 minute average for 24 hours
            'RRA:AVERAGE:0.5:10:1440',  # 5 minute averge for 3 days
            'RRA:AVERAGE:0.5:10:1440',  # 10 minute averge for 7 days
            'RRA:AVERAGE:0.5:60:1488',  # 30 minute averge for 31 days
        ]


    def create(self, filename, archive):
        """

        rrdtool create target.rrd --start 1023654125 --step 300 DS:mem:GAUGE:600:0:671744 RRA:AVERAGE:0.5:12:24 RRA:AVERAGE:0.5:288:31
        

        """
        
        if not filename: filename = self.filename
        if not archive: archive = self.archive
        
        cmd = "rrdtool create %s --step %s" %(filename, self.step)
        cmd = cmd + ' ' + ' '.join(archive)
        print cmd
        subprocess.call(cmd, shell=True)

    def update(self, bot, val):
        """
            rrdtool update target.rrd N:$total_mem
        
        """
        print "Trying to update %s with %s" %(bot, val)
        

        if bot == 'ardyh/bots/rpi1':
            cmd = "rrdtool update %s N:%s" %(self.filename, val)
            print cmd
            subprocess.call(cmd, shell=True)


    def fetch(self, bot=None, variable=None, start=None, end=None):
        """

        start and end should be datetime objects

        rrdtool fetch test.rrd AVERAGE --start 920804400 --end 920809200

        """


        cmd = "rrdtool fetch %s AVERAGE" %(self.filename)
        if start:
            cmd = cmd + ' --start %s' %(self.utc(start))

        if end:
            cmd = cmd + ' --end %s' %(self.utc(end))

        print cmd
        rs = subprocess.check_output(cmd, shell=True)
        # out  = [(int(item.split(": ")[0]), float(item.split(": ")[1])) 
        #             for item in  rs.strip().split('\n')[3:] ]
        out = []
        for row  in rs.strip().split('\n')[3:]:
            ts, val = row.split(": ")
            ts_verbose = dt.fromtimestamp(int(ts)).strftime(self.ISO_FORMAT)
            
            if val == 'nan':
                val = None
            else:
                val = round(float(val), 2)
            
            out.append([int(ts), val, ts_verbose])


        print "%s entries, starting %s and on %s" %(len(out),out[0][2], out[-1][2])
        return out


    def create2(self):
        for bot in self.bots:
            self.create(self.get_filename(bot), self.archive2)


    def update2(self, bot, vals):
        """
            rrdtool update target.rrd N:$total_mem
        
        """
        bot = bot.replace("/", ".")
        print "Trying to update %s with %s" %(bot, vals)
        val = ":".join([str(v) for v in vals]).replace("None", "U")

        cmd = "rrdtool update %s N:%s" %(self.get_filename(bot), val)
        print cmd
        subprocess.call(cmd, shell=True)



    def fetch2(self, bot=None, start=None, end=None):
        """

        start and end should be datetime objects

        rrdtool fetch test.rrd AVERAGE --start 920804400 --end 920809200

        """


        cmd = "rrdtool fetch %s AVERAGE" %(self.get_filename(bot))
        if start:
            cmd = cmd + ' --start %s' %(self.utc(start))

        if end:
            cmd = cmd + ' --end %s' %(self.utc(end))

        print cmd
        rs = subprocess.check_output(cmd, shell=True)
        # out  = [(int(item.split(": ")[0]), float(item.split(": ")[1])) 
        #             for item in  rs.strip().split('\n')[3:] ]
        out = []
        for row  in rs.strip().split('\n')[3:]:
            ts, vals = row.split(": ")
            ts_verbose = dt.fromtimestamp(int(ts)).strftime(self.ISO_FORMAT)
            new_row = [int(ts)]
            for val in vals.split(" "):
                if val == 'nan':
                    val = None
                else:
                    val = round(float(val), 2)
                new_row.append(val)

            out.append(new_row)


        print "%s entries, starting %s and on %s" %(len(out),out[0][2], out[-1][2])
        return out

    def utc(self, dt_obj):
        tt = dt.timetuple(dt_obj)
        return int(time.mktime(tt))

    def utc_now(self):
        now = dt.now()
        return self.utc(now)

    def get_filename(self, bot):
        return "%s.rrd" %(bot.replace("/", "."))

if __name__ == "__main__":
    db = Db()
    #db.create2()
    db.update2(db.bots[1], [23, 75, 1000, 1200])
    rs = db.fetch2(db.bots[1])
    print rs

    # now = dt.now()
    # start = now - timedelta(minutes=30)
    # end = now - timedelta(minutes=0)
    # rs = db.fetch(start=start, end=end)
    # print rs
    # import pdb; pdb.set_trace()

    while True:
        vals = [randint(10,50)]*4
        db.update2(db.bots[0], vals)
        db.update2(db.bots[1], vals)
        print "Added value %s" %vals
        sleep(5)



