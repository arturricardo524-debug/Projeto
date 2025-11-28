
import os
import pandas as pd
import re, string
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

DATASET_FILE = "dataset_enriquecido.csv"  # Use o dataset novo
MODEL_FILE = "modelo.pkl"
RANDOM_STATE = 42

# Função de limpeza (necessária para o app.py)
def limpar_texto(texto):
    texto = str(texto).lower()
    texto = re.sub(r"http\\S+", "", texto)
    texto = texto.translate(str.maketrans("", "", string.punctuation))
    texto = re.sub(r"\\d+", "", texto)
    texto = re.sub(r"\\s+", " ", texto)
    return texto.strip()

def carregar_dataset(path=DATASET_FILE):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} não encontrado. Gere ou aponte para o dataset correto.")
    df = pd.read_csv(path)

    # Garante colunas corretas
    if "text" in df.columns and "label" in df.columns:
        df = df[["text", "label"]].dropna()
    else:
        if df.shape[1] >= 2:
            df = df.iloc[:, :2]
            df.columns = ["text", "label"]
        else:
            raise ValueError("Formato inválido: dataset precisa ter texto + label.")

    # Remove duplicatas e espaços
    df["text"] = df["text"].astype(str).str.strip()
    df = df.drop_duplicates(subset=["text", "label"])

    # Limpeza
    df["clean"] = df["text"].astype(str).apply(limpar_texto)
    return df

def treinar():
    df = carregar_dataset(DATASET_FILE)
    print("Registros carregados:", len(df))
    print("Distribuição de classes:\n", df["label"].value_counts())

    X = df["clean"]
    y = df["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    vetor = TfidfVectorizer(ngram_range=(1, 2), max_features=20000)
    clf = LogisticRegression(max_iter=3000, class_weight="balanced", random_state=RANDOM_STATE)

    pipeline = Pipeline([
        ("tfidf", vetor),
        ("clf", clf)
    ])

    print("Treinando modelo...")
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Acurácia no teste: {acc:.4f}")
    print("\nRelatório de classificação:\n")
    print(classification_report(y_test, preds))

    joblib.dump(pipeline, MODEL_FILE)
    print(f"Modelo salvo em {MODEL_FILE}")

if __name__ == "__main__":
    treinar()
