from flask import Flask
from config import Config
import json
import numpy as np
import pandas as pd

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle numpy and pandas types"""
    def default(self, obj):
        if isinstance(obj, (np.float64, np.float32)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif pd.isna(obj):
            return None
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    app.json_encoder = CustomJSONEncoder
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
