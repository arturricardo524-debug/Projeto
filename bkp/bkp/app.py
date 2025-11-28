# app.py
from flask import Flask, render_template, request, jsonify
import joblib
import os
from treinar_modelo import limpar_texto, MODEL_FILE

app = Flask(__name__)

# tentar carregar modelo
if os.path.exists(MODEL_FILE):
    modelo = joblib.load(MODEL_FILE)
    print("[OK] modelo carregado.")
else:
    modelo = None
    print("[AVISO] modelo.pkl não encontrado. Rode 'python treinar_modelo.py'.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analisar", methods=["POST"])
def analisar():
    global modelo
    if modelo is None:
        return jsonify({"error":"Modelo não carregado."}), 500

    data = request.get_json()
    texto = data.get("texto", "").strip()

    if not texto:
        return jsonify({"error": "Texto vazio."}), 400

    clean = limpar_texto(texto)
    prob = modelo.predict_proba([clean])[0][1]  # probabilidade de FAKE
    pred = "FAKE" if prob >= 0.5 else "REAL"

    return jsonify({
        "resultado": pred,
        "prob_fake": float(prob)
    })

if __name__ == "__main__":
    app.run(debug=True)
