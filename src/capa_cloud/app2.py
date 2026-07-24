# app.py (Corriendo en la VM de Google Cloud - Actualizado)
from flask import Flask, request, jsonify
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# --- INTEGRACIÓN DEL MODELO DE IA ---
# Entrenamos un modelo rápido de clasificación al arrancar para detectar anomalías
# X = [Vibración, Temperatura]
X_train = np.array([
    [1.5, 50.0], [2.0, 55.0], [2.5, 60.0],  # Normales
    [4.8, 80.0], [5.2, 85.0], [4.6, 79.0]   # Anomalías
])
# y = 0 (Normal), 1 (Anomalía)
y_train = np.array([0, 0, 0, 1, 1, 1])

model = LogisticRegression()
model.fit(X_train, y_train)
# -------------------------------------

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
        
    vibration = float(data.get("vibration", 0))
    temperature = float(data.get("temperature", 0))
    
    # Inferencia con el modelo en ejecución
    features = np.array([[vibration, temperature]])
    prediction = model.predict(features)[0] # Devuelve 0 o 1
    
    anomaly_detected = bool(prediction == 1)
        
    return jsonify({
        "status": "success",
        "anomaly": anomaly_detected,
        "recommendation": "STOP_LINE" if anomaly_detected else "CONTINUE"
    })

if __name__ == '__main__':
    # Forzamos el puerto 8000 que está abierto en tu regla de firewall de GCP
    app.run(host='0.0.0.0', port=8000)
