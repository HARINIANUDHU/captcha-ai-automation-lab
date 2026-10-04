import sqlite3
import pandas as pd
import streamlit as st


DB_NAME = "captcha_results.db"


def load_data():
    connection = sqlite3.connect(DB_NAME)

    query = """
        SELECT
            id,
            challenge_type,
            challenge,
            answer,
            result,
            execution_time,
            created_at
        FROM experiments
        ORDER BY id DESC
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


st.set_page_config(
    page_title="CAPTCHA OCR Analytics",
    layout="wide"
)

st.title("🔍 CAPTCHA OCR Analytics Dashboard")

df = load_data()

if df.empty:
    st.warning("No experiment data found.")
    st.stop()


# -------------------------
# Metrics
# -------------------------

total = len(df)

correct = len(
    df[df["result"].isin(["correct", "SUCCESS"])]
)

accuracy = (correct / total) * 100

average_time = df["execution_time"].mean()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Experiments",
    total
)

col2.metric(
    "Correct",
    correct
)

col3.metric(
    "Accuracy",
    f"{accuracy:.2f}%"
)

col4.metric(
    "Avg Execution Time",
    f"{average_time:.4f}s"
)


st.divider()


# -------------------------
# Challenge type analysis
# -------------------------

st.subheader("Challenge Type Analysis")

challenge_summary = (
    df.groupby("challenge_type")
    .agg(
        experiments=("id", "count"),
        average_time=("execution_time", "mean")
    )
    .reset_index()
)

st.dataframe(
    challenge_summary,
    use_container_width=True
)


# -------------------------
# OCR condition analysis
# -------------------------

ocr_df = df[
    df["challenge_type"].str.startswith("ocr_")
].copy()

if not ocr_df.empty:

    st.subheader("OCR Condition Performance")

    condition_summary = (
        ocr_df.groupby("challenge_type")
        .agg(
            tests=("id", "count"),
            correct=("result", lambda x:
                x.isin(["correct"]).sum()
            ),
            average_time=("execution_time", "mean")
        )
        .reset_index()
    )

    condition_summary["accuracy"] = (
        condition_summary["correct"]
        / condition_summary["tests"]
        * 100
    )

    st.dataframe(
        condition_summary,
        use_container_width=True
    )

    st.bar_chart(
        condition_summary.set_index("challenge_type")["accuracy"]
    )


# -------------------------
# Execution time
# -------------------------

st.subheader("Execution Time by Challenge Type")

time_chart = (
    df.groupby("challenge_type")["execution_time"]
    .mean()
)

st.bar_chart(time_chart)


# -------------------------
# Raw experiment records
# -------------------------

st.subheader("Experiment Records")

st.dataframe(
    df,
    use_container_width=True
)