import pandas as pd


def run_variance_from_file(uploaded_file):

    # Read file as raw text
    df_raw = pd.read_csv(uploaded_file, header=None)

    # Split columns
    df = df_raw[0].str.split(",", expand=True)

    # Drop header
    df = df.iloc[1:]

    # Assign names
    df.columns = ["Month", "Entity", "Account", "Type", "Amount"]

    # Convert Amount
    df["Amount"] = pd.to_numeric(df["Amount"])

    # Split
    actual = df[df["Type"] == "Actual"]
    budget = df[df["Type"] == "Budget"]

    # Merge
    merged = actual.merge(
        budget,
        on=["Month", "Entity", "Account"],
        suffixes=("_Actual", "_Budget")
    )

    # Variance
    merged["Variance"] = merged["Amount_Actual"] - merged["Amount_Budget"]

    ranked = merged.sort_values("Variance")

    return ranked
