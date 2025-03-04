from PlcController import *
import pandas as pd
import time
import threading

class DataAcquisition: 
    def __init__(self):
        self.client = None 
        self.isTesting = False
        self.location_range = [0, 50]
        self.location_duration = 1000 * 30 # 30s
        self.data_name = ['trim', 'rolling', 'speed', 'current1']
        self.file_name = 'test_data_at_speed_'

    def setDataName(self, data_name):
        self.data_name = data_name

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
        df = pd.DataFrame(columns=self.data_name)
        if self.client is None:
            return
        
        while self.isTesting:
            datas = self.getAllTestData()
            for i, name in enumerate(self.data_name):
                df.loc[len(df), name] = datas[i]

            # df.loc[len(df), 'trim'] = datas[0]
            # df.loc[len(df), 'rolling'] = datas[1]
            # df.loc[len(df), 'speed'] = datas[2]
            # df.loc[len(df), 'current1'] = datas[3]

            df.to_csv(self.file_name, index=False, mode='a')
            self.current_data = datas
            time.sleep(100)
        
    
    def startTest(self, rpm):
        self.client = PlcClient().getClient()
        if self.client is None:
            print('client is null')
            return
        self.isTesting = True
        self.file_name = self.file_name + rpm + '.csv'
        self.thread_test = threading.Thread(target=self.testBestSpeedImpl)
        # self.thread_test.setDaemon(1)
        self.thread_test.start()
        for i in range(self.location_range[0], self.location_range[1]):
            setCmd(self.client, 'dest1', i)
            time.sleep(self.location_duration)

    def stopTest(self):
        self.isTesting = False
        if not self.thread_test is None:
            self.thread_test.join()
        if self.client is not None:
            del self.client
            self.client = None

if __name__ == '__main__':
    da = DataAcquisition()
    for i in ['1000','1500','2000']:
        da.startTest(i)
    da.stopTest()