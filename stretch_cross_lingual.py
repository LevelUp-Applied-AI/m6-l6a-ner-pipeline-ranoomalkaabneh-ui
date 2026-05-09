import pandas as pd
import numpy as np
import torch
import seaborn as sns
import matplotlib.pyplot as plt

from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# Load Data
# -----------------------------
def load_data(filepath="data/climate_articles.csv"):
    df = pd.read_csv(filepath)
    return df


# -----------------------------
# Select 10 EN + 10 AR
# -----------------------------
def prepare_texts(df):

    en_df = df[df["language"] == "en"]
    ar_df = df[df["language"] == "ar"]

    en_texts = en_df["text"].head(10).tolist()
    ar_texts = ar_df["text"].head(10).tolist()

    return en_texts, ar_texts


# -----------------------------
# Load Multilingual BERT
# -----------------------------
def load_model():

    model_name = "bert-base-multilingual-cased"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    model.eval()
    return tokenizer, model


# -----------------------------
# Mean Pooling Embedding
# -----------------------------
def get_embedding(text, tokenizer, model):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    token_embeddings = outputs.last_hidden_state
    mask = inputs["attention_mask"].unsqueeze(-1)

    mask = mask.expand(token_embeddings.size()).float()

    summed = torch.sum(token_embeddings * mask, dim=1)
    counts = torch.clamp(mask.sum(dim=1), min=1e-9)

    return (summed / counts).squeeze().numpy()


# -----------------------------
# Batch Embeddings
# -----------------------------
def encode_texts(texts, tokenizer, model):

    return np.array([
        get_embedding(t, tokenizer, model)
        for t in texts
    ])


# -----------------------------
# Similarity Matrix (20x20)
# -----------------------------
def build_similarity_matrix(en_emb, ar_emb):

    all_emb = np.vstack((en_emb, ar_emb))
    return cosine_similarity(all_emb)


# -----------------------------
# Labels
# -----------------------------
def build_labels(en_texts, ar_texts):

    labels = []

    for t in en_texts:
        labels.append("EN: " + t[:40])

    for t in ar_texts:
        labels.append("AR: " + t[:40])

    return labels


# -----------------------------
# Heatmap
# -----------------------------
def plot_heatmap(matrix, labels):

    plt.figure(figsize=(14, 12))

    sns.heatmap(
        matrix,
        xticklabels=labels,
        yticklabels=labels,
        cmap="coolwarm"
    )

    plt.title("Cross-Lingual Embedding Similarity (mBERT)")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig("cross_lingual_heatmap.png")
    plt.show()


# -----------------------------
# Cross-lingual scoring
# -----------------------------
def analyze_pairs(en_emb, ar_emb, en_texts, ar_texts):

    print("\nCross-Lingual Similarity Scores:\n")

    for i in range(10):

        score = cosine_similarity(
            [en_emb[i]],
            [ar_emb[i]]
        )[0][0]

        print(f"Pair {i+1}: {score:.4f}")
        print("EN:", en_texts[i][:80])
        print("AR:", ar_texts[i][:80])
        print("-" * 60)


# -----------------------------
# Main
# -----------------------------
def main():

    df = load_data()

    en_texts, ar_texts = prepare_texts(df)

    tokenizer, model = load_model()

    en_emb = encode_texts(en_texts, tokenizer, model)
    ar_emb = encode_texts(ar_texts, tokenizer, model)

    matrix = build_similarity_matrix(en_emb, ar_emb)

    labels = build_labels(en_texts, ar_texts)

    plot_heatmap(matrix, labels)

    analyze_pairs(en_emb, ar_emb, en_texts, ar_texts)


if __name__ == "__main__":
    main()