import sqlite3

import simplejson as json

from backends import ApiClientBase


DB_NAME = 'growbot.db'
TABLES = [
    'sensor_values',
    'bots'
]





class Api(ApiClientBase):

    def __init__(self):
        self.dbname = DB_NAME

        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

        super(Api, self).__init__()





    def get(self, resource, filters):
        """

        Inputs

        - resource - [String] not used
        - filters: [Dict] keywords
            - bot_name: [String]
            - start: [ISO 8601 datetime string]
            - end: [ISO 8601 datetime string]

        """

        bot_name = filters['bot_name'].replace(".", "_")
        limit = filters.get("limit", 10);
        qs = 'SELECT * FROM  %s ORDER BY datetime("timestamp") DESC LIMIT %s' %(bot_name, limit)


        self.cursor.execute(qs)
        raw = self.cursor.fetchall()
        self.conn.commit()
        out = [ 
            {"timestamp": item[0], 
             "data":json.loads(item[1])['message']['kwargs']
            } for item in raw]
        return out


    def post(self, resource, data):
        
        bot_name = data['bot_name'].replace(".", "_")
        timestamp = data['message']['kwargs']['timestamp']
        qs = "INSERT INTO %s VALUES (?, ?)" %(bot_name)
        
        self.cursor.execute(qs, [timestamp, json.dumps(data) ])
        self.conn.commit()

    def list_tables(self):

        qs = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cursor.execute(qs)
        res = self.cursor.fetchall()
        self.conn.commit()
        return res


    def is_table(self, bot_name):
        import pdb; pdb.set_trace()

    def create_table(self, bot_name):
        """
        Create a table timeseries table to store sensor value.
        This table has 2 fields, 
        - timestamp: [ISO 8601 Timestamp String] e.g. 2015-03-12T12:03:34.12Z
        - data: [String] A stringified JSON object.

        """
        #qs = "CREATE TABLE IF NOT EXISTS ? (timestamp text, data text)"
        #self.cursor.execute(qs, (bot_name.replace(".", "_"), ))
        bot_name = bot_name.replace(".", "_")
        qs = "CREATE TABLE IF NOT EXISTS %s (timestamp text, data text)" %(bot_name)

        self.cursor.execute(qs)
        self.conn.commit()

    def remove_old_entries(self, timeframe):
        now = dt.now()
        if timeframe == '7days':
            ts = now - timedelta(days=7)
        



    def _remove_table(self, bot_name):
        """
        Removes a tbale from the database.

        """
        qs = "DROP TABLE %s" %(bot_name)
        self.cursor.execute(qs)
        self.conn.commit()





# Create database
