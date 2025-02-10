from pymodbus.client.serial import ModbusSerialClient as ModbusClient
import time

# 初始化Modbus RTU客户端
client = ModbusClient(
    method='rtu',
    port='COM3',         # 根据实际RS-485端口修改
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity='N',
    timeout=1
)

# 汇川伺服驱动器的Modbus地址，参考驱动器手册
SERVO_ADDR = 1         # 驱动器的Modbus地址
START_STOP_ADDR = 0x1000  # 启停控制寄存器
SPEED_SET_ADDR = 0x1002   # 速度设定寄存器
DIRECTION_ADDR = 0x1001   # 方向控制寄存器
STATUS_ADDR = 0x2000      # 状态寄存器，读取电机当前状态

# 启动与停止控制的命令
START_COMMAND = 0x0001
STOP_COMMAND = 0x0000

def connect_client():
    if client.connect():
        print("连接到伺服驱动器成功")
    else:
        print("连接失败")

# 启动电机
def start_motor():
    client.write_register(START_STOP_ADDR, START_COMMAND, unit=SERVO_ADDR)
    print("电机启动")

# 停止电机
def stop_motor():
    client.write_register(START_STOP_ADDR, STOP_COMMAND, unit=SERVO_ADDR)
    print("电机停止")

# 设置电机转速，speed为目标速度
def set_speed(speed):
    client.write_register(SPEED_SET_ADDR, speed, unit=SERVO_ADDR)
    print(f"设置电机速度为 {speed} RPM")

# 切换电机方向，direction = 1 正转，direction = 0 反转
def set_direction(direction):
    client.write_register(DIRECTION_ADDR, direction, unit=SERVO_ADDR)
    dir_text = "正转" if direction == 1 else "反转"
    print(f"设置电机方向为 {dir_text}")

# 读取电机状态（例如速度、转矩）
def read_motor_status():
    response = client.read_holding_registers(STATUS_ADDR, 2, unit=SERVO_ADDR)
    if response.isError():
        print("状态读取失败")
    else:
        speed = response.registers[0]  # 读取的速度
        torque = response.registers[1] # 读取的转矩
        print(f"当前速度: {speed} RPM, 当前转矩: {torque} Nm")
    return speed, torque

# 加速函数
def accelerate(target_speed, step=100):
    for speed in range(0, target_speed + 1, step):
        set_speed(speed)
        time.sleep(0.5)  # 延时，模拟平滑加速

# 减速函数
def decelerate(step=100):
    speed, _ = read_motor_status()
    while speed > 0:
        speed = max(0, speed - step)  # 防止减到负值
        set_speed(speed)
        time.sleep(0.5)
        speed, _ = read_motor_status()

# 主程序
def main():
    connect_client()      # 连接驱动器

    # 电机操作示例
    start_motor()         # 启动电机
    set_direction(1)      # 设置为正转
    accelerate(1000)      # 加速到1000 RPM
    time.sleep(5)         # 运行5秒

    decelerate()          # 减速停止
    time.sleep(2)

    set_direction(0)      # 切换为反转
    accelerate(800)       # 加速到800 RPM
    time.sleep(5)

    stop_motor()          # 停止电机

    # 读取电机状态
    speed, torque = read_motor_status()
    print(f"最终速度: {speed} RPM, 最终转矩: {torque} Nm")

    client.close()        # 关闭Modbus连接

if __name__ == "__main__":
    main()
