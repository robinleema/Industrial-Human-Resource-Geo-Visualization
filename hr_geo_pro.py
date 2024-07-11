
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


#Final csv file:
New_hr=pd.read_csv(r"C:/Users/USER/Desktop/Robin vs/guvi_projects/Final_HR.csv")

#Streamlit Part:
st.set_page_config(layout="wide",
                   initial_sidebar_state="expanded")
st.header(':rainbow[Industrial Human Resource]')
st.write("***HR Data Analysis***")

opt=st.radio(label="",options=["Home", "Analysis"],
             index=0,
             format_func=lambda x:x.title(),
             horizontal=True,
             key="Menu")

if opt == "Home":
    st.write(" ")
    st.write(" ")     
    st.markdown("#### :Green[*OVERVIEW* ]")
    st.markdown("##### This project aims to analyze  industrial human resources & perform data cleaning and preparation, develop interactive geospatial visualizations")
    st.markdown("#### :Green[*DOMAIN* ] ")
    st.markdown(" ##### Resource Management ")
    st.markdown("""
                #### :Green[*TECHNOLOGIES USED*]    
        
                ##### EDA, Visualization, NLP


                """)
 

elif opt == "Analysis":
    
    unique_states = sorted(New_hr['State'].unique())
    selected_state = st.selectbox("Select State", unique_states, key="state_selector_unique")

    filtered_districts = sorted(New_hr[New_hr['State'] == selected_state]['District'].unique())
    selected_district = st.selectbox("Select District", filtered_districts, key="district_selector_unique")

    state_data = New_hr[(New_hr['State'] == selected_state)]
    district_data = New_hr[(New_hr['District'] == selected_district)]

    state_data = New_hr[(New_hr['State'] == selected_state)]
    district_data = New_hr[(New_hr['District'] == selected_district)]

    st.write(f"Showing data for {selected_state} - {selected_district}")

    total_state_workers = state_data['MainWorkersTotalPersons'].sum()
    total_district_workers = district_data['MainWorkersTotalPersons'].sum()

    st.write(f"Total number of state workers: {total_state_workers}")
    st.write(f"Total number of district workers: {total_district_workers}")

    st.subheader("DATA FRAME")
    st.write(New_hr.describe())

    names = New_hr[New_hr['District'] == selected_district]['NICName'].unique()
    names = [nic.replace('[', '').replace(']', '').replace("'", "") for nic in names]
    names = [nic.capitalize() for nic in names]
    names = sorted(names)

    #selected_name = st.selectbox("Select NIC Name", names, key="nic_name_selector")

    # Plot for Rural, Main, and Urban workers:
    rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
    urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']

    rural_data = New_hr[rural_cols].sum().values
    main_data = New_hr[['MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales']].iloc[0].values
    urban_data = New_hr[urban_cols].sum().values

    fig, ax = plt.subplots(figsize=(6,2.5))
    x_labels = ['Rural', 'Main', 'Urban']
    ax.bar(x_labels, rural_data, color='#ff9999', label='Rural')
    ax.bar(x_labels, main_data, bottom=rural_data, color='#66b3ff', label='Main')
    ax.bar(x_labels, urban_data, bottom=rural_data + main_data, color='#99ff99', label='Urban')
    ax.set_title(f"{selected_state} - {selected_district} - Workers Distribution")
    ax.legend()
    st.pyplot(fig)

    # Plot for Marginal workers:
    marginal_cols_rural = ['MarginalWorkersRuralPersons', 'MarginalWorkersRuralMales', 'MarginalWorkersRuralFemales']
    marginal_cols_urban = ['MarginalWorkersUrbanPersons', 'MarginalWorkersUrbanMales', 'MarginalWorkersUrbanFemales']

    marginal_data_rural = New_hr[marginal_cols_rural].sum().values
    marginal_data_urban = New_hr[marginal_cols_urban].sum().values

    fig, ax = plt.subplots(figsize=(10,8))
    ax.pie(marginal_data_rural, labels=marginal_cols_rural, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.set_title(f"{selected_state} - {selected_district} - Rural Marginal Workers Distribution")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10,8))
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)
    ax.pie(marginal_data_urban, labels=marginal_cols_urban, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.set_title(f"{selected_state} - {selected_district} - Urban Marginal Workers Distribution")
    st.pyplot(fig)

    # Filter data for Main, Rural, and Urban workers
    main_cols = ['MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales']
    rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
    urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']

    main_data = New_hr[['State'] + main_cols].groupby('State').sum().reset_index()
    rural_data = New_hr[['State'] + rural_cols].groupby('State').sum().reset_index()
    urban_data = New_hr[['State'] + urban_cols].groupby('State').sum().reset_index()

    # Melt the data to have a single column for worker type and another for the count
    main_data_melted = main_data.melt(id_vars='State', var_name='WorkerType', value_name='Count')

    # Plot the differences in counts
    fig = px.bar(main_data_melted, x='State', y='Count', color='WorkerType', 
                title='Differences in Main, Rural, and Urban Workers Counts (State-wise)',
                labels={'Count': 'Total Workers Count'},
                color_discrete_sequence=['#c2c2f0','#ffb3e6','#c2f0c2'],
                template='plotly_white')

    # Update the layout for better visualization
    fig.update_layout(barmode='group', xaxis_title='State', yaxis_title='Total Workers Count (Log Scale)',
                    showlegend=True, yaxis_type="log")

    # Display the chart
    st.plotly_chart(fig)

# Geo-Map Visualization

    New_hr=pd.read_csv(r"C:/Users/USER/Desktop/Robin vs/guvi_projects/Final_HR.csv")
    fig1 = px.scatter_geo(New_hr, lat="latitude", lon="longitude", color="MainWorkersTotalPersons",
                        hover_name="NICName", size="MainWorkersTotalPersons",
                        projection="natural earth", title="Geographical Distribution of Industries")

    fig2 = px.scatter(New_hr, x="MainWorkersTotalPersons", y="Male_Female_Ratio",
                    color="MainWorkersTotalPersons", hover_name="NICName",
                    title="2D Embedding of Industries based on NIC Name")
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

