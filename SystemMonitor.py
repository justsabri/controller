from PlcController import *
import threading ,os

class Watchdog:
    def __init__(self, func, timeout=5):
        self.timeout = timeout  # 设定超时时间
        self.func = func
        self.timer = None
        self.reset()

    def _timeout_handler(self):
        print("看门狗超时！执行复位操作...")
        if self.func is not None:
            self.func()
        # os._exit(1)  # 退出程序（可改为其他复位操作

    def reset(self):
        """喂狗，重置定时器"""
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.timeout, self._timeout_handler)
        self.timer.start()

    def stop(self):
        """停止看门狗"""
        if self.timer:
            self.timer.cancel()

class SysMonitor():
    def __init__(self, client): 
        self.client = client
        self.location_range = [0, 50]
        self.data_name = ['trim', 'rolling', 'm_v_1', 'm_i_1', 'm_p_1', 'm_t_1', 'm_v_2', 'm_i_2', 'm_p_2', 'm_t_2', 'm_v_3', 'm_i_3', 'm_p_3', 'm_t_3', 'm_v_4', 'm_i_4', 'm_p_4', 'm_t_4', 'speed']
        self.limit_data = {}
        self.monitor_thread = threading.Thread(target=self.monitor_thread_proc)
        self.monitor_flag = False
    
    def setDataName(self, data_name):
        self.data_name = data_name
    
    def setLimit(self, limit_data):
        self.limit_data = limit_data

    def monitor_thread_proc(self):
        pass

    def start_monitor(self):
        # self.client = PlcClient().getClient()
        if self.client is None:
            return False
        self.monitor_flag = True
        self.monitor_thread.start()
        return True

    def stop_monitor(self):
        self.monitor_flag = False
        if not self.monitor_thread is None:
            if self.monitor_thread.is_alive():
                self.monitor_thread.join()
            self.monitor_thread = None
    
    def getMonitorData(self):
        datas = []
        for name in self.data_name:
            data = getData(self.client, name)
            datas.append(data)
        self.datas = datas
        return datas
    
    def get_current_data(self):
        return self.datas
    
    def getInitValue(self):
        datas = []
        for name in ['current2', 'current3']:
            data = getData(self.client, name)
            datas.append(data * 100.0 / self.location_range[1])
        return datas
    
if __name__ == '__main__':
    client = connectPLC()
    sys_monitor = SysMonitor(client)
    sys_monitor.start_monitor()
