# app.py (Corriendo en la VM de Google Cloud)
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/predict', methods=['POST'], strict_slashes=False)
def predict():
    data = request.json
    vibration = data.get("vibration", 0)
    temperature = data.get("temperature", 0)
    
    # Simulación de lógica de IA (Reemplazar por tu modelo de Scikit-Learn/TensorFlow)
    anomaly_detected = False
    if vibration > 4.5 or temperature > 78.0:
        anomaly_detected = True
        
    return jsonify({
        "status": "success",
        "anomaly": anomaly_detected,
        "recommendation": "STOP_LINE" if anomaly_detected else "CONTINUE"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
