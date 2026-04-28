"""
Module 6 Week A — Lab: NER Pipeline

Build and compare Named Entity Recognition pipelines using spaCy
and Hugging Face on climate-related text data.

Run: python ner_pipeline.py
"""

import pandas as pd
import numpy as np
import spacy
from transformers import pipeline as hf_pipeline


def load_data(filepath="data/climate_articles.csv"):
    """Load the climate articles dataset.

    Args:
        filepath: Path to the CSV file.

    Returns:
        DataFrame with columns: id, text, source, language, category.
    """
    df = pd.read_csv(filepath)
    return df




def explore_data(df):
    """Summarize basic corpus statistics.

    Args:
        df: DataFrame returned by load_data.

    Returns:
        Dictionary with keys:
          'shape': tuple (n_rows, n_cols)
          'lang_counts': dict mapping language code -> row count
          'category_counts': dict mapping category -> row count
          'text_length_stats': dict with 'mean', 'min', 'max' word counts
    """
    dict_summary = {}
    dict_summary['shape'] = df.shape
    dict_summary['lang_counts'] = df['language'].value_counts().to_dict()
    dict_summary['category_counts'] = df['category'].value_counts().to_dict()
    text_lengths = df['text'].apply(lambda x: len(str(x).split()))
    dict_summary['text_length_stats'] = {
        'mean': text_lengths.mean(),
        'min': text_lengths.min(),
        'max': text_lengths.max()
    }   
    return dict_summary

def preprocess_text(text, nlp):
    """Preprocess a single text string for NLP analysis.

    Normalize Unicode, lowercase, remove punctuation, tokenize,
    and lemmatize using the injected spaCy pipeline.

    Args:
        text: Raw text string.
        nlp: A loaded spaCy Language object (e.g., en_core_web_sm).

    Returns:
        List of cleaned, lemmatized token strings.
    """
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space]
    return tokens


def extract_spacy_entities(df, nlp):
    """Extract named entities from English texts using spaCy NER.

    Args:
        df: DataFrame with columns id, text, language, ...
        nlp: A loaded spaCy Language object.

    Returns:
        DataFrame with columns: text_id, entity_text, entity_label,
        start_char, end_char.
    """
    entities = []
    for _, row in df[df['language'] == 'en'].iterrows():
        doc = nlp(row['text'])
        for ent in doc.ents:
            entities.append({
                'text_id': row['id'],
                'entity_text': ent.text,
                'entity_label': ent.label_,
                'start_char': ent.start_char,
                'end_char': ent.end_char
            })
    return pd.DataFrame(entities)



def strip_iob(label):
    """Remove B- or I- prefix from Hugging Face NER labels."""
    return label.replace("B-", "").replace("I-", "")



def extract_hf_entities(df,ner_pipeline):
    """Extract named entities from English texts using Hugging Face NER.

    Uses the injected HF pipeline (expected: dslim/bert-base-NER).

    Args:
        df: DataFrame with columns id, text, language, ...
        ner_pipeline: A loaded Hugging Face `pipeline('ner', ...)` object.

    Returns:
        DataFrame with columns: text_id, entity_text, entity_label,
        start_char, end_char.
    """
    entities = []

    for _, row in df[df["language"] == "en"].iterrows():
        ner_results = ner_pipeline(row["text"])

        current_entity = None

        for ent in ner_results:
            word = ent["word"]
            label = strip_iob(ent["entity"])
            start = ent["start"]
            end = ent["end"]

            if word.startswith("##"):
                if current_entity is not None:
                    current_entity["entity_text"] += word[2:]
                    current_entity["end_char"] = end
                continue

            if current_entity is not None:
                entities.append(current_entity)

            current_entity = {
                "text_id": row["id"],
                "entity_text": word,
                "entity_label": label,
                "start_char": start,
                "end_char": end
            }

        if current_entity is not None:
            entities.append(current_entity)

    return pd.DataFrame(
        entities,
        columns=["text_id", "entity_text", "entity_label", "start_char", "end_char"]
    )

