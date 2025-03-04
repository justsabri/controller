from PlcController import *
import threading

class SysMonitor():
    def __init__(self):
        self.client = None
        self.data_name = []
        self.monitor_thread = threading.Thread(self.monitor_thread_proc)
        self.monitor_flag = False
    
    def monitor_thread_proc(self):
        pass

    def start_monitor(self):
        self.client = PlcClient().getClient()
        self.monitor_flag = True
        self.monitor_thread.start()

    def stop_monitor(self):
        self.monitor_flag = False
        if not self.monitor_thread is None:
            self.monitor_thread.join()
    
    def getMonitorData(self):
        datas = []
        for name in self.data_name:
            data = getData(self.client, name)
            datas.append(data)
        return datas
