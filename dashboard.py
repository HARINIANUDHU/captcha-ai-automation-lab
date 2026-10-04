import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="OCR Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 OCR Analysis Dashboard")
st.caption("Controlled OCR experiments — local synthetic image dataset")

# Load experiment CSV files
files = []

if Path("ocr_results.csv").exists():
    baseline = pd.read_csv("ocr_results.csv")
    baseline["condition"] = "baseline"
    baseline["experiment"] = "Initial experiment"
    files.append(baseline)

if Path("ocr_condition_results.csv").exists():
    conditions = pd.read_csv("ocr_condition_results.csv")
    conditions["experiment"] = "Image condition experiment"
    files.append(conditions)

if not files:
    st.error("No experiment CSV files found. Run your OCR experiments first.")
    st.stop()

data = pd.concat(files, ignore_index=True)

# Normalize fields
data["correct"] = (
    data["correct"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({"true": True, "false": False})
)

data["processing_time_seconds"] = pd.to_numeric(
    data["processing_time_seconds"],
    errors="coerce"
)

data = data.dropna(subset=["correct", "processing_time_seconds"])

# Filters
st.sidebar.header("Filters")

experiments = ["All"] + sorted(data["experiment"].unique().tolist())
selected_experiment = st.sidebar.selectbox(
    "Experiment",
    experiments
)

if selected_experiment != "All":
    data = data[data["experiment"] == selected_experiment]

conditions = ["All"] + sorted(data["condition"].unique().tolist())
selected_condition = st.sidebar.selectbox(
    "Image condition",
    conditions
)

if selected_condition != "All":
    data = data[data["condition"] == selected_condition]

if data.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# Summary metrics
total = len(data)
correct_count = int(data["correct"].sum())
accuracy = correct_count / total * 100
average_time = data["processing_time_seconds"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total samples", total)
col2.metric("Correct readings", correct_count)
col3.metric("Exact-match accuracy", f"{accuracy:.1f}%")
col4.metric("Average OCR time", f"{average_time:.3f} s")

st.divider()

# Grouped analysis
summary = (
    data.groupby("condition")
    .agg(
        samples=("correct", "count"),
        correct=("correct", "sum"),
        average_time=("processing_time_seconds", "mean")
    )
    .reset_index()
)

summary["accuracy_percent"] = (
    summary["correct"] / summary["samples"] * 100
)

left, right = st.columns(2)

with left:
    st.subheader("Exact-match accuracy by condition")
    accuracy_chart = summary.set_index("condition")[
        "accuracy_percent"
    ]
    st.bar_chart(accuracy_chart, y_label="Accuracy (%)")

with right:
    st.subheader("Average OCR processing time")
    time_chart = summary.set_index("condition")[
        "average_time"
    ]
    st.bar_chart(time_chart, y_label="Seconds")

st.subheader("Experiment summary")
st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)
# Compare OCR accuracy across experiment runs
if "run_id" in data.columns:
    st.divider()
    st.subheader("📈 OCR Accuracy Across Runs")

    run_data = data.dropna(subset=["run_id"]).copy()

    if not run_data.empty:
        run_summary = (
            run_data.groupby(["run_id", "condition"])
            .agg(
                samples=("correct", "count"),
                correct=("correct", "sum")
            )
            .reset_index()
        )

        run_summary["accuracy_percent"] = (
            run_summary["correct"] / run_summary["samples"] * 100
        )

        run_chart = run_summary.pivot(
            index="run_id",
            columns="condition",
            values="accuracy_percent"
        )

        st.line_chart(
            run_chart,
            y_label="Exact-match accuracy (%)"
        )

        st.caption(
            "Each point represents the accuracy for one condition "
            "during one experiment run."
        )

        st.dataframe(
            run_summary,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No experiment run history found yet.")
st.subheader("Individual OCR records")

show_errors = st.checkbox("Show incorrect readings only")

records = data.copy()

if show_errors:
    records = records[records["correct"] == False]

st.dataframe(
    records[
        [
            "experiment",
            "condition",
            "expected_text",
            "recognized_text",
            "correct",
            "processing_time_seconds"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# Download filtered records
csv_data = records.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download displayed records as CSV",
    data=csv_data,
    file_name="ocr_dashboard_records.csv",
    mime="text/csv"
)
# OCR error analysis
st.divider()
st.subheader("🔎 OCR Error Analysis")

errors = data[data["correct"] == False].copy()

total_records = len(data)
total_errors = len(errors)

if total_errors == 0:
    st.success("No incorrect readings in the selected dataset.")
else:
    error_rate = (total_errors / total_records) * 100

    col1, col2 = st.columns(2)
    col1.metric("Incorrect readings", total_errors)
    col2.metric("Error rate", f"{error_rate:.1f}%")

    st.write("### Incorrect OCR readings")

    st.dataframe(
        errors[
            [
                "condition",
                "expected_text",
                "recognized_text",
                "processing_time_seconds"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # Compare characters at matching positions
    character_errors = []

    for _, row in errors.iterrows():
        expected = str(row["expected_text"])
        recognized = str(row["recognized_text"])

        for position, (expected_char, recognized_char) in enumerate(
            zip(expected, recognized),
            start=1
        ):
            if expected_char != recognized_char:
                character_errors.append({
                    "position": position,
                    "expected_character": expected_char,
                    "recognized_character": recognized_char
                })

    if character_errors:
        character_error_df = pd.DataFrame(character_errors)

        st.write("### Character-level mismatches")

        mismatch_counts = (
            character_error_df
            .groupby(
                ["expected_character", "recognized_character"]
            )
            .size()
            .reset_index(name="count")
        )

        st.dataframe(
            mismatch_counts,
            use_container_width=True,
            hide_index=True
        )