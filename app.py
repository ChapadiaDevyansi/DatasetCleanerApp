import streamlit as st
import pandas as pd



st.set_page_config(
    page_title="Dataset Cleaner & Business Insights",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dataset Cleaner & Business Insights")
st.write("Upload a CSV file to clean, analyze data.")


uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    
    df = pd.read_csv(uploaded_file)

    
    cleaned_df = df.copy()

    st.success("✅ File uploaded successfully!")

   
    st.markdown("---")
    st.subheader("📈 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicate Rows", int(df.duplicated().sum()))

   
    st.markdown("---")
    st.subheader("📄 Dataset Preview")

    st.dataframe(df.head(10), use_container_width=True)

       
    st.markdown("---")
    st.subheader("🔍 Missing Values")

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) > 0:
        st.dataframe(missing)
    else:
        st.success("No missing values found.")

    
    st.markdown("---")
    st.subheader("📑 Duplicate Rows")

    duplicates = df.duplicated().sum()

    if duplicates > 0:
        st.warning(f"{duplicates} duplicate rows found.")
    else:
        st.success("No duplicate rows found.")

   
    st.markdown("---")
    st.subheader("📋 Column Information")

    info = pd.DataFrame({
        "Data Type": df.dtypes,
        "Missing Values": df.isnull().sum(),
        "Unique Values": df.nunique()
    })

    st.dataframe(info, use_container_width=True)

    
    st.markdown("---")
    st.subheader("📊 Statistical Summary")

    st.dataframe(df.describe(include="all"), use_container_width=True)

    
    st.markdown("---")
    st.subheader("🧹 Data Cleaning")

    if st.button("Clean Dataset"):

        cleaned_df = df.copy()

        
        cleaned_df = cleaned_df.drop_duplicates()

        
        cleaned_df = cleaned_df.dropna(how="all")

        
        cleaned_df = cleaned_df.dropna(axis=1, how="all")

        
        text_cols = cleaned_df.select_dtypes(include="object").columns

        for col in text_cols:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()

        
        for col in text_cols:
            cleaned_df[col] = cleaned_df[col].str.title()

        
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == "object":
                try:
                    cleaned_df[col] = pd.to_datetime(cleaned_df[col])
                except:
                    pass

        df = cleaned_df

        st.success("✅ Dataset cleaned successfully!")

        st.subheader("Cleaned Dataset Preview")
        st.dataframe(df, use_container_width=True)

        
        st.markdown("---")
        st.subheader("📊 Statistical Summary")

        st.dataframe(df.describe(include="all"), use_container_width=True)

        
        st.markdown("---")
        st.subheader("📈 Business Insights")

        # Total Records
        st.success(f"📋 Total Records: {len(df):,}")

        # Numeric Columns
        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:

         
            highest_col = df[numeric_cols].mean().idxmax()
            highest_value = df[highest_col].mean()

            st.success(
             f"📊 Highest Average: {highest_col} ({highest_value:.2f})"
            )

            
            lowest_col = df[numeric_cols].mean().idxmin()
            lowest_value = df[lowest_col].mean()

            st.success(
            f"📉 Lowest Average: {lowest_col} ({lowest_value:.2f})"
            )

            
            sales_columns = ["Sales", "Revenue", "Amount"]

            for col in sales_columns:
                if col in df.columns:
                    st.success(f"💰 Total {col}: ₹{df[col].sum():,.2f}")
                break

            
            if "Profit" in df.columns:
                st.success(f"📈 Total Profit: ₹{df['Profit'].sum():,.2f}")

           
            quantity_columns = ["Quantity", "Qty"]

            for col in quantity_columns:
                if col in df.columns:
                    st.success(f"📦 Total Quantity: {df[col].sum():,.0f}")
                break

           
            order_columns = [
                "Order ID",
                "OrderID",
                "InvoiceNo",
                "Invoice No"
            ]

            for col in order_columns:
                if col in df.columns:
                    st.success(f"🛒 Total Orders: {df[col].nunique():,}")
                    break

           
            customer_columns = [
                "CustomerID",
                "Customer ID",
                "Customer Name",
                "Customer"
            ]

            for col in customer_columns:
                if col in df.columns:
                    st.success(f"👥 Unique Customers: {df[col].nunique():,}")
                break

           
            product_columns = [
            "Product Name",
            "Description",
            "Product"
            ]

            for col in product_columns:
                if col in df.columns:

                    product = df[col].mode()[0]

                    st.success(f"⭐ Most Purchased Product: {product}")

                    break

            
            location_columns = [
                "Country",
                "Region",
                "State",
                "City"
            ]

            for col in location_columns:
                if col in df.columns:

                    location = df[col].mode()[0]

                    st.success(f"🌍 Top {col}: {location}")

                break

           
            if "Category" in df.columns:

                category = df["Category"].mode()[0]

                st.success(f"🏆 Most Common Category: {category}")

            
            date_columns = [
                "Order Date",
                "InvoiceDate",
                "Date"
            ]

            for col in date_columns:
                if col in df.columns:

                    try:

                        dates = pd.to_datetime(df[col])

                        st.success(
                            f"📅 Data Period: {dates.min().date()} to {dates.max().date()}"
                        )

                    except:
                        pass

                    break
                    
                    st.markdown("---")

                    csv = df.to_csv(index=False)

                    st.download_button(
                    "⬇ Download Cleaned Dataset",
                    data=csv,
                    file_name="cleaned_dataset.csv",
                    mime="text/csv"
)
