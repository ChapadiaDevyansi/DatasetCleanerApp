import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Dataset Cleaner & Business Insights",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dataset Cleaner & Business Insights")

st.write("Upload your CSV file")


uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head())

    # Info
    st.subheader("📊 Dataset Info")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])
        st.metric("Columns", df.shape[1])

    with col2:
        st.metric("Missing Values", df.isnull().sum().sum())
        st.metric("Duplicate Rows", df.duplicated().sum())

   
    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = None

   
    st.subheader(" Clean Dataset")

    if st.button("Clean Dataset"):

        cleaned_df = df.copy()
        cleaned_df = cleaned_df.drop_duplicates()
        cleaned_df = cleaned_df.dropna()

        st.session_state.cleaned_df = cleaned_df

        st.success("Dataset cleaned successfully!")

   
    if st.session_state.cleaned_df is not None:

        cleaned_df = st.session_state.cleaned_df

        st.subheader("📊 Final Business Insight")

        insights = []

      
        insights.append(
            f"The dataset contains {len(cleaned_df)} records and {cleaned_df.shape[1]} columns."
        )

        cols = [c.lower() for c in cleaned_df.columns]

        is_sales = any(x in cols for x in ["sales", "revenue", "price", "quantity", "amount"])
        is_hr = any(x in cols for x in ["salary", "department", "experience", "designation"])
        is_time = any("date" in c for c in cols)

       
        if is_sales:

            if "quantity" in cols and "price" in cols:
                cleaned_df["Revenue"] = cleaned_df["Quantity"] * cleaned_df["Price"]
                insights.append("Revenue is driven by quantity and price.")

            product_col = next((c for c in cleaned_df.columns if "product" in c.lower() or "description" in c.lower()), None)

            if product_col:
                top_product = cleaned_df[product_col].value_counts().idxmax()
                insights.append(f"Top product is '{top_product}' showing high demand.")

      
        if is_hr:

            if "department" in cleaned_df.columns:
                top_dept = cleaned_df["department"].value_counts().idxmax()
                insights.append(f"{top_dept} department has highest employees.")

    
        if is_time:
            insights.append("Data shows time-based variation and trends.")

       
        cat_cols = cleaned_df.select_dtypes(include="object").columns

        if len(cat_cols) > 0:
            col = cat_cols[0]
            top_value = cleaned_df[col].value_counts().idxmax()
            percent = (cleaned_df[col].value_counts().max() / len(cleaned_df)) * 100

            insights.append(f"{top_value} dominates dataset (~{percent:.1f}%).")

       
        insights.append(
            "Overall, dataset shows clear patterns useful for decision making."
        )

        
        st.write("Key Business Insights")

        for i, point in enumerate(insights, 1):
            st.write(f"{i}. {point}")

        
        csv = cleaned_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download Cleaned CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )