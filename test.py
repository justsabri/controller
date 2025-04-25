import os, joblib
from scipy.interpolate import interp1d


speed = [0, 20.6, 24.5, 28.3, 32.2, 36.2, 42]
extension = [1.0, 0.75, 0.7, 0.5, 0.4, 0.15, 0.03]
os.makedirs('model', exist_ok=True)
extension_limit_model = interp1d(speed, extension, kind='cubic', fill_value='extrapolate')
joblib.dump(extension_limit_model, 'model/extension_limit_model.pkl')
