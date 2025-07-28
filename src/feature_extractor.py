import pandas as pd

def extract_features_from_spans(spans):
    df = pd.DataFrame(spans)
    return df  # Assumes all features already computed in extract_spans_from_pdf

def align_features(df, feature_columns):
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    return df[feature_columns]
