import os, joblib
from scipy.interpolate import interp1d
import numpy as np

# speed = [0, 20.6, 24.5, 28.3, 32.2, 36.2, 42]
# extension = [1.0, 0.75, 0.7, 0.5, 0.4, 0.15, 0.03]
# os.makedirs('model', exist_ok=True)
# extension_limit_model = interp1d(speed, extension, kind='cubic', fill_value='extrapolate')

# 构造离散航速(x)和对应比例(y) 
x = np.array([0, 20, 40])         # 航速(kn)
y = np.array([1.0, 1.0, -0.2])    # 比例

# 构建线性插值模型
extension_limit_model = interp1d(x, y, kind='linear', fill_value='extrapolate')

# 创建模型保存目录
os.makedirs('model', exist_ok=True)
joblib.dump(extension_limit_model, 'model/extension_limit_model.pkl')