def compare_ner_outputs(spacy_df, hf_df):
    """Compare entity extraction results from spaCy and Hugging Face.

    Args:
        spacy_df: DataFrame of spaCy entities (from extract_spacy_entities).
        hf_df: DataFrame of HF entities (from extract_hf_entities).

    Returns:
        Dictionary with keys:
          'spacy_counts': dict of entity_label -> count for spaCy
          'hf_counts': dict of entity_label -> count for HF
          'total_spacy': int total entities from spaCy
          'total_hf': int total entities from HF
          'both': set of (text_id, entity_text) tuples found by both systems
          'spacy_only': set of (text_id, entity_text) tuples found only by spaCy
          'hf_only': set of (text_id, entity_text) tuples found only by HF
    """
   
    spacy_counts = spacy_df["entity_label"].value_counts().to_dict()
    hf_counts = hf_df["entity_label"].value_counts().to_dict()

    total_spacy = len(spacy_df)
    total_hf = len(hf_df)

    spacy_set = set(zip(spacy_df["text_id"], spacy_df["entity_text"]))
    hf_set = set(zip(hf_df["text_id"], hf_df["entity_text"]))

    both = spacy_set.intersection(hf_set)
    spacy_only = spacy_set.difference(hf_set)
    hf_only = hf_set.difference(spacy_set)

    spacy_series = spacy_df["entity_label"].value_counts().rename("spaCy")
    hf_series = hf_df["entity_label"].value_counts().rename("Hugging Face")

    count_table = pd.concat([spacy_series, hf_series], axis=1).fillna(0)
    count_table = count_table.apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)

    count_table.loc["TOTAL"] = count_table.sum()

    return {
        "spacy_counts": spacy_counts,
        "hf_counts": hf_counts,
        "total_spacy": total_spacy,
        "total_hf": total_hf,
        "both": both,
        "spacy_only": spacy_only,
        "hf_only": hf_only,
        "count_table": count_table
    }

def evaluate_ner(predicted_df, gold_df):
    """Evaluate NER predictions against gold-standard annotations.

    Computes entity-level precision, recall, and F1. An entity is a
    true positive if both the entity text and label match a gold entry
    for the same text_id.

    Args:
        predicted_df: DataFrame with columns text_id, entity_text,
                      entity_label.
        gold_df: DataFrame with columns text_id, entity_text,
                 entity_label.

    Returns:
        Dictionary with keys: 'precision', 'recall', 'f1' (floats 0-1).
    """
    pred_set = set(zip(predicted_df['text_id'], predicted_df['entity_text'], predicted_df['entity_label']))
    gold_set = set(zip(gold_df['text_id'], gold_df['entity_text'], gold_df['entity_label']))

    tp = len(pred_set.intersection(gold_set))
    fp = len(pred_set.difference(gold_set))
    fn = len(gold_set.difference(pred_set))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

   


if __name__ == "__main__":
    # Load spaCy and HF models once, reuse across functions
    nlp = spacy.load("en_core_web_sm")
    hf_ner = hf_pipeline("ner", model="dslim/bert-base-NER")

    # Load and explore
    df = load_data()
    if df is not None:
        summary = explore_data(df)
        if summary is not None:
            print(f"Shape: {summary['shape']}")
            print(f"Languages: {summary['lang_counts']}")
            print(f"Categories: {summary['category_counts']}")
            print(f"Text length (words): {summary['text_length_stats']}")

        # Preprocess a sample to verify your function
        sample_row = df[df["language"] == "en"].iloc[0]
        sample_tokens = preprocess_text(sample_row["text"], nlp)
        if sample_tokens is not None:
            print(f"\nSample preprocessed tokens: {sample_tokens[:10]}")

        # spaCy NER across the English corpus
        spacy_entities = extract_spacy_entities(df, nlp)
        if spacy_entities is not None:
            print(f"\nspaCy entities: {len(spacy_entities)} total")

        # HF NER across the English corpus
        hf_entities = extract_hf_entities(df, hf_ner)
        if hf_entities is not None:
            print(f"HF entities: {len(hf_entities)} total")

        # Compare the two systems
    if spacy_entities is not None and hf_entities is not None:

        comparison = compare_ner_outputs(spacy_entities, hf_entities)
    if comparison is not None:
        print(f"\nBoth systems agreed on {len(comparison['both'])} entities")
        print(f"spaCy-only: {len(comparison['spacy_only'])}")
        print(f"HF-only: {len(comparison['hf_only'])}")

        print("\nEntity Count Summary")
        print(comparison["count_table"].to_markdown())

       # Evaluate against gold standard
gold = pd.read_csv("data/gold_entities.csv")

if spacy_entities is not None:
    spacy_metrics = evaluate_ner(spacy_entities, gold)
    if spacy_metrics is not None:
        print(f"\nspaCy evaluation: {spacy_metrics}")

if hf_entities is not None:
    hf_metrics = evaluate_ner(hf_entities, gold)
    if hf_metrics is not None:
        print(f"HF evaluation: {hf_metrics}")

metrics_table = pd.DataFrame({
    "Metric": ["Precision", "Recall", "F1"],
    "spaCy": [
        spacy_metrics["precision"],
        spacy_metrics["recall"],
        spacy_metrics["f1"],
    ],
    "Hugging Face": [
        hf_metrics["precision"],
        hf_metrics["recall"],
        hf_metrics["f1"],
    ],
})

metrics_table["spaCy"] = metrics_table["spaCy"].map(lambda x: f"{x:.4f}")
metrics_table["Hugging Face"] = metrics_table["Hugging Face"].map(lambda x: f"{x:.4f}")

print("\nGold Standard Evaluation")
print(metrics_table.to_markdown(index=False))