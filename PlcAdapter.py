from PlcController import PlcClient
from AlgProcesser import AlgorithmProcesser
from SystemMonitor import SysMonitor
from DataAcquisition import DataAcquisition

class PlcAdapter():
    def __init__(self, ip = '127.0.0.1', port = '80'):
        self.plc_client = PlcClient()
        self.client = self.plc_client.getClient()
        self.alg_process = AlgorithmProcesser(50, self.client)
        self.sys_monitor = SysMonitor(self.client)
        self.data_acq = DataAcquisition(self.client)

    def is_connected(self):
        if self.client is None:
            return False
        return True
    
    def disconnect(self):
        print('adpter disconnect')
        if self.plc_client:
            del self.plc_client
            self.client = None

    def get_alg_process(self):
        return self.alg_process
    
    def get_sys_monitor(self):
        return self.sys_monitor
    
    def get_data_acq(self):
        return self.data_acq