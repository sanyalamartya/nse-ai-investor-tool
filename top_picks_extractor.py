import pandas as pd

def get_top_picks(csv_file="batch_results.csv", top_n=5):
    try:
        df = pd.read_csv(csv_file)

        # Drop rows with errors or missing recommendations
        df_clean = df[(df["Recommendation"] != "") & (df["Error"] == "")]

        top_short = df_clean[df_clean["Recommendation"] == "Short Term"].head(top_n)
        top_mid = df_clean[df_clean["Recommendation"] == "Mid Term"].head(top_n)
        top_long = df_clean[df_clean["Recommendation"] == "Long Term"].head(top_n)

        # Combine into one DataFrame with a new column indicating category
        top_short["Category"] = "Short Term"
        top_mid["Category"] = "Mid Term"
        top_long["Category"] = "Long Term"

        combined = pd.concat([top_short, top_mid, top_long])

        # Save to new CSV
        combined.to_csv("top_5_recommendations.csv", index=False)
        print("✅ Top 5 picks per category saved to: top_5_recommendations.csv")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    get_top_picks()
