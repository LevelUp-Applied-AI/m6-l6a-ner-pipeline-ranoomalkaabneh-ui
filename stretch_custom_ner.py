import pandas as pd
import spacy
from spacy.pipeline import EntityRuler


STANDARD_LABELS = {
    "ORG", "GPE", "DATE", "LAW", "MONEY",
    "PERSON", "QUANTITY", "LOC", "EVENT", "WORK_OF_ART"
}


def load_data(filepath="data/climate_articles.csv"):
    return pd.read_csv(filepath)


def load_gold(filepath="data/gold_entities.csv"):
    return pd.read_csv(filepath)


def climate_patterns():
    """Return custom climate-domain EntityRuler patterns."""
    return [
        {"label": "CLIMATE_EVENT", "pattern": "COP28"},
        {"label": "CLIMATE_EVENT", "pattern": "COP27"},
        {"label": "CLIMATE_EVENT", "pattern": "UN Climate Change Conference"},

        {"label": "AGREEMENT", "pattern": "Paris Agreement"},
        {"label": "AGREEMENT", "pattern": "Kyoto Protocol"},

        {"label": "REPORT", "pattern": "IPCC AR6"},
        {"label": "REPORT", "pattern": "Sixth Assessment Report"},
        {"label": "REPORT", "pattern": "Emissions Gap Report"},

        {"label": "THRESHOLD", "pattern": "2°C target"},
        {"label": "THRESHOLD", "pattern": "1.5°C"},
        {
            "label": "THRESHOLD",
            "pattern": [
                {"LIKE_NUM": True},
                {"TEXT": {"REGEX": "°C|degrees"}},
                {"LOWER": {"IN": ["target", "limit", "threshold"]}, "OP": "?"}
            ],
        },

        {"label": "POLICY", "pattern": "Nationally Determined Contributions"},
        {"label": "POLICY", "pattern": "NDCs"},
        {"label": "POLICY", "pattern": "net-zero pledge"},
        {"label": "POLICY", "pattern": "carbon pricing"},
    ]


def build_pipeline(position="after"):
    """
    Build spaCy pipeline with EntityRuler either before or after built-in NER.

    position: "before" or "after"
    """
    nlp = spacy.load("en_core_web_sm")

    if "entity_ruler" in nlp.pipe_names:
        nlp.remove_pipe("entity_ruler")

    if position == "before":
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    elif position == "after":
        ruler = nlp.add_pipe("entity_ruler", after="ner")
    else:
        raise ValueError("position must be 'before' or 'after'")

    ruler.add_patterns(climate_patterns())

    return nlp


def extract_entities(df, nlp):
    """Extract entities from English texts only."""
    rows = []

    for _, row in df[df["language"] == "en"].iterrows():
        doc = nlp(row["text"])

        for ent in doc.ents:
            rows.append({
                "text_id": row["id"],
                "entity_text": ent.text,
                "entity_label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
            })

    return pd.DataFrame(
        rows,
        columns=["text_id", "entity_text", "entity_label", "start_char", "end_char"]
    )


def entity_count_table(base_df, before_df, after_df):
    """Compare entity counts by label."""
    table = pd.DataFrame({
        "Base spaCy": base_df["entity_label"].value_counts(),
        "Ruler Before NER": before_df["entity_label"].value_counts(),
        "Ruler After NER": after_df["entity_label"].value_counts(),
    }).fillna(0).astype(int)

    table.loc["TOTAL"] = table.sum()
    return table


def evaluate_standard_labels(predicted_df, gold_df):
    """
    Evaluate only overlapping standard-label entities.

    Custom labels are excluded because gold_entities.csv does not contain them.
    """
    pred_filtered = predicted_df[predicted_df["entity_label"].isin(STANDARD_LABELS)]
    gold_filtered = gold_df[gold_df["entity_label"].isin(STANDARD_LABELS)]

    pred_set = set(zip(
        pred_filtered["text_id"],
        pred_filtered["entity_text"],
        pred_filtered["entity_label"]
    ))

    gold_set = set(zip(
        gold_filtered["text_id"],
        gold_filtered["entity_text"],
        gold_filtered["entity_label"]
    ))

    tp = len(pred_set & gold_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)

    precision = tp / (tp + fp) if tp + fp > 0 else 0.0
    recall = tp / (tp + fn) if tp + fn > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def metrics_table(base_metrics, before_metrics, after_metrics):
    table = pd.DataFrame({
        "Metric": ["Precision", "Recall", "F1"],
        "Base spaCy": [
            base_metrics["precision"],
            base_metrics["recall"],
            base_metrics["f1"],
        ],
        "Ruler Before NER": [
            before_metrics["precision"],
            before_metrics["recall"],
            before_metrics["f1"],
        ],
        "Ruler After NER": [
            after_metrics["precision"],
            after_metrics["recall"],
            after_metrics["f1"],
        ],
    })

    for col in ["Base spaCy", "Ruler Before NER", "Ruler After NER"]:
        table[col] = table[col].map(lambda x: f"{x:.4f}")

    return table


def show_custom_examples(df, ruler_df, max_examples=12):
    """Print examples where custom labels fired."""
    custom_df = ruler_df[~ruler_df["entity_label"].isin(STANDARD_LABELS)]

    print("\nCustom Rule Examples")
    print("--------------------")

    shown = 0

    for _, ent in custom_df.iterrows():
        text_id = ent["text_id"]
        text = df.loc[df["id"] == text_id, "text"].iloc[0]

        print(f"\nText ID: {text_id}")
        print(f"Custom entity: {ent['entity_text']} [{ent['entity_label']}]")
        print(f"Text: {text}")

        shown += 1
        if shown >= max_examples:
            break


if __name__ == "__main__":
    df = load_data()
    gold = load_gold()

    base_nlp = spacy.load("en_core_web_sm")
    before_nlp = build_pipeline(position="before")
    after_nlp = build_pipeline(position="after")

    base_entities = extract_entities(df, base_nlp)
    before_entities = extract_entities(df, before_nlp)
    after_entities = extract_entities(df, after_nlp)

    print("\nEntity Count Summary")
    counts = entity_count_table(base_entities, before_entities, after_entities)
    print(counts.to_markdown())

    base_metrics = evaluate_standard_labels(base_entities, gold)
    before_metrics = evaluate_standard_labels(before_entities, gold)
    after_metrics = evaluate_standard_labels(after_entities, gold)

    print("\nEvaluation on Standard Gold Labels Only")
    eval_table = metrics_table(base_metrics, before_metrics, after_metrics)
    print(eval_table.to_markdown(index=False))

    show_custom_examples(df, before_entities)

    base_entities.to_csv("base_spacy_entities.csv", index=False)
    before_entities.to_csv("custom_rules_before_ner_entities.csv", index=False)
    after_entities.to_csv("custom_rules_after_ner_entities.csv", index=False)

    print("\nSaved output CSV files.")