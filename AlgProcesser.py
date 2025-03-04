from PlcController import *
import Logger
import queue
import time
import threading
import PID_20250113_1 as pidAlg

class AlgorithmProcesser():
    def __init__(self, feq):
        print('construct')
        self.logger = Logger.GetLogger(__name__)
        self.client = None
        self.mode = 0
        self.data_queue = queue.Queue()
        self.condition = threading.Condition()
        self.data_flag = False
        self.sleep_time = 1.0 / feq # unit: second

        self.data_thread = threading.Thread(target=self.data_threadloop)
        self.process_thread = threading.Thread(target=self.process)
    
    # def __del__(self):
    #     print('disconstruct')
    #     disconnectPLC(self.client)

    def setAlgMode(self, mode):
        self.mode = mode

    def start_process(self):
        self.data_flag = True
        self.client = PlcClient().getClient()
        # self.data_thread.setDaemon(True)
        self.data_thread.start()
        # self.process_thread.setDaemon(True)
        self.process_thread.start()
    
    def stop_process(self):
        self.data_flag = False
        if not self.data_thread is None:
            self.data_thread.join()
        if not self.process_thread is None:
            self.process_thread.join()

    def process(self, data):
        while self.data_flag:
            data = self.wait_for_next_data()
            # data送入算法处理，获取算法执行结果
            self.logger.debug('mode ' + self.mode + ' angle ' + data[0] + ' current '+ data[1])
            dest = pidAlg.PID_parameter_transfer(self.mode, data[0], 0, data[0], 0, data[1])
            self.logger.debug('dest ' + dest)
            # 执行结果下发给plc
            if self.client is not None:
                setCmd(self.client, 'dest1', dest)
            else:
                self.logger.error('client is null')


    def wait_for_next_data(self):
        with self.condition:
            if len(self.data_queue) == 0:
                self.condition.wait()
            data = self.data_queue.get()
        return data
                

    def data_threadloop(self):
        while self.data_flag:
            # 获取所需数据并打包
            data = self.getModeData()
            if data is None:
                self.logger.error('data is null')
                time.sleep(self.sleep_time)
                continue
            self.logger.debug(data.to_string())
            with self.condition:
                self.data_queue.put(data)
                self.condition.notify_all()
            time.sleep(self.sleep_time)

    def getModeData(self):
        if self.client is None:
            self.logger.error('client is null')
            return None
        data_name = []
        datas = []
        if self.mode == 1: # 纵倾控制
            data_name = ['trim', 'current1']
        elif self.mode == 2: #横摇控制
            data_name = ['rolling', 'current1']

        for name in data_name:
            data = getData(self.client, name)
            datas.append(data)
        
        return datas
        



if __name__ == '__main__':
    ap = AlgorithmProcesser()
    ap.setAlgMode(1)
    ap.start_process()
    try:
        while True:
            time.sleep(1)
            print("Main thread is running...")
    except KeyboardInterrupt:
        ap.stop_process()
