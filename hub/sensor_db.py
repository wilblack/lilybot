from time import sleep
from random import randint
from datetime import datetime as dt
from datetime import timedelta
import time
import subprocess

class Db(object):
    
    conn = None;
    step = 30
    filename = '/home/pi/projects/lilybot/hub/sensors.rrd'
    archive = [
            'DS:temp:GAUGE:30:0:100',
            'RRA:AVERAGE:0.5:2:1440',  # 1 minute average for 24 hours
            'RRA:AVERAGE:0.5:10:1440',  # 5 minute averge for 3 days
            'RRA:AVERAGE:0.5:10:1440',  # 10 minute averge for 7 days
            'RRA:AVERAGE:0.5:60:1488',  # 30 minute averge for 31 days
        ]

    def create(self):
        """

        rrdtool create target.rrd --start 1023654125 --step 300 DS:mem:GAUGE:600:0:671744 RRA:AVERAGE:0.5:12:24 RRA:AVERAGE:0.5:288:31
        

        """
        
        
        
        cmd = "rrdtool create %s --step %s" %(self.filename, self.step)
        cmd = cmd + ' ' + ' '.join(self.archive)
        print cmd
        subprocess.call(cmd, shell=True)



    def update(self, bot, val):
        """
            rrdtool update target.rrd N:$total_mem
        
        """

        if bot == 'ardyh.bots.rpi1':
            cmd = "rrdtool update %s N:%s" %(self.filename, val)
            print cmd
            subprocess.call(cmd, shell=True)


    def fetch(self, start=None, end=None):
        """
        rrdtool fetch test.rrd AVERAGE --start 920804400 --end 920809200
        """


        cmd = "rrdtool fetch %s AVERAGE" %(self.filename)
        if start:
            tt = dt.timetuple(start)
            epoch = int(time.mktime(tt))
            cmd = cmd + ' --start %s' %(epoch)

        if end:
            tt = dt.timetuple(end)
            epoch = int(time.mktime(tt))
            cmd = cmd + ' --end %s' %(epoch)

        print cmd
        rs = subprocess.check_output(cmd, shell=True)
        out  = [(int(item.split(": ")[0]), float(item.split(": ")[1])) 
                    for item in  rs.strip().split('\n')[3:] ]

        return out


if __name__ == "__main__":
    db = Db()
    # db.create()
    # db.update(23)
    # now = dt.now()
    # start = now - timedelta(minutes=30)
    # end = now - timedelta(minutes=0)
    # rs = db.fetch(start=start, end=end)
    # print rs
    # import pdb; pdb.set_trace()

    # while True:
    #     val = randint(10,50)
    #     db.update(val)
    #     print "Added value %s" %val
    #     sleep(5)



