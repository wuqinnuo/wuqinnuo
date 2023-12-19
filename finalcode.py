import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
from st_pages import Page, show_pages, add_page_title

#Read the file from excel
data = pd.read_csv('data.csv')


#page 1 Where are the most crime-prone areas in Boston?
# Function to get longtitude and lantitude for map
def lat_long(data):
    location = data[['Lat', 'Long']]
    return location


# Function to create crime map
def create_crime_map():
    location=lat_long(data)
    st.markdown("# Boston Crime Map")
    st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9",initial_view_state={"latitude": 42.30, "longitude": -71.10, "zoom": 11, "pitch": 50},
                    layers=[pdk.Layer("HexagonLayer",data=location,get_position="[Long, Lat]",radius=200,elevation_scale=4,elevation_range=[0, 1000],pickable=True,extruded=True),
                    pdk.Layer("ScatterplotLayer",data=location,get_position="[Long, Lat]",get_color="[200, 30, 0, 160]",get_radius=200,),],))
#page 2
# Function to display crime statistics by district
def display_crime_statistics():
    st.title(''':blue[Crime Statistics by District]''')
    dist_name = {'A1': 'Downtown',
        'A15': 'Charlestown',
        'A7': 'East Boston',
        'B2': 'Roxbury',
        'B3': 'Mattapan',
        'C6': 'South Boston',
        'C11': 'Dorchester',
        'D4': 'South End',
        'D14': 'Brighton',
        'E5': 'West Roxbury',
        'E13': 'Jamaica Plain',
        'E18': 'Hyde Park'}

    st.write("The list of district names corresponding region name")
    for i in dist_name:
        st.write(i, dist_name[i])
    st.subheader("Please choose specific district you want to discover:")
    # Create a select box to select the district
    selected_district_code = st.selectbox('Select a district:', data['DISTRICT'].unique())
    selected_district = dist_name[selected_district_code]

    st.write("You choose", selected_district)

    # Filter the data for the selected district
    st.write("The following table is all offense description in", selected_district)
    selected_district_data = data[data['DISTRICT'] == selected_district_code][["DISTRICT", "OFFENSE_DESCRIPTION"]]
    st.write(selected_district_data)

    # Group by crime category and count occurrences
    crime_type=selected_district_data['OFFENSE_DESCRIPTION'].unique()
    crime_counts =selected_district_data['OFFENSE_DESCRIPTION'].value_counts()

    st.write("Here is bar chart covering all type of offense in",selected_district)
    fig, ax = plt.subplots()
    ax.bar(crime_counts.index, crime_counts.values)
    ax.set_xticklabels(crime_counts.index, rotation=90,size=5)
    ax.set_xlabel('Crime Category')
    ax.set_ylabel('Count')
    ax.set_title(f'Crime Statistics in {selected_district}')
    st.pyplot(fig)
    #select specific crime  you want to see
    st.subheader("Please choose specific offense you want to see:")
    selected_offenses = st.multiselect('Select Offense Descriptions (you can select multiple):', crime_type)

    # Filter data for the selected offense descriptions
    selected_offense_data = selected_district_data[selected_district_data['OFFENSE_DESCRIPTION'].isin(selected_offenses)]

    # Group by crime category and count occurrences for selected offenses
    selected_counts = selected_offense_data['OFFENSE_DESCRIPTION'].value_counts()

    # Visualization - Bar chart for selected offense descriptions
    st.bar_chart(selected_counts)



#Page 3: which day in week have the highest crime rate in boston
# Title and Subheader



#page 4: see the crime within certain dates
# Title and Subheader
def createslider():
    st.title("Crime happened within range of chosen months")
    st.subheader("Select your time range")

    # Double-ended slider for selecting start and end time
    month_range = st.slider("Duble ended slider", 1, 12,(1,12))
    month_dict = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'}

    st.write("You select to see the crime between",month_dict[month_range[0]],"and",month_dict[month_range[1]])




# Sidebar navigation
page_names= {"Boston Crime Map": create_crime_map,"Crime in Specific District": display_crime_statistics,"Highest Crime day": createslider}


# Select the page using the sidebar

code = st.sidebar.selectbox("Choose a page", page_names.keys())
page_names[code]()