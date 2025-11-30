import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import os

DATASET_FILE = "dataset_enriquecido.csv"

def carregar_dataset():
    df = pd.read_csv(DATASET_FILE)

    if "text" in df.columns and "label" in df.columns:
        df = df[["text", "label"]].dropna()
    else:
        raise ValueError("Dataset precisa ter colunas text e label.")

    return df

def salvar(fig, nome):
    os.makedirs("graficos", exist_ok=True)
    fig.savefig(f"graficos/{nome}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

def grafico_distribuicao_classes(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df["label"].value_counts().plot(kind="bar", ax=ax)
    ax.set_title("Distribuição de classes (Fake vs Real)")
    ax.set_xlabel("Classe")
    ax.set_ylabel("Quantidade")
    salvar(fig, "1_distribuicao_classes")

def grafico_tamanho_textos(df):
    df["tamanho"] = df["text"].apply(lambda x: len(str(x).split()))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df["tamanho"], bins=20)
    ax.set_title("Distribuição do tamanho dos textos")
    ax.set_xlabel("Número de palavras")
    ax.set_ylabel("Frequência")

    salvar(fig, "2_tamanho_textos")

def grafico_wordcloud(df):
    textos_fake = " ".join(df[df["label"] == 1]["text"])
    textos_real = " ".join(df[df["label"] == 0]["text"])

    wc_fake = WordCloud(width=800, height=400, background_color="white").generate(textos_fake)
    wc_real = WordCloud(width=800, height=400, background_color="white").generate(textos_real)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    axes[0].imshow(wc_fake, interpolation="bilinear")
    axes[0].set_title("WordCloud - Fake News")
    axes[0].axis("off")

    axes[1].imshow(wc_real, interpolation="bilinear")
    axes[1].set_title("WordCloud - Notícias Reais")
    axes[1].axis("off")

    salvar(fig, "3_wordcloud_fake_vs_real")

def grafico_top_palavras(df):
    from collections import Counter
    import re

    def limpar(texto):
        return re.sub(r"[^a-zA-Záéíóúãõâêôç ]", "", texto.lower())

    palavras = " ".join(df["text"].apply(limpar)).split()
    contagem = Counter(palavras).most_common(20)

    palavras, valores = zip(*contagem)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(palavras, valores)
    plt.xticks(rotation=45, ha="right")
    ax.set_title("Top 20 palavras mais frequentes")
    ax.set_ylabel("Frequência")

    salvar(fig, "4_top20_palavras")

def main():
    df = carregar_dataset()

    print("Gerando gráficos...")

    grafico_distribuicao_classes(df)
    grafico_tamanho_textos(df)
    grafico_wordcloud(df)
    grafico_top_palavras(df)

    print("Gráficos salvos na pasta 'graficos/'")

if __name__ == "__main__":
    main()
