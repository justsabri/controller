"""
声明：
1. 当前算法为其他程序调用和本程序仿真两部分构成，既可以实现其他函数的调用，又可以实现仿真测试。
2. 当前采用的控制为基础的PID，主要原因是缺少真实数据。
3. 算法开发的逻辑是，先使用最基础的方法，便于排查问题/优化效果。待当前程序正常运行后，再升级算法/优化效果。
4. 当前的函数构成说明：
        PID_parameter_transfer函数：PID参数传递函数，用于接收外部参数，并传递给控制部分

        PIDControler类：PID控制的核心逻辑
        simulation_angle函数：模拟纵倾/横倾输出函数，给定航速和截流板伸缩量，计算纵倾/横倾角
        PID_pitch_control函数：PID纵倾控制函数
        PID_heel_control函数：PID横倾控制函数
        main函数：主函数
"""

"""
模式说明：
采用比特位传输，二进制的“XYZ”中Z表示纵倾/纵摇是否运行，Y表示横倾/横摇是否运行，X表示在YZ的基础上是否进行拓展

  模式        比特位
         二进制   十进制
纵倾/纵摇：001      1
横倾/横摇：010      2
舒适优先： 011      3
速度优先： 101      5
协调转弯： 110      6

"""

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
# 纵倾控制全局参数
Kp_pitch = 0.6  # 纵倾比例系数
Ki_pitch = 0.02  # 纵倾积分系数
Kd_pitch = 0.1  # 纵倾微分系数

# 横倾控制全局参数
Kp_heel = 0.5  # 横倾比例系数
Ki_heel = 0.01  # 横倾积分系数
Kd_heel = 0.05  # 横倾微分系数

max_extension = 50  # 截流板最大伸缩量（单位mm）
dt = 0.1  # 时间间隔（单位秒）

# 初始化PID控制器
pid_pitch = PIDController(Kp_pitch, Ki_pitch, Kd_pitch)  # 纵倾PID控制器
pid_heel = PIDController(Kp_heel, Ki_heel, Kd_heel)  # 横倾PID控制器

# 输入输出函数
def PID_parameter_transfer(mode, speed, pitch_angle_params, heel_angle_params,
                           actual_extensions, max_extension=50.0):
    """
    船舶姿态控制参数分发函数
    :param mode: 整型，控制模式（1=纵倾，2=横倾，3=舒适优先，6=协调转弯）
    :param speed: 浮点型，当前船舶航速（单位：节），用于后续扩展速度相关控制
    :param pitch_angle_params: 元组，纵倾参数(current_angle, target_angle)，
    :param heel_angle_params: 元组，横倾参数(current_angle, target_angle)，
    :param actual_extensions: 元组，左右截流板当前伸缩量(left_current, right_current)（单位：毫米）
    :param max_extension: 浮点型，截流板最大允许伸缩量（左右共用，单位：毫米）
    :return: 元组，更新后的左右伸缩量(new_left, new_right)
    """
    # 解包当前伸缩量参数
    left_current, right_current = actual_extensions  # 左侧当前值赋值给left_current，右侧同理

    if mode == 1:  # 纵倾控制模式
        # 验证纵倾参数的目标角度为None时设定默认值
        if pitch_angle_params[1] == None:
            pitch_angle_params[1] = -1.0

        # 调用纵倾控制核心算法
        new_left, new_right = PID_pitch_control(
            current_angle=pitch_angle_params[0],  # 当前纵倾角度
            target_angle=pitch_angle_params[1],  # 目标纵倾角度
            left_current=left_current,  # 左侧当前伸缩量
            right_current=right_current,  # 右侧当前伸缩量
            max_extension=max_extension,  # 最大允许伸缩量
            pid=pid_pitch  # PID控制器实例
        )

    elif mode == 2:  # 横倾控制模式
        # 验证横倾参数的目标角度为None时设定默认值
        if heel_angle_params[1] == None:
            heel_angle_params[1] = 0

        # 调用横倾控制核心算法
        new_left, new_right = PID_heel_control(
            current_angle=heel_angle_params[0],  # 当前横倾角度
            target_angle=heel_angle_params[1],  # 目标横倾角度
            left_current=left_current,  # 左侧当前伸缩量
            right_current=right_current,  # 右侧当前伸缩量
            max_extension=max_extension,  # 最大允许伸缩量
            pid=pid_heel  # PID控制器实例
        )

    elif mode == 3:  # 舒适优先模式（功能未实现，返回当前值）
        new_left, new_right = left_current, right_current  # 保持当前状态

    elif mode == 6:  # 协调转弯模式（功能未实现，返回当前值）
        new_left, new_right = left_current, right_current  # 保持当前状态

    else:
        raise ValueError("无效控制模式，当前支持模式：纵倾控制/横倾控制/舒适优先/协调转弯")

    return new_left, new_right  # 返回更新后的伸缩量元组

