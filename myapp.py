import streamlit as st
import time
import pandas as pd
import numpy as np


st.title ("Hello My App")

df2= pd.DataFrame( 
    np.random.randn(10, 2),  
    columns=['x', 'y'])
st.line_chart(df2) 


df1= pd.DataFrame( 
    np.random.randn(500, 2) / [50 , 50] + [51.5080, - 0.1281],  
    columns=['lat', 'lon'])
st.map(df1)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("🎗️ Cancer Survival Dashboard")

# Load the data based on the selected cancer type
@st.cache_data  # @st.cache_data to upload the data 
def load_data(sheet_name):
    file_path = "cancersurvivaladultsclean2.xls"
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

# Load the metadata sheets
@st.cache_data
def load_metadata(sheet_name):
    file_path = "cancersurvivaladultsclean2.xls"
    metadata_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)  
    return metadata_df

# Sidebar: Select Cancer Type
st.sidebar.header("Filter Options")    # creating options to filter from
cancer_types = {                       # creating dictionary to hold the cancer types
    "Breast Cancer (women) E1": "E1. Breast women",
    "Cervical Cancer (women) E2": "E2. Cervix women",
    "Prostate Cancer (men) E3": "E3. Prostate men"
}
selected_cancer_type = st.sidebar.selectbox("Select Cancer Type", list(cancer_types.keys()))
sheet_name = cancer_types[selected_cancer_type]

# Load the data for the selected cancer type
df = load_data(sheet_name)

# Forward-fill the "Area Code" column to propagate values downward
df["Area Code"] = df["Area Code"].fillna(method="ffill")

# Sidebar: Select Area Code, this create Area Code sidebar
area_code = st.sidebar.selectbox("Select Area Code", df["Area Code"].unique())
filtered_df = df[df["Area Code"] == area_code]


# Display filtered data on the dashboard
st.subheader(f"Cancer Survival Data for {selected_cancer_type} in {area_code}")
st.dataframe(filtered_df)

# Visualizations
st.subheader(f"Survival Trends Over Years for {selected_cancer_type}")
selected_area = st.selectbox("Select Area", filtered_df["Area Name"].unique())
area_data = filtered_df[filtered_df["Area Name"] == selected_area]

# Define years according to the dataset
years = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]
survival_rates = area_data[years].values.flatten()

# Plot survival rates over years
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))  

# Line plot for survival trends
ax1.plot(years, survival_rates, marker="o", color="blue")
ax1.set_title(f"Survival Rates for {selected_area}")
ax1.set_xlabel("Year")
ax1.set_ylabel("Survival Rate (%)")

# Histogram for survival rate distribution
ax2.hist(survival_rates, bins=10, color="orange", edgecolor="black")
ax2.set_title(f"Distribution of Survival Rates for {selected_area}")
ax2.set_xlabel("Survival Rate (%)")
ax2.set_ylabel("Frequency")

# Adjust layout to prevent overlap
plt.tight_layout()

# Display the plots in Streamlit
st.pyplot(fig)


# Additional Metrics
st.subheader("Key Metrics")
st.write(f"Average Survival Rate: {survival_rates.mean():.2f}%")
st.write(f"Change in Survival Rate (2003-2010): {survival_rates[-1] - survival_rates[0]:.2f}%")

# Sidebar: About Information
st.sidebar.header("About Information")
about_options = ["None", "Contents", "Notes and definitions", 
                 "Quality of data", "Related publications", 
                 "Terms and conditions"]
selected_about_option = st.sidebar.selectbox("Select Option", about_options)

# Display metadata content if an option other than "None" is selected
if selected_about_option != "None":
    st.subheader(f"About Information: {selected_about_option}")
    if selected_about_option == "Contents":
        contents_df = load_metadata("Contents")
        st.write(contents_df)
    elif selected_about_option == "Notes and definitions":
        notes_df = load_metadata("Notes and definitions ")
        st.write(notes_df)
    elif selected_about_option == "Quality of data":
        quality_df = load_metadata("Quality of data")
        st.write(quality_df)
    elif selected_about_option == "Related publications":
        publications_df = load_metadata("Related publications")
        st.write(publications_df)
    elif selected_about_option == "Terms and conditions":
        terms_df = load_metadata("Terms and conditions")
        st.write(terms_df)



 

