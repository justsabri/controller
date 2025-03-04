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


# 模拟纵摇/横摇输出函数，给定航速和截流板伸缩量，计算纵摇/横摇角
def simulation_angle(speed, x):
    """
    根据航速和截流板伸缩量（x）计算船舶的纵摇/横摇角度（z）。
    :param speed: 航速（单位knots）
    :param x: 截流板伸缩量（单位mm）
    :return: 纵摇/横摇角度z
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

    # 计算纵摇/横摇角度 y = a*x^4 + b*x^3 + c*x^2 + d*x + e
    z = a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e

    # 返回值为纵摇/横摇角度
    return z


# 全局参数
Kp_pitch, Ki_pitch, Kd_pitch = 0.5, 0.01, 0.05  # 纵倾PID参数
Kp_heel, Ki_heel, Kd_heel = 0.5, 0.01, 0.05    # 横倾PID参数
# 初始化PID控制器，分别用于纵倾和横倾
pid_pitch = PIDController(Kp=Kp_pitch, Ki=Ki_pitch, Kd=Kd_pitch)
pid_heel = PIDController(Kp=Kp_heel, Ki=Ki_heel, Kd=Kd_heel)

max_extension = 50      # 截流板最大伸缩量 (单位：mm)
dt = 1  # 时间间隔（秒）


# PID纵倾控制函数
def PID_pitch_control(current_pitch_angle, target_pitch_angle, extension, pid_pitch):
    """
    控制纵倾角度，使其接近目标角度
    :param current_pitch_angle: 当前纵倾角度
    :param target_pitch_angle: 目标纵倾角度
    :param extension: 当前纵倾控制对应的截流板伸缩量
    :param pid_pitch: PID控制器实例
    :return: 更新后的截流板伸缩量
    """
    # 计算纵倾误差（目标角度 - 当前角度）
    error_pitch = target_pitch_angle - current_pitch_angle
    # 通过PID控制器计算纵倾控制量（输出）
    pid_output_pitch = pid_pitch.compute(error_pitch, dt)
    # 更新截流板伸缩量，确保伸缩量在有效范围内（0到max_extension）
    extension += pid_output_pitch
    extension = max(0, min(extension, max_extension))  # 保证伸缩量不超出最大值
    return extension


# PID横倾控制函数
def PID_heel_control(current_heel_angle, target_heel_angle, extension, pid_heel):
    """
    控制横倾角度，使其接近目标角度
    :param current_heel_angle: 当前横倾角度
    :param target_heel_angle: 目标横倾角度
    :param extension: 当前横倾控制对应的截流板伸缩量
    :param pid_heel: PID控制器实例
    :return: 更新后的截流板伸缩量
    """
    # 计算横倾误差（目标角度 - 当前角度）
    error_heel = target_heel_angle - current_heel_angle
    # 通过PID控制器计算横倾控制量（输出）
    pid_output_heel = pid_heel.compute(error_heel, dt)
    # 更新截流板伸缩量，确保伸缩量在有效范围内（0到max_extension）
    extension += pid_output_heel
    extension = max(0, min(extension, max_extension))  # 保证伸缩量不超出最大值
    return extension



# PID参数传递函数：用于接收外部参数，并传递给控制部分
def PID_parameter_transfer(mode, current_pitch_angle, target_pitch_angle, current_heel_angle, target_heel_angle, extension):
    """
    输入参数函数，依据模式来选择进行纵倾控制或横倾控制。
    :param mode: 模式，1为纵倾控制，2为横倾控制
    :param extension: 对应的截流板伸缩量
    :param pid_pitch: 纵倾PID控制器实例
    :param pid_heel: 横倾PID控制器实例
    :return: 更新后的截流板伸缩量
    """
    # 判断控制模式
    if mode == 1:
        # 纵倾控制模式
        extension = PID_pitch_control(current_pitch_angle, target_pitch_angle, extension, pid_pitch)
        return extension
    elif mode == 2:
        # 横倾控制模式
        extension = PID_heel_control(current_heel_angle, target_heel_angle, extension, pid_heel)
        return extension
    else:
        raise ValueError("无效模式，模式应为“1：纵倾”或“2：横倾”")


# 主函数
def main():
    """
    主函数，初始化PID控制器并仿真纵倾和横倾的控制过程，绘制结果图。
    """

    speed = 50  # 航速 kn
    target_pitch_angle = 0  # 目标纵倾角度
    target_heel_angle = 0  # 目标横倾角度
    initial_extension = 0  # 截流板初始伸缩量
    extension = initial_extension # 初始的截流板伸缩量

    # 仿真时间步骤数（300步），即仿真持续的时间
    time_steps = 300
    times = []  # 用于记录时间的列表
    pitch_angles = []  # 用于记录纵倾角度的列表
    heel_angles = []  # 用于记录横倾角度的列表
    extensions_pitch = []  # 用于记录纵倾对应的截流板伸缩量的列表
    extensions_heel = []  # 用于记录横倾对应的截流板伸缩量的列表

    # 模式（1为纵倾控制，2为横倾控制）
    mode = 2  # 可以动态调整为1或2来测试纵倾和横倾控制

    # 仿真过程
    for t in range(time_steps):
        # 使用输入函数处理控制模式并获取更新后的截流板伸缩量
        # 纵倾模式
        if mode == 1:
            # 使用输入函数处理控制模式并获取更新后的截流板伸缩量
            # mode, current_pitch_angle, target_pitch_angle, current_heel_angle, target_heel_angle, extension
            extension = PID_parameter_transfer(mode, simulation_angle(speed, extension), target_pitch_angle, None, None, extension)
            # 计算当前的纵倾角度
            current_pitch_angle = simulation_angle(speed, extension)
            # 将当前数据添加到相应的列表中
            pitch_angles.append(current_pitch_angle)  # 记录当前纵倾角度
            extensions_pitch.append(extension)  # 记录纵倾对应的截流板伸缩量
            times.append(t * dt)  # 记录当前时间

        # 横倾模式
        elif mode == 2:
            # 使用输入函数处理控制模式并获取更新后的截流板伸缩量
            extension = PID_parameter_transfer(mode, None, None, simulation_angle(speed, extension), target_heel_angle, extension)
            # 计算当前的横倾角度
            current_heel_angle = simulation_angle(speed, extension)
            # 将当前数据添加到相应的列表中
            heel_angles.append(current_heel_angle)  # 记录当前横倾角度
            extensions_heel.append(extension)  # 记录横倾对应的截流板伸缩量
            times.append(t * dt)  # 记录当前时间


    # 绘图部分：根据模式分别绘制图形
    if mode == 1:
        # 绘制纵倾角度和电机旋转角度（对应纵倾的截流板伸缩量）
        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.set_xlabel('Time (s)')  # X轴为时间
        ax1.set_ylabel('Pitch Angle (degrees)', color='tab:red')  # Y轴为纵倾角度
        ax1.plot(times, pitch_angles, color='tab:red', label='Pitch Angle')  # 绘制纵倾角度变化曲线
        ax1.set_title("Pitch Angle & Extension")  # 子图标题
        ax1.tick_params(axis='y', labelcolor='tab:red')  # 设置纵倾角度Y轴的标签颜色为红色

        # 在同一图上叠加绘制纵倾截流板伸缩量
        ax3 = ax1.twinx()  # 创建共享X轴的第二个Y轴
        ax3.set_ylabel('Extension (mm)', color='tab:blue')  # 设置Y轴为截流板伸缩量
        ax3.plot(times, extensions_pitch, color='tab:blue', label='Pitch Extension')  # 绘制纵倾控制的截流板伸缩量
        ax3.tick_params(axis='y', labelcolor='tab:blue')  # 设置纵倾伸缩量Y轴的标签颜色为蓝色

        fig.tight_layout()  # 自动调整布局，防止标签重叠
        plt.show()  # 显示图形

    elif mode == 2:
        # 绘制横倾角度和电机旋转角度（对应横倾的截流板伸缩量）
        fig, ax2 = plt.subplots(figsize=(10, 6))

        ax2.set_xlabel('Time (s)')  # X轴为时间
        ax2.set_ylabel('Heel Angle (degrees)', color='tab:green')  # Y轴为横倾角度
        ax2.plot(times, heel_angles, color='tab:green', label='Heel Angle')  # 绘制横倾角度变化曲线
        ax2.set_title("Heel Angle & Extension")  # 子图标题
        ax2.tick_params(axis='y', labelcolor='tab:green')  # 设置横倾角度Y轴的标签颜色为绿色

        # 在同一图上叠加绘制横倾截流板伸缩量
        ax4 = ax2.twinx()  # 创建共享X轴的第二个Y轴
        ax4.set_ylabel('Extension (mm)', color='tab:purple')  # 设置Y轴为截流板伸缩量
        ax4.plot(times, extensions_heel, color='tab:purple', label='Heel Extension')  # 绘制横倾控制的截流板伸缩量
        ax4.tick_params(axis='y', labelcolor='tab:purple')  # 设置横倾伸缩量Y轴的标签颜色为紫色

        fig.tight_layout()  # 自动调整布局，防止标签重叠
        plt.show()  # 显示图形

if __name__ == "__main__":
    # 执行模拟PID控制并绘制图形
    main()