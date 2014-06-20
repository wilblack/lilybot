"""


rp3 looks like 

{"timestamp": 1403166406.620432, 
  "message": {"sensor_package": "grovebot", 
              "sensor_values": {"sound": 58, 
                                "dist": 183, 
                                "temp": 20.1, 
                                "light": 186, 
                                "acc_xyz": [2, 22, 5], 
                                "humidity": 52.6, 
                                "slider": 0, 
                                "touch": 0, 
                                "pir": 1}}, 
              "channel": "rp3.solalla.ardyh"}
"""
import json
import redis


r = redis.StrictRedis(host='localhost', port=6379, db=0)
bot_names = ['rp1.solalla.ardyh', 'rp2.solalla.ardyh', 'rp3.solalla.ardyh']

# Get the list for redis


def read_lists():
    for bot in bot_names:
        values = r.lrange(bot, 0, -1)
        print "%s - %s" %(bot, len(values) )





def rp3_to_bq():
    items = r.lrange('rp3.solalla.ardyh', 0, -1)
    rows = []
    for item in items:
        try:
            obj = json.loads(item)
            sensor_values = obj['message']['sensor_values']
        except:
            print "Could not parse ", item
            continue

        acc_x, acc_y, acc_z = sensor_values.pop('acc_xyz')
        sensor_values.update({'acc_x':acc_x,
                              'acc_y':acc_y,
                              'acc_z':acc_z,
                              })
        row = {'json':sensor_values }
        rows.append(row)
        
    
    out = {'rows':rows}
    return out


def load_mock_data():
    for i in range(0,100):
        r.rpush('rp1.solalla.ardyh', i)
        r.rpush('rp2.solalla.ardyh', 200+i)
        r.rpush('rp3.solalla.ardyh', 400+i)



if __name__ == 'main':
    # load mock data
    load_mock_data()

    read_lists()
