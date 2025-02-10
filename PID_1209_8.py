import matplotlib.pyplot as plt
import numpy as np


# PID控制器类
class PIDController:
    def __init__(self, Kp, Ki, Kd):
        """
        初始化PID控制器
        :param Kp: 比例系数
        :param Ki: 积分系数
        :param Kd: 微分系数
        """
        self.Kp = Kp  # 比例系数
        self.Ki = Ki  # 积分系数
        self.Kd = Kd  # 微分系数
        self.prev_error = 0  # 上一次误差
        self.integral = 0  # 积分值

    def compute(self, error, dt):
        """
        计算PID控制输出
        :param error: 当前误差值
        :param dt: 时间间隔
        :return: PID控制器输出
        """
        # 积分项
        self.integral += error * dt
        # 微分项
        derivative = (error - self.prev_error) / dt

        # PID控制公式 = 比例 + 积分 + 微分
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error  # 更新误差
        return output


# 模拟纵摇角输出函数，给定航速和截流板伸缩量，计算纵摇角
def simulation_pitch_angle(speed, x):
    """
    根据航速和截流板伸缩量（x）计算船舶的纵摇角度（y）。
    :param speed: 航速（单位knots）
    :param x: 截流板伸缩量（单位mm）
    :return: 纵摇角度y
    """
    # 多项式系数字典，键为航速，值为对应的多项式系数
    coefficients = {
        5: [-2E-07, 2E-05, -0.001, 0.0195, -1.46],
        10: [-1E-07, 1E-05, -0.0005, 0.0139, -2.06],
        15: [-2E-07, 2E-05, -0.0008, 0.0385, -4.46],
        20: [-5E-07, 6E-05, -0.0025, 0.083, -4.5],
        25: [-4E-07, 5E-05, -0.0026, 0.1199, -4.86],
        30: [1E-07, -1E-05, -0.0006, 0.1309, -5.26],
        35: [-2E-06, 0.0002, -0.0058, 0.1466, -4.84],
        40: [-3E-06, 0.0003, -0.0086, 0.1689, -4.24],
        45: [-3E-06, 0.0003, -0.0085, 0.1493, -3.61],
        50: [-2E-06, 0.0002, -0.0063, 0.1437, -3.16]
    }

    # 检查航速是否在预设范围内
    if speed not in coefficients:
        raise ValueError("航速必须为5, 10, 15, 20, 25, 30, 35, 40, 45 或 50 kn之一")

    # 获取对应的多项式系数
    a, b, c, d, e = coefficients[speed]

    # 计算纵摇角度 y = a*x^4 + b*x^3 + c*x^2 + d*x + e
    y = a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e

    # 返回值为纵摇角度
    return y

# 模拟PID控制过程
def simulate_pid_control():
    speed = 50  # 航速 kn
    target_angle = 0  # 目标纵摇角度为0
    initial_extension = 0  # 截流板初始伸缩量
    max_extension = 50  # 截流板最大伸缩量 (单位：mm)

    # PID控制器参数 (根据实际情况调整)
    pid = PIDController(Kp=0.5, Ki=0.01, Kd=0.05)

    # 初始化变量
    extension = initial_extension
    time_steps = 300  # 仿真时间步长
    dt = 1  # 时间间隔（秒）
    pitch_angles = []  # 用于存储每个时间步的纵摇角
    extensions = []  # 用于存储每个时间步的截流板伸缩量
    times = []  # 用于存储每个时间步的时间

    # 仿真过程
    for t in range(time_steps):
        # 计算当前纵摇角度
        current_pitch_angle = simulation_pitch_angle(speed, extension)

        # 计算误差
        error = target_angle - current_pitch_angle

        # 计算PID输出
        pid_output = pid.compute(error, dt)

        # 更新截流板伸缩量
        extension += pid_output
        extension = max(0, min(extension, max_extension))  # 保证伸缩量在有效范围内

        # 存储数据
        times.append(t * dt)
        pitch_angles.append(current_pitch_angle)
        extensions.append(extension)

    # 绘图
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Pitch Angle (degrees)', color='tab:red')
    ax1.plot(times, pitch_angles, color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Extension (mm)', color='tab:blue')
    ax2.plot(times, extensions, color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title(" Pitch Angle & Extension")
    plt.show()


# 执行模拟PID控制并绘制图形
simulate_pid_control()
