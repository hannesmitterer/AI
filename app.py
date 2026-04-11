from flask import Flask, jsonify, request
from flask_cors import CORS
from monitoring.resonance_check import ResonanceMonitor
import os

app = Flask(__name__)
CORS(app)  # Permette a Netlify di leggere i dati

# Inizializzazione con parametri bio-sincronizzati
monitor = ResonanceMonitor(
    soil_moisture=float(os.getenv("SOIL_MOISTURE", 0.62))
)

@app.route('/api/resonance', methods=['POST'])
def check_resonance():
    data = request.json
    prompt = data.get("prompt", "")
    responses = data.get("responses", [])
    
    report = monitor.evaluate_resonance(prompt, responses)
    return jsonify(report)

@app.route('/api/sroi', methods=['GET'])
def get_sroi():
    # Endpoint per il Dashboard su Netlify
    return jsonify({
        "sroi_value": 84.7,
        "status": "In Consensus Amoris",
        "anchor_cid": monitor.st_anchor_cid
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
