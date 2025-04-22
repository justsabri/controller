import os, joblib
from datetime import datetime
import pandas as pd
from PlcController import *
import Logger
import queue
import time
import threading
from scipy.interpolate import CubicSpline
# import PID_20250113_1 as pidAlg
# import PID_20250324_2 as pidAlg
import PID_20250422 as pidAlg

class AlgorithmProcesser():
    def __init__(self, feq, client):
        print('construct')
        self.logger = Logger.GetLogger(__name__)
        # self.client = None
        self.client = client
        self.cb = None
        self.mode = 0
        if os.path.exists('model/speed2extension_model.pkl'):
            self.speed2extension = joblib.load('model/speed2extension_model.pkl')
        else:
            self.speed2extension = None
        
        if os.path.exists('model/optspeed2extension_model.pkl'):
            self.optspeed2extension = joblib.load('model/optspeed2extension_model.pkl')
        else:
            self.optspeed2extension = None

        self.data_queue = queue.Queue()
        self.condition = threading.Condition()
        self.data_flag = False
        self.data_name = ['trim', 'rolling', 'speed', 'current1', 'current3']
        self.sleep_time = 1.0 / feq # unit: second
        self.location_range = [0, 50]

        self.isRecording = False
        self.record_duration = 0.05 # 50ms
        self.thread_record = None
        self.record_event = None
        self.record_plc_data = ['trim', 'rolling', 'speed', 'current1', 'current3']
        self.record_data_name = ['time', 'trim', 'rolling', 'speed', 'current1', 'current3', 'mode', 'dest1', 'dest3']

        self.data_thread = None
        self.process_thread = None
    
    # def __del__(self):
    #     print('disconstruct')
    #     disconnectPLC(self.client)

    def setAlgMode(self, mode):
        self.mode = mode

    def setCallback(self, func):
        self.cb = func

    def start_process(self):
        self.data_flag = True
        # self.client = PlcClient().getClient()
        self.data_thread = threading.Thread(target=self.data_threadloop)
        # self.data_thread.setDaemon(True)
        self.data_thread.start()
        
        self.process_thread = threading.Thread(target=self.process)
        # self.process_thread.setDaemon(True)
        self.process_thread.start()
    
    def stop_process(self):
        self.data_flag = False
        if not self.process_thread is None:
            self.process_thread.join()
            self.process_thread = None
        if not self.data_thread is None:
            self.data_thread.join()
            self.data_thread = None
        self.mode = 0

    def process(self):
        while self.data_flag:
            data = self.wait_for_next_data()
            # data送入算法处理，获取算法执行结果
            self.logger.debug('mode ' + str(self.mode) + ' angle ' + str(data[0]) + ' current '+ str(data[3]))
            print('mode ' + str(self.mode) + ' angle ' + str(data[0]) + ' current '+ str(data[3]))
            # dest = pidAlg.PID_parameter_transfer(self.mode, data[0], 0, data[1], 0, data[3])
            # self.logger.debug('dest ' + str(dest))
            # # 发送取数据事件
            # if self.record_event:
            #     if self.mode == 1:
            #         self.record_data = [*data, self.mode, dest]
            #     else:
            #         self.record_data = [*data, self.mode, *dest]
            #     self.record_event.set()
            
            # # 执行结果下发给plc
            # if self.client is not None:
            #     if self.mode == 1:
            #         self.setLocation('both', dest, dest)
            #         percent = int(100.0 * dest / self.location_range[1])
            #         if self.cb:
            #             self.cb(percent, percent)
            #     elif self.mode == 2:
            #         self.setLocation('both', dest[0], dest[1])
            #         percent1 = int(100.0 * dest[0] / self.location_range[1])
            #         percent2 = int(100.0 * dest[0] / self.location_range[1])
            #         if self.cb:
            #             self.cb(percent1, percent2)
            # else:
            #     self.logger.error('client is null')
            if self.mode == 3: # 速度优先
                if self.speed2extension is not None and self.optspeed2extension is not None:
                    current_speed = data[2]
                    current_extension1 = data[3]
                    current_extension2 = data[4]
                    target_extension = self.optspeed2extension(current_speed)
                    if abs(target_extension - current_extension1) > 3.0:
                        dest_extension = min(current_extension1, self.location_range[1] * get_max_extension(current_speed))
                        dest = (dest_extension, dest_extension)
                    else:
                        dest = (-0.1, -0.1)
                else:
                    print('no self.cs')
            else:
                dest = pidAlg.PID_parameter_transfer(self.mode, data[2], (data[0], 0), (data[1], 0), (data[3], data[4]), self.location_range[1] * get_max_extension(data[2]))
            self.logger.debug('dest ' + str(dest))
            # 发送取数据事件
            if self.record_event:
                self.record_data = [*data, self.mode, *dest]
                self.record_event.set()
            # 执行结果下发给plc
            if self.client is not None:
                self.setLocation('both', dest[0], dest[1])
                percent1 = int(100.0 * dest[0] / self.location_range[1])
                percent2 = int(100.0 * dest[1] / self.location_range[1])
                if self.cb:
                    self.cb(percent1, percent2)
            else:
                self.logger.error('client is null')
        print('stop process')


    def wait_for_next_data(self):
        with self.condition:
            if self.data_queue.empty():
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
            self.logger.debug(' '.join(map(str, data)))
            with self.condition:
                self.data_queue.put(data)
                self.condition.notify_all()
            time.sleep(self.sleep_time)
        print('stop data_threadloop')

    def getModeData(self):
        if self.client is None:
            self.logger.error('client is null')
            return None
        datas = []
        for name in self.data_name:
            data = getData(self.client, name)
            datas.append(data)
        
        return datas
    
    def setLocation(self, side, *args):
        names = []
        if side == 'left':
            names.append('dest1')
            names.append('dest2')
        elif side == 'right':
            names.append('dest3')
            names.append('dest4')
        elif side == 'both':
            names.append('dest1')
            names.append('dest2')
            names.append('dest3')
            names.append('dest4')
        for i,name in enumerate(names):
            if self.location_range[0] <= args[i] <= self.location_range[1]:
                setCmd(self.client, name, args[i])
    
    def setLocationByPercent(self, side, *args):
        names = []
        if side == 'left':
            names.append('dest1')
            names.append('dest2')
        elif side == 'right':
            names.append('dest3')
            names.append('dest4')
        elif side == 'both':
            names.append('dest1')
            names.append('dest2')
            names.append('dest3')
            names.append('dest4')
        for i,name in enumerate(names):
            debug_info = str(i) + ' ' + name + ' ' + str(args[i] * (self.location_range[1] / 100.0))
            self.logger.debug(debug_info)
            print(i, name, args[i] * (self.location_range[1] / 100.0))
            if 0 <= args[i] <= 100:
                setCmd(self.client, name, args[i] * (self.location_range[1] / 100.0))
    
    def record_impl(self):
        if self.client is None:
            return

        while self.isRecording:
            datas = self.getAllRecordData()
            datas_padded = datas + [np.nan] * (len(self.record_df.columns) - len(datas))
            print(datas)
            print(datas_padded)
            self.record_df.loc[len(self.record_df)] = datas_padded
            # self.record_data.append(datas_padded, ignore_index=True)

            self.record_df.tail(1).to_csv(self.record_file_name, header=False, index=False, mode='a')
            if self.mode == 0:
                time.sleep(self.record_duration)

    def getAllRecordData(self):
        current_time = datetime.now().strftime('%H:%M:%S') + f"-{datetime.now().microsecond // 1000:03d}"
        if self.mode == 0:
            datas = [current_time]
            for name in self.record_plc_data:
                data = getData(self.client, name)
                datas.append(data)
            datas.append(self.mode)
            return datas
        else:
            if self.record_event:
                self.record_event.wait()
            return [current_time] + self.record_data
            
    
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
        self.record_df = pd.DataFrame(columns=self.record_data_name)
        self.record_df.to_csv(self.record_file_name, index=False, mode='a')
        self.thread_record = threading.Thread(target=self.record_impl)
        self.record_event = threading.Event()
        self.thread_record.start()

    def stop_record(self):
        self.isRecording = False
        self.record_event.set()
        if not self.thread_record is None:
            self.thread_record.join()
        self.record_event = None
        return self.record_file_name
        



# if __name__ == '__main__':
#     client = connectPLC()
#     ap = AlgorithmProcesser(50, client)
#     ap.setAlgMode(1)
#     ap.start_process()
#     try:
#         while True:
#             time.sleep(1)
#             print("Main thread is running...")
#     except KeyboardInterrupt:
#         ap.stop_process()

if __name__ == '__main__':
    client = connectPLC()
    alg_process = AlgorithmProcesser(50, client)
    alg_process.start_record()
    print('start record')
    time.sleep(3)
    print('wait done')
    alg_process.stop_record()
    print('stop record')