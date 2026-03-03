import os
import pandas as pd
import matplotlib.pyplot as plt

IN_PATH = os.path.join("data_processed", "processed_listings.csv")
SUMMARY_PATH = os.path.join("data_processed", "summary.txt")
CORR_PATH = os.path.join("data_processed", "correlations.txt")
VIS_DIR = "visuals"

# Selected features (rubric-aligned)
QUANT_FEATURES = ["price", "accommodates", "bedrooms", "number_of_reviews"]
QUAL_FEATURES = ["room_type"]


def _write_summary(df: pd.DataFrame) -> None:
    """
    Writes summary statistics to data_processed/summary.txt
    - Quantitative: min, max, median
    - Qualitative: number of categories, most frequent, least frequent
    """
    lines = []
    lines.append("SUMMARY STATISTICS\n")
    lines.append("Quantitative features: min / max / median\n")

    for col in QUANT_FEATURES:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        lines.append(f"\n[{col}]\n")
        lines.append(f"min: {s.min()}\n")
        lines.append(f"max: {s.max()}\n")
        lines.append(f"median: {s.median()}\n")

    lines.append("\n\nQualitative features: categories / most frequent / least frequent\n")
    for col in QUAL_FEATURES:
        s = df[col].astype("string").dropna()
        vc = s.value_counts(dropna=False)
        num_categories = vc.shape[0]
        max_count = vc.max()
        min_count = vc.min()

        most_freq = vc[vc == max_count].index.tolist()
        least_freq = vc[vc == min_count].index.tolist()

        lines.append(f"\n[{col}]\n")
        lines.append(f"number_of_categories: {num_categories}\n")
        lines.append(f"most_frequent (count={max_count}): {most_freq}\n")
        lines.append(f"least_frequent (count={min_count}): {least_freq}\n")

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)


def _write_correlations(df: pd.DataFrame) -> None:
    corr_df = df[QUANT_FEATURES].corr(method="pearson")

    # Save a readable text format
    with open(CORR_PATH, "w", encoding="utf-8") as f:
        f.write("PAIRWISE CORRELATIONS (Pearson)\n")
        f.write(f"Features: {QUANT_FEATURES}\n\n")
        f.write(corr_df.to_string())
        f.write("\n")


def _scatter_plot(df: pd.DataFrame, x: str, y: str, out_path: str) -> None:
    plt.figure()
    plt.scatter(df[x], df[y])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"{y} vs {x}")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def _bar_chart_counts(df: pd.DataFrame, col: str, out_path: str) -> None:
    counts = df[col].astype("string").value_counts().sort_values(ascending=False)

    plt.figure()
    plt.bar(counts.index.astype(str), counts.values)
    plt.xlabel(col)
    plt.ylabel("count")
    plt.title(f"Distribution of {col}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def _make_plots(df: pd.DataFrame) -> None:
    os.makedirs(VIS_DIR, exist_ok=True)

    # Scatter plots for all pairs of quantitative features
    for i in range(len(QUANT_FEATURES)):
        for j in range(i + 1, len(QUANT_FEATURES)):
            a = QUANT_FEATURES[i]
            b = QUANT_FEATURES[j]
            out = os.path.join(VIS_DIR, f"scatter_{a}_vs_{b}.png")
            sub = df[[a, b]].dropna()
            _scatter_plot(sub, a, b, out)

    # Qualitative distribution plots
    for col in QUAL_FEATURES:
        out = os.path.join(VIS_DIR, f"hist_{col}.png")
        _bar_chart_counts(df, col, out)


def run_visualization() -> dict:
    if not os.path.exists(IN_PATH):
        raise FileNotFoundError(
            f"Processed data not found at {IN_PATH}. Run wf_dataprocessing.py first."
        )

    os.makedirs("data_processed", exist_ok=True)

    df = pd.read_csv(IN_PATH)

    # Write summary + correlations
    _write_summary(df)
    _write_correlations(df)

    # Create plots
    _make_plots(df)

    return {
        "summary": SUMMARY_PATH,
        "correlations": CORR_PATH,
        "visuals_dir": VIS_DIR,
    }


if __name__ == "__main__":
    artifacts = run_visualization()
    print("Visualization complete.")
    for k, v in artifacts.items():
        print(f"{k}: {v}")