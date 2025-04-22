import matplotlib.pyplot as plt
import numpy as np


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
        self.integral += error * dt  # 积分项累加
        derivative = (error - self.prev_error) / dt  # 微分项计算
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative  # PID输出
        self.prev_error = error  # 更新误差记录
        return output


def simulation_angle(speed, x):
    """
    根据航速和等效截流板伸缩量计算船舶角度
    :param speed: 航速（单位knots）
    :param x: 等效截流板伸缩量（单位mm）
    :return: 船舶角度（单位度）
    """
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
    a, b, c, d, e = coefficients[speed]  # 获取当前航速对应的多项式系数
    z = a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e  # 计算船舶角度
    return z


# 全局参数
Kp_pitch = 0.8  # 纵倾比例系数
Ki_pitch = 0.02  # 纵倾积分系数
Kd_pitch = 0.1  # 纵倾微分系数
Kp_heel = 0.5  # 横倾比例系数
Ki_heel = 0.01  # 横倾积分系数
Kd_heel = 0.05  # 横倾微分系数
max_extension = 50  # 截流板最大伸缩量（单位mm）
dt = 0.04  # 时间间隔（单位秒）

# 初始化PID控制器
pid_pitch = PIDController(Kp_pitch, Ki_pitch, Kd_pitch)  # 纵倾PID控制器
pid_heel = PIDController(Kp_heel, Ki_heel, Kd_heel)  # 横倾PID控制器


def PID_pitch_control(current_angle, target_angle, left_ext, right_ext, pid):
    """
    纵倾控制：同步调整两侧截流板
    :param current_angle: 当前纵倾角度（单位度）
    :param target_angle: 目标纵倾角度（单位度）
    :param left_ext: 左侧截流板当前伸缩量（单位mm）
    :param right_ext: 右侧截流板当前伸缩量（单位mm）
    :param pid: PID控制器实例
    :return: (new_left_ext, new_right_ext) 更新后的两侧伸缩量
    """
    error = target_angle - current_angle  # 计算角度误差
    output = pid.compute(error, dt)  # 获取PID输出

    # 同步调整两侧截流板
    new_left = max(0, min(left_ext + output, max_extension))  # 限制左侧伸缩量范围
    new_right = max(0, min(right_ext + output, max_extension))  # 限制右侧伸缩量范围
    return new_left, new_right


def PID_heel_control(current_angle, target_angle, left_ext, right_ext, pid):
    """
    横倾控制：反向调整两侧截流板
    :param current_angle: 当前横倾角度（单位度）
    :param target_angle: 目标横倾角度（单位度）
    :param left_ext: 左侧截流板当前伸缩量（单位mm）
    :param right_ext: 右侧截流板当前伸缩量（单位mm）
    :param pid: PID控制器实例
    :return: (new_left_ext, new_right_ext) 更新后的两侧伸缩量
    """
    error = target_angle - current_angle  # 计算角度误差
    output = pid.compute(error, dt)  # 获取PID输出

    # 根据误差方向决定调整策略
    if error > 0:  # 需要向右舷倾斜
        adj_left = left_ext - output  # 收回左侧截流板
        adj_right = right_ext + output  # 伸出右侧截流板
    else:  # 需要向左舷倾斜
        adj_left = left_ext + output  # 伸出左侧截流板
        adj_right = right_ext - output  # 收回右侧截流板

    # 限制伸缩量在有效范围内
    new_left = max(0, min(adj_left, max_extension))
    new_right = max(0, min(adj_right, max_extension))
    return new_left, new_right


def PID_parameter_transfer(mode, pitch_params, heel_params, left_ext, right_ext):
    """
    参数分发函数：根据模式选择控制策略
    :param mode: 控制模式（1=纵倾，2=横倾）
    :param pitch_params: 纵倾参数元组（current_angle, target_angle）
    :param heel_params: 横倾参数元组（current_angle, target_angle）
    :param left_ext: 左侧截流板当前伸缩量（单位mm）
    :param right_ext: 右侧截流板当前伸缩量（单位mm）
    :return: (new_left_ext, new_right_ext) 更新后的两侧伸缩量
    """
    if mode == 1:  # 纵倾控制模式
        current, target = pitch_params
        new_left, new_right = PID_pitch_control(current, target, left_ext, right_ext, pid_pitch)
        return new_left, new_right
    elif mode == 2:  # 横倾控制模式
        current, target = heel_params
        new_left, new_right = PID_heel_control(current, target, left_ext, right_ext, pid_heel)
        return new_left, new_right
    else:
        raise ValueError("无效模式，模式应为1（纵倾）或2（横倾）")


def main():
    """
    主仿真函数：执行控制仿真并绘制结果曲线
    """
    speed = 50  # 航速（单位knots）
    target_pitch = 0  # 目标纵倾角度（单位度）
    target_heel = 0  # 目标横倾角度（单位度）
    left_ext = right_ext = 0  # 初始截流板伸缩量（单位mm）

    # 数据记录列表
    times = []  # 时间轴
    angles = []  # 角度记录
    left_extensions = []  # 左侧截流板伸缩量记录
    right_extensions = []  # 右侧截流板伸缩量记录

    mode = 1  # 控制模式（1=纵倾，2=横倾）
    for t in range(300):  # 仿真300个时间步
        times.append(t * dt)  # 记录当前时间

        if mode == 1:  # 纵倾控制模式
            # 计算等效截流板伸缩量（取两侧平均值）
            equivalent_extension = (left_ext + right_ext) / 2
            current_angle = simulation_angle(speed, equivalent_extension)
            # 更新截流板状态
            left_ext, right_ext = PID_parameter_transfer(
                mode, (current_angle, target_pitch), None, left_ext, right_ext
            )
        else:  # 横倾控制模式
            # 计算等效截流板伸缩量（右侧减左侧）
            equivalent_extension = right_ext - left_ext
            current_angle = simulation_angle(speed, equivalent_extension)
            # 更新截流板状态
            left_ext, right_ext = PID_parameter_transfer(
                mode, None, (current_angle, target_heel), left_ext, right_ext
            )

        # 记录当前状态
        angles.append(current_angle)
        left_extensions.append(left_ext)
        right_extensions.append(right_ext)

    # 绘图部分
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 设置角度曲线（左Y轴）
    if mode == 1:
        ax1.set_ylabel('Pitch Angle (degrees)', color='tab:red')
        angle_line, = ax1.plot(times, angles, color='tab:red', label='Pitch Angle')
    else:
        ax1.set_ylabel('Heel Angle (degrees)', color='tab:green')
        angle_line, = ax1.plot(times, angles, color='tab:green', label='Heel Angle')
    ax1.tick_params(axis='y', labelcolor='tab:red' if mode == 1 else 'tab:green')
    ax1.set_xlabel('Time (s)')

    # 设置截流板曲线（右Y轴）
    ax2 = ax1.twinx()
    left_line, = ax2.plot(times, left_extensions, 'b--', label='Left')
    right_line, = ax2.plot(times, right_extensions, 'g-.', label='Right')
    ax2.set_ylabel('Extension (mm)')
    ax2.tick_params(axis='y')

    # 添加图例
    lines = [angle_line, left_line, right_line]
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper right')

    # 设置标题
    plt.title("Pitch Control" if mode == 1 else "Heel Control")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()