from pymodbus.client.tcp import ModbusTcpClient
import struct
import numpy as np
import Logger

PLC_IP = '192.168.0.1'
PLC_PORT = 502

data_prot = {
    'auto_mode' : [314, 1], # data : [addr, count]
    'dest1' : [158, 2],
    'lat' : [151, 2],
    'lon' : [153, 2],
    'height' : [155, 2],
    'switch' : [157, 1]
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
    response = client.read_holding_registers(addr, count)

    if response.isError():
        logger.error("Error reading holding registers")
    else:
        # 打印读取的寄存器值
        registers = response.registers
        hex_res = ''
        for reg in registers:
            reg_hex = hex(reg)[2:]
            shift_bit = 4 - len(reg_hex)
            hex_res += reg_hex + '0' * shift_bit
        
        # 将十六进制字符串转换为字节
        byte_res = bytes.fromhex(hex_res)

        # 使用struct将字节数据解析为浮点数
        float_res = struct.unpack('>f', byte_res)[0]  # '>f' 表示大端格式的32位浮点数

        # logger.info(f"Read Holding Registers {addr} to {addr + count - 1}: {registers}")
        # 示例：访问特定寄存器的值
        # logger.info(f"Value of Register {addr}: {registers[0]}")  # 第1个寄存器值

        return float_res

def setCmd(client, data_name, data):
    if client is None:
        logger.error("tcp connect first!")
        return
    
    if data_name not in data_prot.keys():
        e = "unknown data name " + data_name
        logger.error(e)
        return
    
    data_info = data_prot[data_name]
    addr = data_info[0]
    count = data_info[1]
    # if len(str(data)) != count * 2:
    #     e = 'data error ' + data
    #     logger.error(e)
    rigister_data = []
    #拆分data
    # for i in count:
    #     print(int(data[i:i+2]))
    #     rigister_data.append(int(data[i:i+2]))
    rigister_data.append(data)
    client.write_registers(addr, rigister_data) #[10, 20, 30, 40, 50]

def hex_to_float_or_int(hex_str):
    """将 16 进制字符串转换为浮点数"""
    binary = bytes.fromhex(hex_str)  # 转换为字节
    if len(binary) == 2:
        half = np.frombuffer(binary[::-1], dtype=np.float16)  # 反转字节序并转换
        res = float(half[0]) # 转换为 Python float 类型
    elif len(binary) == 4:
        res = struct.unpack('>f', binary)[0]  # '>f' 表示大端格式的32位浮点数
    elif len(binary) == 1:
        res = int(hex_str)
    else:
        print("unknown length " + hex_str)
    return res

def float_to_half_precision_hex(f):
    half = np.float16(f)  # 转换为 16 位浮点数
    binary = half.tobytes()  # 获取字节表示
    return ''.join(f'{b:02x}' for b in binary[::-1])  # 反转字节序并转换为 16 进制

def float_to_ieee754_hex(f):
    return ''.join(f'{b:02x}' for b in struct.pack('>f', f))

if __name__ == '__main__':
    client = connectPLC()
    setCmd(client, 'switch', 8)
    # try:
    #     while True:
    #         print(getData(client, 'lat'))
    #         print(getData(client, 'lon'))
    #         print(getData(client, 'height'))
    #         print("Main thread is running...")
    # except KeyboardInterrupt:
    #     disconnectPLC(client)
    disconnectPLC(client)
    
    



