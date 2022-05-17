import requests
import json
import time
from urllib.parse import urljoin
from configparser import ConfigParser
from mongo_client import MongoDBClient

general_config = {}

def read_configuration():
    config_parser = ConfigParser()
    config_parser.read('configuration.cfg')
    general_config['DB_ADDRESS'] = config_parser['DATABASE'].get('address', False)
    general_config['DB_PORT'] = config_parser['DATABASE'].getint('port')
    general_config['DB_USERNAME'] = config_parser['DATABASE'].get('username', False)
    general_config['DB_PASSWORD'] = config_parser['DATABASE'].get('password', False)
    general_config['DB_DATABASE_NAME'] = config_parser['DATABASE'].get('table', False)

    general_config['URL_SENSORS_LIST'] = config_parser['ENDPOINTS'].get('sensors_list', False)
    general_config['URL_SENSORS_INFO'] = config_parser['ENDPOINTS'].get('sensors_info', False)

def connect_db():
    try:
        client = MongoDBClient(general_config['DB_ADDRESS'], general_config['DB_PORT'], 
                                general_config['DB_USERNAME'], general_config['DB_PASSWORD'], general_config['DB_DATABASE_NAME'])
        client.connectDB()
        print('DB connected.')
        return client
    except:
        print('DB not connected!')
        return None

def request_sensors():
    try:
        return requests.get(general_config['URL_SENSORS_LIST'])
    except:
        print('Cannot read sensor list')
        return None

def run():
    try:
        read_configuration()
        print(general_config)
        client = connect_db()
        response = request_sensors()
        sensors = json.loads(response.text)
        print(sensors)
        last_f_cnt = [0] * len(sensors)
        while True:
            for index in range(len(sensors)):
                response = requests.get(urljoin(general_config['URL_SENSORS_INFO'], sensors[index]))
                item = json.loads(response.text)
                if item['uplink_message']['f_cnt'] == last_f_cnt[index]:
                    continue
                print(item)
                last_f_cnt[index] = item['uplink_message']['f_cnt']
                client.insertData(item, "uplinks")
            time.sleep(10)
    except:
        print('Error: Stopping application.')
        return

        
if __name__ == "__main__": 
    run()