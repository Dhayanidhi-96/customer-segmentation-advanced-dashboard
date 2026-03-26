from __future__ import annotations

import pandas as pd


SEGMENT_MAP = {
    "555": "VIP",
    "554": "VIP",
    "544": "VIP",
    "543": "Loyal",
    "444": "Loyal",
    "435": "Loyal",
    "155": "At-Risk",
    "154": "At-Risk",
    "144": "At-Risk",
    "111": "Churned",
    "112": "Churned",
    "121": "Churned",
    "512": "New",
    "511": "New",
    "411": "New",
    "311": "Potential",
    "331": "Potential",
}


def _score_series(series: pd.Series, reverse: bool = False) -> pd.Series:
    rank = series.rank(method="first", ascending=not reverse)
    bins = pd.qcut(rank, 5, labels=[1, 2, 3, 4, 5])
    return bins.astype(int)


def score_rfm(features_df: pd.DataFrame) -> pd.DataFrame:
    if features_df.empty:
        return pd.DataFrame(columns=["customer_id", "r_score", "f_score", "m_score", "rfm_total_score", "segment_label"])

    result = features_df[["customer_id", "recency_days", "frequency", "monetary"]].copy()
    result["r_score"] = _score_series(result["recency_days"], reverse=True)
    result["f_score"] = _score_series(result["frequency"], reverse=False)
    result["m_score"] = _score_series(result["monetary"], reverse=False)
    result["rfm_code"] = result[["r_score", "f_score", "m_score"]].astype(str).agg("".join, axis=1)
    result["segment_label"] = result["rfm_code"].map(SEGMENT_MAP).fillna("Potential")
    result["rfm_total_score"] = result["r_score"] + result["f_score"] + result["m_score"]
    return result
