import pandas as pd

def process_csv(input_csv_path, output_excel_path):
    try:
        # Read CSV safely
        df = pd.read_csv(input_csv_path)

        # Safety check: minimum columns
        if df.shape[1] < 5:
            raise ValueError("CSV does not have required number of columns")

        # Extract by column POSITION (Google Forms stable order)
        df = df.iloc[:, [3, 4]]
        df.columns = ["roll_number", "coursera_link"]

        # Clean data
        df["roll_number"] = df["roll_number"].astype(str).str.strip()
        df["coursera_link"] = df["coursera_link"].astype(str).str.strip()

        # Remove empty / invalid Coursera links
        df = df[df["coursera_link"] != ""]
        df = df[df["coursera_link"].str.lower() != "nan"]

        # ---- total submissions ----
        total_submissions = (
            df.groupby("roll_number")
            .size()
            .reset_index(name="total_submissions")
        )

        # ---- unique submissions ----
        unique_df = df.drop_duplicates(
            subset=["roll_number", "coursera_link"]
        )

        unique_submissions = (
            unique_df.groupby("roll_number")
            .size()
            .reset_index(name="unique_submissions")
        )

        # ---- merge ----
        summary = pd.merge(
            total_submissions,
            unique_submissions,
            on="roll_number",
            how="left"
        )

        # ---- duplicate logic ----
        summary["duplicate_count"] = (
            summary["total_submissions"] - summary["unique_submissions"]
        )

        summary["flag"] = (summary["duplicate_count"] > 0).astype(int)

        # ---- final output ----
        final_df = summary[
            [
                "roll_number",
                "total_submissions",
                "unique_submissions",
                "flag",
                "duplicate_count"
            ]
        ]

        # Save Excel
        final_df.to_excel(output_excel_path, index=False)

    except Exception as e:
        print("❌ ERROR while processing CSV:", str(e))
        raise
