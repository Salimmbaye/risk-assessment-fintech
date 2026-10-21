#!/usr/bin/env python3
"""
risk_scoring.py — turn the risk register into prioritized, scored output.

Reads  : data/risk-register.csv
Writes : outputs/risk-register-scored.csv   (adds inherent/residual scores + levels)
         outputs/risk-heatmap.png            (5x5 residual-risk heatmap)
         outputs/risk-summary.md             (counts by level and CSF function)

Usage  : python3 scripts/risk_scoring.py
Model  : Risk Score = Likelihood x Impact (1-5 scales). See
         docs/02-risk-assessment-methodology.md for the full methodology.
"""
from pathlib import Path
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "data" / "risk-register.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

LEVELS = [(1, 4, "Low"), (5, 9, "Moderate"), (10, 14, "High"), (15, 25, "Critical")]
LEVEL_ORDER = ["Low", "Moderate", "High", "Critical"]


def band(score: int) -> str:
    for lo, hi, name in LEVELS:
        if lo <= score <= hi:
            return name
    return "Unknown"


def load() -> pd.DataFrame:
    if not REGISTER.exists():
        sys.exit(f"ERROR: register not found at {REGISTER}")
    df = pd.read_csv(REGISTER)
    for col in ("Inherent_Likelihood", "Inherent_Impact",
                "Residual_Likelihood", "Residual_Impact"):
        df[col] = pd.to_numeric(df[col], errors="raise").clip(1, 5)
    return df


def score(df: pd.DataFrame) -> pd.DataFrame:
    df["Inherent_Score"] = df["Inherent_Likelihood"] * df["Inherent_Impact"]
    df["Residual_Score"] = df["Residual_Likelihood"] * df["Residual_Impact"]
    df["Inherent_Level"] = df["Inherent_Score"].apply(band)
    df["Residual_Level"] = df["Residual_Score"].apply(band)
    df["Risk_Reduction"] = df["Inherent_Score"] - df["Residual_Score"]
    return df.sort_values("Residual_Score", ascending=False).reset_index(drop=True)


def write_scored(df: pd.DataFrame) -> None:
    cols = ["Risk_ID", "Risk_Title", "CSF_Function", "CSF_Category",
            "Inherent_Likelihood", "Inherent_Impact", "Inherent_Score", "Inherent_Level",
            "Control_Effectiveness",
            "Residual_Likelihood", "Residual_Impact", "Residual_Score", "Residual_Level",
            "Risk_Reduction", "Treatment", "Risk_Owner", "Recommended_Controls", "Status"]
    df[cols].to_csv(OUT / "risk-register-scored.csv", index=False)


def heatmap(df: pd.DataFrame) -> None:
    """5x5 grid (Likelihood x Impact), each cell colored by its discrete risk
    band so colors match the legend exactly; risk IDs placed in their cells."""
    band_colors = {"Low": "#2e7d32", "Moderate": "#f9a825",
                   "High": "#ef6c00", "Critical": "#c62828"}
    band_index = {name: i for i, name in enumerate(LEVEL_ORDER)}
    idx_grid = np.zeros((5, 5), dtype=int)
    for i in range(5):        # impact index 0..4 -> impact 1..5
        for j in range(5):    # likelihood index 0..4 -> likelihood 1..5
            idx_grid[i, j] = band_index[band((j + 1) * (i + 1))]

    cmap = matplotlib.colors.ListedColormap([band_colors[n] for n in LEVEL_ORDER])
    fig, ax = plt.subplots(figsize=(8, 6.5))
    ax.imshow(idx_grid, cmap=cmap, origin="lower", vmin=0, vmax=3,
              aspect="auto", alpha=0.9)

    # place each risk's ID in its residual cell
    from collections import defaultdict
    cell = defaultdict(list)
    for _, r in df.iterrows():
        cell[(int(r.Residual_Likelihood) - 1, int(r.Residual_Impact) - 1)].append(r.Risk_ID)
    for (l, im), ids in cell.items():
        ax.text(l, im, "\n".join(ids), ha="center", va="center",
                fontsize=8, fontweight="bold", color="white")

    ax.set_xticks(range(5)); ax.set_xticklabels(range(1, 6))
    ax.set_yticks(range(5)); ax.set_yticklabels(range(1, 6))
    ax.set_xlabel("Likelihood", fontweight="bold")
    ax.set_ylabel("Impact", fontweight="bold")
    ax.set_title("NorthStar Lending — Residual Risk Heatmap (NIST CSF 2.0)",
                 fontweight="bold")
    # legend
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in
               ["#2e7d32", "#f9a825", "#ef6c00", "#c62828"]]
    ax.legend(handles, LEVEL_ORDER, title="Residual level",
              loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "risk-heatmap.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_summary(df: pd.DataFrame) -> None:
    by_level = df["Residual_Level"].value_counts().reindex(LEVEL_ORDER).fillna(0).astype(int)
    by_func = df["CSF_Function"].value_counts().sort_index()
    lines = ["# Risk Summary (auto-generated)\n",
             f"Total risks assessed: **{len(df)}**\n",
             "## Residual risk by level\n",
             "| Level | Count |", "|-------|-------|"]
    lines += [f"| {lvl} | {by_level[lvl]} |" for lvl in LEVEL_ORDER]
    lines += ["\n## Risks by NIST CSF function\n", "| Function | Count |", "|----------|-------|"]
    lines += [f"| {fn} | {ct} |" for fn, ct in by_func.items()]
    lines += ["\n## Top 5 residual risks\n", "| ID | Risk | Residual | Level |",
              "|----|------|----------|-------|"]
    for _, r in df.head(5).iterrows():
        lines.append(f"| {r.Risk_ID} | {r.Risk_Title} | {r.Residual_Score} | {r.Residual_Level} |")
    (OUT / "risk-summary.md").write_text("\n".join(lines) + "\n")


def main():
    df = score(load())
    write_scored(df)
    heatmap(df)
    write_summary(df)
    # console report
    counts = df["Residual_Level"].value_counts().reindex(LEVEL_ORDER).fillna(0).astype(int)
    print(f"Assessed {len(df)} risks.")
    print("Residual levels:", ", ".join(f"{k}={counts[k]}" for k in LEVEL_ORDER))
    print("\nTop 5 residual risks:")
    for _, r in df.head(5).iterrows():
        print(f"  {r.Risk_ID}  [{r.Residual_Level:8}] score {r.Residual_Score:2}  {r.Risk_Title}")
    print(f"\nOutputs written to {OUT}/")


if __name__ == "__main__":
    main()
