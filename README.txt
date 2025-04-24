1. 速度优先测试数据采集
采集功能在DataAcquisition中，在界面中点击开始记录后，截流板按照步长self.location_step来遍历伸出量，每个伸出量保持时间为self.location_duration。数据采集过程中采集间隔为self.duration。
2. 算法执行频率
在PlcAdapter的构造函数中构造AlgorithmProcesser时传入频率：self.alg_process = AlgorithmProcesser(50, self.client)