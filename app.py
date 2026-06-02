import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------
# Page Config
# --------------------------------

st.set_page_config(
    page_title="Universal CSV Cleaner",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# Load CSS
# --------------------------------

with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# --------------------------------
# Title
# --------------------------------

st.title("📊 Universal CSV Cleaner Tool")

st.write("Clean, analyze, and visualize any CSV dataset.")

# --------------------------------
# Sidebar Navigation
# --------------------------------

st.sidebar.title("📁 Navigation")

menu = st.sidebar.radio(
    "Go To",
    [
        "Dataset Info",
        "Data Preview",
        "Missing Values",
        "Duplicates",
        "Column Profile",
        "Health Score",
        "Statistics",
        "Visualizations",
        "Outlier Analysis",
        "Download"
    ]
)

# --------------------------------
# File Upload
# --------------------------------

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# --------------------------------
# Read Dataset
# --------------------------------

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    # --------------------------------
    # Automatic Datatype Correction
    # --------------------------------

    for col in df.columns:

        try:
            df[col] = pd.to_numeric(df[col])

        except:
            pass

    # --------------------------------
    # Clean Missing Values
    # --------------------------------

    num_cols = df.select_dtypes(include=np.number).columns

    for col in num_cols:
        df[col] = df[col].fillna(df[col].mean())

    cat_cols = df.select_dtypes(include='object').columns

    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # --------------------------------
    # Dataset Info
    # --------------------------------

    if menu == "Dataset Info":

        st.subheader("📂 Dataset Information")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                <div class='metric-card'>
                    <h3>Total Rows</h3>
                    <h2>{df.shape[0]}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class='metric-card'>
                    <h3>Total Columns</h3>
                    <h2>{df.shape[1]}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.subheader("🔍 Data Types")

        st.write(df.dtypes)

    # --------------------------------
    # Data Preview
    # --------------------------------

    elif menu == "Data Preview":

        st.subheader("📌 Dataset Preview")

        selected_columns = st.multiselect(
            "Select Columns",
            df.columns,
            default=df.columns
        )

        filtered_df = df[selected_columns]

        st.dataframe(filtered_df.head(20))

        # Search / Filter

        st.subheader("🔍 Search Data")

        search_column = st.selectbox(
            "Select Column to Search",
            filtered_df.columns
        )

        search_value = st.text_input(
            "Enter value to search"
        )

        if search_value:

            result = filtered_df[
                filtered_df[search_column]
                .astype(str)
                .str.contains(search_value, case=False)
            ]

            st.write(result)

    # --------------------------------
    # Missing Values
    # --------------------------------

    elif menu == "Missing Values":

        st.subheader("❌ Missing Values Analysis")

        missing_values = df.isnull().sum()

        missing_percentage = (
            df.isnull().sum() / len(df)
        ) * 100

        missing_df = pd.DataFrame({
            "Missing Values": missing_values,
            "Missing Percentage (%)": missing_percentage
        })

        missing_df = missing_df[
            missing_df["Missing Values"] > 0
        ]

        if not missing_df.empty:

            st.dataframe(
                missing_df.sort_values(
                    by="Missing Percentage (%)",
                    ascending=False
                )
            )

        else:
            st.success("No missing values found!")

    # --------------------------------
    # Duplicates
    # --------------------------------

        # --------------------------------
    # Duplicates
    # --------------------------------

    elif menu == "Duplicates":

        st.subheader("🔁 Duplicate Rows")

        duplicates = df.duplicated().sum()

        st.write(f"Duplicate Rows: {duplicates}")

        if st.button("Remove Duplicates"):

            df = df.drop_duplicates()

            st.success("Duplicates removed successfully!")

            st.write("Updated Shape:", df.shape)

    # --------------------------------
    # Health Score
    # --------------------------------

    elif menu == "Health Score":

        st.subheader("🏥 Dataset Health Score")

        missing_percent = (
            df.isnull().sum().sum()
            /
            (df.shape[0] * df.shape[1])
        ) * 100

        duplicate_percent = (
            df.duplicated().sum()
            /
            len(df)
        ) * 100

        score = 100

        score -= missing_percent
        score -= duplicate_percent

        score = round(max(score, 0))

        st.metric(
            "Dataset Health Score",
            f"{score}/100"
        )

        if score >= 90:
            st.success("Excellent Dataset")

        elif score >= 70:
            st.warning("Good Dataset")

        else:
            st.error("Dataset Needs Cleaning")

    # --------------------------------
    # Column Profile
    # --------------------------------

    elif menu == "Column Profile":

        st.subheader("📋 Column Profile")

        selected_col = st.selectbox(
            "Select Column",
            df.columns
        )

        st.write(
            "Datatype:",
            df[selected_col].dtype
        )

        st.write(
            "Missing Values:",
            df[selected_col].isnull().sum()
        )

        st.write(
            "Unique Values:",
            df[selected_col].nunique()
        )

        if pd.api.types.is_numeric_dtype(
            df[selected_col]
        ):

            st.write(
                "Mean:",
                round(df[selected_col].mean(), 2)
            )

            st.write(
                "Median:",
                df[selected_col].median()
            )

            st.write(
                "Minimum:",
                df[selected_col].min()
            )

            st.write(
                "Maximum:",
                df[selected_col].max()
            )

    # --------------------------------
    # Statistics
    # --------------------------------

    elif menu == "Statistics":

        st.subheader("📈 Summary Statistics")

        st.dataframe(df.describe())

        st.subheader("🔥 Correlation Matrix")

        numeric_df = df.select_dtypes(include=np.number)

        if not numeric_df.empty:

            corr = numeric_df.corr()

            fig, ax = plt.subplots(figsize=(10, 6))

            sns.heatmap(
                corr,
                annot=True,
                cmap="coolwarm",
                ax=ax
            )

            st.pyplot(fig)

        else:

            st.warning("No numeric columns found.")
    # --------------------------------
    # Visualizations
    # --------------------------------
    # --------------------------------
    # Visualizations
    # --------------------------------

    elif menu == "Visualizations":

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns

        # -----------------------------
        # Histogram
        # -----------------------------

        st.subheader("📊 Histogram")

        if len(numeric_columns) > 0:

            hist_column = st.selectbox(
                "Select Column for Histogram",
                numeric_columns
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.hist(
                df[hist_column].dropna(),
                bins=20
            )

            ax.set_title(
                f"Histogram of {hist_column}"
            )

            ax.set_xlabel(hist_column)

            ax.set_ylabel("Frequency")

            st.pyplot(fig)

        else:

            st.warning(
                "No numeric columns available."
            )

        # -----------------------------
        # Boxplot
        # -----------------------------

        st.subheader("📦 Boxplot (Outlier Detection)")

        if len(numeric_columns) > 0:

            box_column = st.selectbox(
                "Select Column for Boxplot",
                numeric_columns,
                key="boxplot"
            )

            fig2, ax2 = plt.subplots(figsize=(8, 5))

            sns.boxplot(
                x=df[box_column],
                ax=ax2
            )

            ax2.set_title(
                f"Boxplot of {box_column}"
            )

            st.pyplot(fig2)

        # -----------------------------
        # Pie Chart
        # -----------------------------

        st.subheader("🥧 Pie Chart")

        cat_cols = df.select_dtypes(
            include="object"
        ).columns

        if len(cat_cols) > 0:

            pie_col = st.selectbox(
                "Select Category Column",
                cat_cols
            )

            fig3, ax3 = plt.subplots()

            df[pie_col].value_counts().head(10).plot(
                kind="pie",
                autopct="%1.1f%%",
                ax=ax3
            )

            st.pyplot(fig3)

        else:

            st.warning(
                "No categorical columns found."
            )

        # -----------------------------
        # Scatter Plot
        # -----------------------------

        st.subheader("📍 Scatter Plot")

        if len(numeric_columns) >= 2:

            x_col = st.selectbox(
                "X Axis",
                numeric_columns,
                key="scatter_x"
            )

            y_col = st.selectbox(
                "Y Axis",
                numeric_columns,
                key="scatter_y"
            )

            fig4, ax4 = plt.subplots()

            sns.scatterplot(
                data=df,
                x=x_col,
                y=y_col,
                ax=ax4
            )

            st.pyplot(fig4)

        # -----------------------------
        # Automatic Chart Generator
        # -----------------------------

        st.subheader("🤖 Automatic Chart Generator")

        auto_col = st.selectbox(
            "Choose Any Column",
            df.columns
        )

        if pd.api.types.is_numeric_dtype(
            df[auto_col]
        ):

            fig5, ax5 = plt.subplots()

            sns.histplot(
                df[auto_col],
                kde=True,
                ax=ax5
            )

            st.pyplot(fig5)

        else:

            fig6, ax6 = plt.subplots()

            df[auto_col].value_counts().head(10).plot(
                kind="bar",
                ax=ax6
            )

            ax6.set_title(
                f"{auto_col} Distribution"
            )

            st.pyplot(fig6)

    # --------------------------------
    # Download
    # --------------------------------

    elif menu == "Download":

        st.subheader("⬇ Download Cleaned Dataset")

        csv = df.to_csv(
            index=False
        ).encode('utf-8')

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

# --------------------------------
# No File Uploaded
# --------------------------------

else:

    st.info(
        "Please upload a CSV file from the sidebar."
    )