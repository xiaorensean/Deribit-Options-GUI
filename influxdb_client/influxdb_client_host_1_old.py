from influxdb import InfluxDBClient,DataFrameClient
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))


# host name 
HOST_1_old = 'ec2-35-183-41-80.ca-central-1.compute.amazonaws.com'
#HOST_2_old = 'ec2-35-183-244-102.ca-central-1.compute.amazonaws.com'
HOST_1 = "ec2-99-79-47-186.ca-central-1.compute.amazonaws.com"
HOST_2 = "ec2-35-182-170-72.ca-central-1.compute.amazonaws.com"

# database name
database = 'md_rates'


class InfluxClientHost1Old:
    
    def __init__(self):        
        user_name = ''
        passwords = ''         
        self.client = InfluxDBClient(host=HOST_1_old, port=8086, username=user_name, password=passwords)
        self.client.switch_database(database)
        #self.dfclient = DataFrameClient(host=HOST,port=8086, username=user_name, password=passwords)
    
    
        
    # get the table names
    def get_table_name(self,exchange = None):
        # switch to a database
        #self.client.switch_database(db_name)
        measurements = self.client.get_list_measurements()
        if exchange is not None:
            table_names = []
            for i in measurements:
                table_names.append(i['name'])
            # in list format 
            table_name_exchange = list(sorted([i for i in table_names if exchange in i]))
            return(table_name_exchange)
        else:
            return(measurements)
    
    def show_keys(self,queryString):
        # SHOW TAG KEYS
        # SHOE FIELD KEYS
        query_results = self.client.query(queryString)
        dict_results = dict(query_results)
        list_results = list(query_results)
        table_name = []
        for ii in dict_results:
            table_name.append(ii[0])
        fields_type = {}
        for idx,item in enumerate(table_name):
            fields_type.update({item:list_results[idx]})
        return fields_type
    
        
    # query the results
    def query_tables(self,table_name, conditions,raw=None):
        #self.client.switch_database(db_name)
        queryString = ("SELECT " + conditions[0] + " FROM {} " + conditions[1]).format(table_name)
        #query_results = self.client.query(queryString, chunked=True, chunk_size=50000)
        query_results = self.client.query(queryString)
        results_df = []
        for result in query_results:
            results_df.append(pd.DataFrame(result)) 
        df = results_df[0]
        if raw is None:
            result = df
        else:
            result = list(query_results)[0]
        return result

    # get tag values
    def get_tag_values(self,table_name,key):
        tags_temp = list(self.client.query("SHOW TAG VALUES FROM {} WITH KEY = {}".format(table_name,key)))
        tags_temp_c = tags_temp.copy()
        tags = tags_temp_c[0]
        symbol_tags = []
        for tag in tags:
            symbol_tags.append(tag['value'])
        return(symbol_tags)

        
    def delete(self,table_name,start_time=None,end_time=None):
        # time format
        # 2019-08-16 16:37:09.000
        #self.client.switch_database(db_name)
        if start_time is not None and end_time is not None:
            queryString = "DELETE FROM {} WHERE time > '{}' AND time < '{}'".format(table_name,start_time,end_time)
        if start_time is not None and end_time is None:
            queryString = "DELETE FROM {} WHERE time > '{}'".format(table_name,start_time)
        if start_time is None and end_time is not None:
            queryString = "DELETE FROM {} WHERE time < '{}'".format(table_name,end_time)
            
        self.client.query(queryString)
    
   
                
    # write points to table
    def write_points_to_measurement(self,measurement, time, tags, fields):
        #self.client.switch_database(db_name)
        json_body = []
        if time:
            json_body = [
                    {
                        "measurement": measurement,
                        "time": time,
                        "tags": tags,
                        "fields": fields
                            }
                    ]
        else:
            json_body = [
                    {
                        "measurement":measurement,
                        "tags":tags,
                        "fields":fields
                            }
                    ]
            
        return self.client.write_points(json_body)
    
    
      

if __name__ == '__main__':
    db = InfluxClientHost1()
    db_names = db.client.get_list_database()
    #tables = db.get_table_name()
    #a = db.get_tag_values('deribit_optionsTicker','symbol')
    #a = db.show_keys("SHOW TAG KEYS")
    a = db.query_tables('okex_future_stats_longShortPositionRatio',['*',""])
    #a1 = a.to_dict()
    #tags_temp = list(db.client.query("SHOW tag values from FTX_trades with key = symbol"))
    #tags_temp_c = tags_temp.copy()
    #tags = tags_temp_c[0]
    #symbol_tags = []
    #for tag in tags:
    #    symbol_tags.append(tag['value'])
    #ftx_trade_2 = db.query_tables('FTX_trades',["*",""])
    #a = {}   
    #for symb in sorted(list(set(ftx_trade.symbol.tolist()))):
    #    a.update({symb:ftx_trade[ftx_trade.symbol==symb].shape[0]})

    
    #bitmex_funding_rates = db.query_tables('bitmex_funding_rates',["*",""])
    #bitmex_leaderboard_roe = db.query_tables('bitmex_leaderboard_ROE',["*",""])
    #bitmex_leaderboard_notional = db.query_tables('bitmex_leaderboard_notional',["*",""])

    #query = db.query_tables('okex_longShortPositionRatio',["*",""])
    #db.delete('namebase_orderbosok',"2018-08-28 00:02:02",None)





