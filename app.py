import streamlit as st
import pandas as pd
import re
from rapidfuzz.fuzz import ratio

st.title("🔍 Duplicate Customer Detector")

st.write(
    "Upload a customer CSV file to identify potential duplicate records "
    "using normalization, exact matching, blocking, and similarity scoring."
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

def normalize_text(value):
    if pd.isna(value):
        return ""

    value = str(value).lower()
    value = re.sub(r"[^\w\s]", "", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    required_columns = [
        "Customer ID",
        "Name",
        "Email",
        "Phone",
        "Address"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        st.error(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    else:

        st.success("CSV file is valid!")
        normalized_df = df.copy()

        text_columns = [
            "Name",
            "Email",
            "Phone",
            "Address"
        ]

        for column in text_columns:
            normalized_df[column] = normalized_df[column].apply(
                normalize_text
            )

        normalized_df["Name Block"] = normalized_df["Name"].str[0]

        blocked_matches = []
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0,
            max_value=100,
            value=80
        )


        for i in range(len(normalized_df)):
            for j in range(i + 1, len(normalized_df)):

                if normalized_df.loc[i, "Name Block"] == normalized_df.loc[j, "Name Block"]:

                    name_score = ratio(
                        normalized_df.loc[i, "Name"],
                        normalized_df.loc[j, "Name"]
                    )

                    blocked_matches.append({
                        "Customer 1": normalized_df.loc[i, "Customer ID"],
                        "Customer 2": normalized_df.loc[j, "Customer ID"],
                        "Name Similarity": name_score,
                        "Match Result": "Potential Duplicate"
                            if name_score >= similarity_threshold
                            else "Not Duplicate",
                        "Review": "Pending"
                    })

        similarity_df = pd.DataFrame(blocked_matches)

        st.subheader("Similarity Scores")

        st.dataframe(similarity_df)

        potential_duplicates = similarity_df[
            similarity_df["Match Result"] == "Potential Duplicate"
        ]



        st.subheader("Potential Duplicates")

        for index in potential_duplicates.index:

            review_decision = st.selectbox(
                f"Review {potential_duplicates.loc[index, 'Customer 1']} vs {potential_duplicates.loc[index, 'Customer 2']}",
                ["Pending", "Duplicate", "Not Duplicate"],
                key=f"review_{index}"
            )

            potential_duplicates.loc[index, "Review"] = review_decision

        st.dataframe(potential_duplicates)
        csv_data = potential_duplicates.to_csv(index=False)

        st.download_button(
            label="Download Reviewed Results",
            data=csv_data,
            file_name="reviewed_duplicates.csv",
            mime="text/csv"
        )
 

        st.subheader("Customer Data")

        st.dataframe(df)
        st.subheader("Normalized Data")

        st.dataframe(normalized_df)

        match_columns = [
            "Name",
            "Email",
            "Phone",
            "Address"
        ]

        exact_matches = []

        for i in range(len(normalized_df)):
            for j in range(i + 1, len(normalized_df)):

                if all(
                    normalized_df.loc[i, column]
                    == normalized_df.loc[j, column]
                    for column in match_columns
                ):

                    exact_matches.append({
                        "Customer 1": normalized_df.loc[i, "Customer ID"],
                        "Customer 2": normalized_df.loc[j, "Customer ID"],
                        "Name": normalized_df.loc[i, "Name"],
                        "Match Type": "Exact Match"
                    })

        st.subheader("Exact Matches")

        if exact_matches:

            exact_matches_df = pd.DataFrame(exact_matches)

            st.dataframe(exact_matches_df)

        else:

            st.info("No exact matches found.")


        st.subheader("Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Customers", len(df))
        col2.metric("Exact Matches", len(exact_matches))
        col3.metric("Potential Duplicates", len(potential_duplicates))