# 纵倾控制
def PID_pitch_control(current_angle, target_angle, left_current, right_current, max_extension, pid):
    """
    纵倾控制核心算法：同步调整两侧截流板
    :param current_angle: 浮点型，当前纵倾角度（单位：度）
    :param target_angle: 浮点型，目标纵倾角度（单位：度）
    :param left_current: 浮点型，左侧截流板当前伸缩量（单位：毫米）
    :param right_current: 浮点型，右侧截流板当前伸缩量（单位：毫米）
    :param max_extension: 浮点型，截流板最大允许伸缩量（单位：毫米）
    :param pid: PID控制器实例
    :return: 元组，更新后的左右伸缩量(new_left, new_right)
    """
    error = target_angle - current_angle  # 计算目标与当前角度的误差
    output = pid.compute(error, dt)  # 通过PID计算调整量

    # 同步调整两侧伸缩量（同增同减）
    new_left = left_current + output  # 计算左侧新伸缩量
    new_right = right_current + output  # 计算右侧新伸缩量

    # 应用物理限制：不允许小于0或超过最大值
    new_left = max(0.0, min(new_left, max_extension))  # 限制左侧范围
    new_right = max(0.0, min(new_right, max_extension))  # 限制右侧范围

    return new_left, new_right  # 返回调整后的伸缩量

# 横倾控制
def PID_heel_control(current_angle, target_angle, left_current, right_current, max_extension, pid):
    """
    横倾控制核心算法：反向调整两侧截流板
    :param current_angle: 浮点型，当前横倾角度（单位：度）
    :param target_angle: 浮点型，目标横倾角度（单位：度）
    :param left_current: 浮点型，左侧截流板当前伸缩量（单位：毫米）
    :param right_current: 浮点型，右侧截流板当前伸缩量（单位：毫米）
    :param max_extension: 浮点型，截流板最大允许伸缩量（单位：毫米）
    :param pid: PID控制器实例
    :return: 元组，更新后的左右伸缩量(new_left, new_right)
    """
    error = target_angle - current_angle  # 计算目标与当前角度的误差
    output = pid.compute(error, dt)  # 通过PID计算调整量

    if error > 0:  # 需要向右舷倾斜的情况
        adj_left = left_current - output  # 收回左侧截流板
        adj_right = right_current + output  # 伸出右侧截流板
    else:  # 需要向左舷倾斜的情况
        adj_left = left_current + output  # 伸出左侧截流板
        adj_right = right_current - output  # 收回右侧截流板

    # 应用物理限制：不允许小于0或超过最大值
    new_left = max(0.0, min(adj_left, max_extension))  # 限制左侧范围
    new_right = max(0.0, min(adj_right, max_extension))  # 限制右侧范围

    return new_left, new_right  # 返回调整后的伸缩量



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

    mode = 2  # 控制模式（1=纵倾，2=横倾）
    for t in range(300):  # 仿真300个时间步
        times.append(t * dt)  # 记录当前时间

        if mode == 1:  # 纵倾控制模式
            # 计算等效截流板伸缩量（取两侧平均值）
            equivalent_extension = (left_ext + right_ext) / 2
            current_angle = simulation_angle(speed, equivalent_extension)
            # 更新截流板状态
            left_ext, right_ext = PID_parameter_transfer(
                mode, None, (current_angle, target_pitch), None, (left_ext, right_ext),max_extension=50.0
            )

        else:  # 横倾控制模式
            # 计算等效截流板伸缩量（右侧减左侧）
            equivalent_extension = right_ext - left_ext
            current_angle = simulation_angle(speed, equivalent_extension)
            # 更新截流板状态
            left_ext, right_ext = PID_parameter_transfer(
                mode, None, None, (current_angle, target_heel), (left_ext, right_ext),max_extension=50.0
            )

        # 记录当前状态
        angles.append(current_angle)
        left_extensions.append(left_ext)
        right_extensions.append(right_ext)

    # 绘图部分
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 设置角度曲线（左Y轴）
    if mode == 1:
        ax1.set_ylabel('Pitch Angle (°)', color='tab:red')
        angle_line, = ax1.plot(times, angles, color='tab:red', label='Pitch Angle')
    else:
        ax1.set_ylabel('Heel Angle (°)', color='tab:red')
        angle_line, = ax1.plot(times, angles, color='tab:red', label='Heel Angle')
    ax1.tick_params(axis='y', labelcolor='tab:red' if mode == 1 else 'tab:red')
    ax1.set_xlabel('Time (s)')

    # 设置截流板曲线（右Y轴）
    ax2 = ax1.twinx()
    left_line, = ax2.plot(times, left_extensions, 'b--', label='Left')
    right_line, = ax2.plot(times, right_extensions, 'g-.', label='Right')
    ax2.set_ylabel('Extension (mm)')
    ax2.tick_params(axis='y')

    # 添加图例（右上角，避免遮挡）
    lines = [angle_line, left_line, right_line]
    ax1.legend(
        lines,
        [l.get_label() for l in lines],
        loc='upper right',  # 放在右上角
        bbox_to_anchor=(0.95, 0.95),  # 确保图例在图表内
    )

    # 设置标题
    plt.title("Pitch Control" if mode == 1 else "Heel Control")
    # 调整布局，避免图例超出边界
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()