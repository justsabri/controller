import os, joblib
from scipy.interpolate import interp1d


speed = []
extension = []
os.makedirs('model', exist_ok=True)
extension_limit_model = interp1d(speed, extension, kind='cubic', fill_value='extrapolate')
joblib.dump(extension_limit_model, 'model/extension_limit_model.pkl')
