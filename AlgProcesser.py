from PlcController import *
import Logger
import queue
import time
import threading

class AlgorithmProcesser():
    def __init__(self, feq):
        print('construct')
        self.logger = Logger.GetLogger(__name__)
        self.client = connectPLC()
        self.data_queue = queue.Queue()
        self.condition = threading.Condition()
        self.data_flag = False
        self.sleep_time = 1.0 / feq # unit: second

        self.data_thread = threading.Thread(target=self.data_threadloop)
        self.process_thread = threading.Thread(target=self.process)
    
    def __del__(self):
        print('disconstruct')
        disconnectPLC(self.client)

    def start_process(self):
        self.data_flag = True
        self.data_thread.setDaemon(True)
        self.data_thread.start()
        self.process_thread.setDaemon(True)
        self.process_thread.start()
    
    def stop_process(self):
        self.data_flag = False
        self.data_thread.join()
        self.process_thread.join()

    def process(self, data):
        while self.data_flag:
            data = self.wait_for_next_data()
            # data送入算法处理，获取算法执行结果

            # 执行结果下发给plc
            # setCmd 


    def wait_for_next_data(self):
        with self.condition:
            if len(self.data_queue) == 0:
                self.condition.wait()
            data = self.data_queue.get()
        return data
                

    def data_threadloop(self):
        while self.data_flag:
            # 获取所需数据并打包
            data = getData(self.client,'')

            self.logger.debug(data.to_string())
            with self.condition:
                self.data_queue.put(data)
                self.condition.notify_all()
            time.sleep(self.sleep_time)
            



if __name__ == '__main__':
    ap = AlgorithmProcesser()
    ap.start_process()
    try:
        while True:
            time.sleep(1)
            print("Main thread is running...")
    except KeyboardInterrupt:
        ap.stop_process()
