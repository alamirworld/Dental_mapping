import streamlit as st
import pandas as pd

# Streamlit settings for English text support
st.set_page_config(page_title="Dental Mapping", layout="centered")

# Add CSS for proper text alignment, enable text selection, make the table larger, add fixed bottom-left text, and customize background and text colors
st.markdown(
    """
    <style>
    body, input, select, textarea, .stTextInput > div > div > input {
        font-family: 'Arial', sans-serif;
        direction: ltr;
        text-align: left;
        background-color: #E0F7FA; /* White mixed with light cyan background */
    }
    table {
        direction: ltr;
        text-align: left;
        width: 100%;
        border-collapse: collapse;
        user-select: text; /* Enable text selection */
        -webkit-user-select: text;
        -moz-user-select: text;
        -ms-user-select: text;
    }
    th, td {
        font-family: 'Arial', sans-serif;
        font-size: 18px; /* Increase font size for larger text */
        padding: 12px; /* Increase padding for larger cells */
        border: 1px SOLID #ddd;
        line-height: 1.5; /* Increase line height for better readability */
    }
    th {
        background-color: #f2f2f2;
    }
    /* Style for the fixed bottom-left text */
    .fixed-bottom-left {
        position: fixed;
        bottom: 10px;
        left: 10px;
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        color: #FF0000; /* Change text color to red */
        z-index: 1000; /* Ensure it stays on top of other elements */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Application title
st.title("Dental Mapping")

# Load Excel file
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Dental Final UL V1.xlsx")
        return df
    except FileNotFoundError:
        st.error("Error: File 'Dental Final UL V1.xlsx' not found in the directory. Ensure the file exists.")
        return None
    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")
        return None

# Load the data
df = load_data()

# Add the fixed bottom-left text
st.markdown(
    '<div class="fixed-bottom-left">Designed by: Mostafa El-beshbeshy</div>',
    unsafe_allow_html=True
)

if df is not None:
    # Search input box (placeholder removed)
    search_query = st.text_input("Search in data:")

    # Search the data
    if search_query:
        # Search across all columns (convert values to strings to avoid comparison errors)
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)
        filtered_df = df[mask]

        if not filtered_df.empty:
            st.write(f"Found {len(filtered_df)} result(s):")
            # Revert to st.dataframe for interactive table
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("No matching results found.")
    else:
        st.info("Enter a word or value to search in the data.")
else:
    st.info("Please ensure the Excel file is present and loaded correctly.")