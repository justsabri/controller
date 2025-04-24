from pymodbus.client.tcp import ModbusTcpClient
import struct, joblib, os
import numpy as np
import Logger
import traceback

PLC_IP = '192.168.0.1'
PLC_PORT = 502

data_prot = { # data : [addr, count, type(byte:0, int:1, float:2)]
    'auto_mode' : [157, 1, 1], # 0: 手动； 1：自动
    # 'dest1' : [158, 2, 2],
    # 'current1' : [65, 2, 2],
    'dest1' : [158, 2, 2],
    'current1' : [65, 2, 2],
    'dest2' : [160, 2, 2],
    'current2' : [87, 2, 2],
    'dest3' : [162, 2, 2],
    'current3' : [109, 2, 2],
    'dest4' : [164, 2, 2],
    'current4' : [131, 2, 2],
    'lat' : [151, 2, 2],
    'lon' : [153, 2, 2],
    'height' : [155, 2, 2], 
    'rolling' : [0, 2, 2],
    'trim' : [2, 2, 2],
    'speed': [178, 2, 2],
    # 电机参数

    'm_rpm_1' : [67, 2, 1],  # 电机转速
    'm_v_1' : [69, 2, 1],  # 电机电压
    'm_i_1' : [71, 2, 1],  # 电机电流
    'm_p_1' : [73, 2, 1],  # 电机功率
    'm_t_1' : [75, 2, 1],  # 电机温度

    'm_rpm_2' : [89, 2, 1],  # 电机转速
    'm_v_2' : [91, 2, 1],  # 电机电压
    'm_i_2' : [93, 2, 1],  # 电机电流
    'm_p_2' : [95, 2, 1],  # 电机功率
    'm_t_2' : [97, 2, 1],  # 电机温度

    'm_rpm_3' : [111, 2, 1],  # 电机转速
    'm_v_3' : [113, 2, 1],  # 电机电压
    'm_i_3' : [115, 2, 1],  # 电机电流
    'm_p_3' : [117, 2, 1],  # 电机功率
    'm_t_3' : [119, 2, 1],  # 电机温度

    'm_rpm_4' : [133, 2, 1],  # 电机转速
    'm_v_4' : [135, 2, 1],  # 电机电压
    'm_i_4' : [137, 2, 1],  # 电机电流
    'm_p_4' : [139, 2, 1],  # 电机功率
    'm_t_4' : [141, 2, 1],  # 电机温度

    # 零位
    'zero_1' : [169, 1, 1],
    'zero_2' : [170, 1, 1],
    'zero_3' : [171, 1, 1],
    'zero_4' : [172, 1, 1]
}

logger = Logger.GetLogger(__name__)

def connectPLC():
    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
    if client.connect():
        logger.debug("tcp connect sucessful")
        return client
    else:
        logger.error("tcp connect error")
        return None

def disconnectPLC(client):
    if client is not None:
        client.close()

def getData(client, data_name):
    if client is None:
        logger.error("tcp connect first!")
        return
    
    if data_name not in data_prot.keys():
        i = "unknown data name " + data_name
        logger.error(i)
        return
    
    data_info = data_prot[data_name]
    addr = data_info[0]
    count = data_info[1]
    type = data_info[2]
    response = client.read_holding_registers(addr, count)

    if response.isError():
        logger.error("Error reading holding registers")
    else:
        # 打印读取的寄存器值
        registers = response.registers
        hex_res = ''
        for reg in registers:
            reg_hex = hex(reg)[2:]
            # print(reg_hex)
            shift_bit = 4 - len(reg_hex)
            hex_res +=  '0' * shift_bit + reg_hex
        # print(hex_res)
        res = hex_to_float_or_int(hex_res, type)

        # logger.info(f"Read Holding Registers {addr} to {addr + count - 1}: {registers}")
        # 示例：访问特定寄存器的值
        # logger.info(f"Value of Register {addr}: {registers[0]}")  # 第1个寄存器值

        return res

def setCmd(client, data_name, data):
    if client is None:
        logger.error("tcp connect first!")
        return
    
    if data_name not in data_prot.keys():
        e = "unknown data name " + data_name
        logger.error(e)
        return
    
    data_info = data_prot[data_name]
    print(data_info)
    addr = data_info[0]
    count = data_info[1]
    type = data_info[2]
    # if len(str(data)) != count * 2:
    #     e = 'data error ' + data
    #     logger.error(e)
    rigister_data = []
    # r_data = ''
    if type == 2: # float
        if count == 4:
            r_data = float_to_ieee754_hex(data) # 待修改
        elif count == 2:
            r_data = float_to_ieee754_hex(data)
        # elif count == 1:
        #     hex_str = data + ''
        # elif count == 0.5:
        #     pass
    elif type == 1 or type == 0: # int or byte
        r_data = (data,)

    print(r_data)
    # if hex_str is None:
    #     return
    # #拆分 hex_str
    # for i in range(0, count * 2):
    #     print(hex_str[i*2:i*2+2])
    #     rigister_data.append(hex_str[i*2:i*2+2])
    rigister_data = list(r_data)
    print(rigister_data)
    client.write_registers(addr, rigister_data) #[10, 20, 30, 40, 50]

