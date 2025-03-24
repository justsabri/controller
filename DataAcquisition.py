from datetime import datetime
import os
from PlcController import *
import pandas as pd
import time
import threading

class DataAcquisition: 
    def __init__(self, client):
        self.client = client 
        self.cb = None
        self.isTesting = False
        self.isEnuming = False
        self.isRecording = False
        self.duration = 0.050 # 50ms
        self.location_range = [0, 50]
        self.location_step = 1
        self.location_duration = 1 # 30s
        self.data_name = ['trim', 'rolling', 'speed', 'current1', 'current2']
        self.file_name = 'test_data_at_speed_'
        self.record_file_name = ''
        self.thread_record = None
        self.thread_test = None
        self.enum_thread = None

    def setDataName(self, data_name):
        self.data_name = data_name

    def setCallback(self, func):
        self.cb = func

    def getAllTestData(self):
        datas = []
        for name in self.data_name:
            data = getData(self.client, name)
            datas.append(data)
        return datas

    def getTestDataByName(self, data_name):
        datas = []
        for name in data_name:
            data = getData(self.client, name)
            datas.append(data)
        return datas

    def testBestSpeedImpl(self):
        if self.client is None:
            return
        
        while self.isTesting:
            datas = self.getAllTestData()
            
            datas_padded = datas + [np.nan] * (len(self.test_df.columns) - len(datas))
            print(datas)
            print(datas_padded)
            self.test_df.loc[len(self.test_df)] = datas_padded
            # self.record_data.append(datas_padded, ignore_index=True)

            self.test_df.tail(1).to_csv(self.file_name, header=False, index=False, mode='a')
            time.sleep(self.duration)
        
    def enumerateLocation(self):
        i = self.location_range[0]
        while self.isEnuming and i < self.location_range[1]:
            setCmd(self.client, 'dest1', i)
            setCmd(self.client, 'dest2', i)
            time.sleep(self.location_duration)
            i = i + self.location_step
            percent = int(100.0 * (i+1) / self.location_range[1])
            self.cb(percent)

    
    def startTest(self, file):
        # self.client = PlcClient().getClient()
        if self.client is None:
            print('client is null')
            return
        self.isTesting = True
        self.isEnuming = True

        # file path
        if not os.path.exists('data') or not os.path.isdir('data'):
            os.mkdir('data')
        self.file_name = f'data/' + self.file_name + file + '.csv'
        self.test_df = pd.DataFrame(columns=self.data_name)
        self.test_df.to_csv(self.file_name, index=False, mode='a')
        self.thread_test = threading.Thread(target=self.testBestSpeedImpl)
        # self.thread_test.setDaemon(1)
        self.thread_test.start()
        self.enum_thread = threading.Thread(target=self.enumerateLocation)
        self.enum_thread.start()

    def stopTest(self):
        self.isTesting = False
        self.isEnuming = False
        if not self.enum_thread is None:
            self.enum_thread.join()
            self.enum_thread = None
        if not self.thread_test is None:
            self.thread_test.join()
            self.thread_test = None

    def record_impl(self):
        if self.client is None:
            return

        while self.isRecording:
            datas = self.getAllTestData()
            self.record_df.loc[len(self.record_df)] = datas

            self.record_df.to_csv(self.record_file_name, header=False, index=False, mode='a')
            time.sleep(self.duration)

    def start_record(self):
        # self.client = PlcClient().getClient()
        if self.client is None:
            return
        self.isRecording = True

        # file path
        if not os.path.exists('data') or not os.path.isdir('data'):
            os.mkdir('data')
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + f".{datetime.now().microsecond // 1000:03d}"
        self.record_file_name = f'data/' + current_time + '.csv'
        self.record_df = pd.DataFrame(columns=self.data_name)
        self.record_df.to_csv(self.record_file_name, index=False, mode='a')
        self.thread_record = threading.Thread(target=self.record_impl)
        self.thread_record.start()

    def stop_record(self):
        self.isRecording = False
        if not self.thread_record is None:
            self.thread_record.join()
        return self.record_file_name

# if __name__ == '__main__':
    # da = DataAcquisition()
    # for i in ['1000','1500','2000']:
    #     da.startTest(i)
    # da.stopTest()

if __name__ == '__main__':
    client = connectPLC()
    data_acq = DataAcquisition(client)
    data_acq.start_record()
    print('start record')
    time.sleep(3)
    print('wait done')
    data_acq.stop_record()
    print('stop record')