def hex_to_float_or_int(hex_str, type):
    """将 16 进制字符串转换为浮点数"""
    binary = bytes.fromhex(hex_str)  # 转换为字节
    if type == 2: # float
        if len(binary) == 2:
            half = np.frombuffer(binary[::-1], dtype=np.float16)  # 反转字节序并转换
            res = float(half[0]) # 转换为 Python float 类型
        elif len(binary) == 4:
            res = struct.unpack('>f', binary)[0]  # '>f' 表示大端格式的32位浮点数
        else:
            print("unknown length " + hex_str)
    elif type == 1 or type == 0: # int, byte
        res = int(hex_str, 16)
    else:
        print("unknown type " + type)
    return res

def float_to_half_precision_hex(f):
    half = np.float16(f)  # 转换为 16 位浮点数
    # print('ssss')
    binary = half.tobytes()  # 获取字节表示
    return ''.join(f'{b:02x}' for b in binary[::-1])  # 反转字节序并转换为 16 进制

def float_to_ieee754_hex(f):
    # 转换为 IEEE 754 单精度浮点数（4 字节 = 2 寄存器）
    packed = struct.pack('>f', f)  # 4 字节
    register_data = struct.unpack('>HH', packed)  # 拆成 2 个 16 位整数
    return register_data

if os.path.exists('model/extension_limit_model.pkl'):
    extension_limit_model = joblib.load('model/extension_limit_model.pkl')
else:
    extension_limit_model = None

def get_max_extension(speed):
    if extension_limit_model:
        return extension_limit_model(speed)
    else:
        return 1.0
    
class PlcClient():
    client = None
    client_count = 0
    def __init__(self):
        if PlcClient.client is None:
            print('connect')
            traceback.print_stack()
            PlcClient.client = connectPLC()
            if PlcClient.client is not None:
                # setCmd(PlcClient.client, 'auto_mode', 1)
                PlcClient.client_count += 1
    
    def __del__(self):
        PlcClient.client_count -= 1
        if PlcClient.client_count == 0:
            print('disconnect')
            setCmd(PlcClient.client, 'dest1', 0)
            setCmd(PlcClient.client, 'dest2', 0)
            setCmd(PlcClient.client, 'dest3', 0)
            setCmd(PlcClient.client, 'dest4', 0)
            # setCmd(PlcClient.client, 'auto_mode', 0)
            disconnectPLC(PlcClient.client)
            PlcClient.client = None

    def getClient(self):
        return PlcClient.client

def set_zero(i):
    name = 'zero_' + str(i)
    print(name)
    client = connectPLC()
    # 设置电机i零位
    setCmd(client, name, 0)
    setCmd(client, name, 1)
    disconnectPLC(client)

def set_by_step(i, step):
    current_name = 'current' + str(i)
    dest_name = 'dest' + str(i)
    print()
    client = connectPLC()
    # 按步长移动
    current = getData(client, current_name)
    print(current)
    dest = current + step
    setCmd(client, dest_name, dest)
    disconnectPLC(client)

# plc_client = None
#     def get_plc_client():
        
# if __name__ == '__main__':
#     client = connectPLC()
    # setCmd(client, 'switch', 8)
    # try:
    #     while True:
    #         print(getData(client, 'lat'))
    #         print(getData(client, 'lon'))
    #         print(getData(client, 'height'))
    #         print("Main thread is running...")
    # except KeyboardInterrupt:
    #     disconnectPLC(client)
    # print(getData(client, 'current1'))
    # print(getData(client, 'current2'))
    # print(getData(client, 'rolling'))
    # print(getData(client, 'trim'))
    # print(getData(client, 'speed'))
    # print(getData(client, 'm_rpm_1'))
    # print(getData(client, 'm_v_1'))
    # print(getData(client, 'm_i_1'))
    # print(getData(client, 'm_p_1'))
    # print(getData(client, 'm_t_1'))
    # print(getData(client, 'm_i_2'))
    # print(getData(client, 'm_v_2'))
    # print(getData(client, 'm_p_2'))
    # print(getData(client, 'm_t_2'))
    # data_name = ['m_v_1', 'm_i_1', 'm_p_1', 'm_t_1', 'm_v_2', 'm_i_2', 'm_p_2', 'm_t_2', 'trim', 'rolling',  'current1']
    # data_name = ['current1', 'm_t_1', 'auto_mode']
    # datas = []
    # for name in data_name:
    #     data = getData(client, name)
    #     datas.append(data)
    # print(datas)
    # setCmd(client, 'auto_mode', 1)
    # print(getData(client, 'auto_mode'))
    # setCmd(client, 'dest1', 25.5)
    # disconnectPLC(client)

# 设置当前位置为零位，需要显示屏在非手动控制界面设置
# if __name__ == '__main__':
#     set_zero(1)

# # 微调电机1
# if __name__ == '__main__':
#     set_by_step(2, -5)

if __name__ == '__main__':
    print('1')
    print(get_max_extension(28.7))
    print('2')




