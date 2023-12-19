"""
Name:       Qinnuo Wu
CS230:      Section 5
Data:       Boston Crime 2023
URL:

Description:
This program illustrates a report on crime incidents that occurred in Boston.
The provided data offers various options for exploration.
On the first page, the program displays the number of crimes that happened in different areas.
The second page primarily focuses on the time when the crimes occurred.
Users have the flexibility to select the specific time range they want to investigate.

"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns
import base64


def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
side_bg = r"C:\python\background.jpg"
sidebar_bg(side_bg)

#Read the file from excel
data = pd.read_csv('data.csv')


def convert_df(df):

    return df.to_csv().encode('utf-8')
csv = convert_df(data)

st.download_button(
    label="Click here to download the crime data",
    data=csv,
    file_name='Crime data 2023',
    mime='text/csv',
)

# Function to get longtitude and lantitude for map
def lat_long(data):
    lat, long = data['Lat'], data['Long']
    return lat, long

# Function to create crime map
def create_crime_map(data):
    lat, long = lat_long(data)
    st.markdown("# :red[Boston Crime Map]")

    tooltip = {"html": "<b>Latitude:</b> {Lat}<br/><b>Longitude:</b> {Long}<br/>"}

    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position="[Long, Lat]",
        get_color="[200, 30, 0, 160]",
        get_radius=200,
        pickable=True,
        auto_highlight=True,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/satellite-streets-v12",
            initial_view_state={"latitude": 42.30, "longitude": -71.10, "zoom": 11, "pitch": 50},
            layers=[scatterplot_layer],
            tooltip=tooltip,
        )
    )

# Call the function with the sample data
create_crime_map(data)


data=data.drop(columns='UCR_PART')
data=data.drop(columns='OFFENSE_CODE_GROUP')
def highest_crime_district():

    # Mapping district codes to district names
    dict_name = {
        'A1': 'Downtown',
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
        'E18': 'Hyde Park',
    }

    crime_district = data['DISTRICT'].value_counts()
    df = pd.DataFrame(list(dict_name.items()), columns=['District', 'District Name'])
    st.write("The list of district names corresponding region name")
    st.write(df)
    print(crime_district)


    max_crime_district = crime_district.idxmax()
    max_crime_district_name = dict_name[max_crime_district]
    total_crimes = data['DISTRICT'].count()

    crime_rates = (crime_district / total_crimes) * 100
    st.write(max_crime_district_name, "has the highest crime rate")

    st.write("Number of crimes for each district:")
    crime_table = pd.DataFrame({'District': crime_district.keys(), 'Number of Crimes': crime_district.values})
    st.table(crime_table)


def display_crime_statistics():
    highest_crime_district()
    st.title(''':blue[Crime Statistics by District]''')
    dict_name = {'A1': 'Downtown',
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



    st.subheader("Please choose specific district you want to discover:")
    # Create a select box to select the district
    selected_district_code = st.selectbox('Select a district:', data['DISTRICT'].unique())
    selected_district = dict_name[selected_district_code]

    st.write("You choose", selected_district)

    # Filter the data for the selected district
    st.write("The following table is all offense description in", selected_district)
    selected_district_data = data[data['DISTRICT'] == selected_district_code][["DISTRICT", "OFFENSE_DESCRIPTION"]]
    st.write(selected_district_data)

    # Group by crime category and count occurrences
    crime_type=selected_district_data['OFFENSE_DESCRIPTION'].unique()
    crime_counts =selected_district_data['OFFENSE_DESCRIPTION'].value_counts()

    st.write("Here is bar chart covering all type of offense in",selected_district)
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(30, 24))

    # Plot the horizontal bar chart for crime counts
    sns.barplot(x=crime_counts.values, y=crime_counts.index, color="b", label="Total")

    # Add labels and title
    ax.set(xlabel="Count", ylabel="Crime Category", title=f'Crime Statistics in {selected_district}')
    max_type=crime_counts.idxmax()
    st.write("The highest type of crime in",selected_district,"is",max_type)
    # Display the chart using Streamlit
    st.pyplot(f)
    #select specific crime  you want to see
    st.subheader("Please choose specific offense you want to see:")
    selected_offenses = st.multiselect('Select Offense Descriptions (you can select multiple):', crime_type)



    # Filter data for the selected offense descriptions
    selected_offense_data = selected_district_data[selected_district_data['OFFENSE_DESCRIPTION'].isin(selected_offenses)]

    # Group by crime category and count occurrences for selected offenses
    selected_counts = selected_offense_data['OFFENSE_DESCRIPTION'].value_counts()

    # Visualization - Bar chart for selected offense descriptions
    st.bar_chart(selected_counts,color="#F9B700")




def highest_crime_week():
    st.title("Highest crime day in a week")
    data['OCCURRED_ON_DATE'] = pd.to_datetime(data['OCCURRED_ON_DATE'])


    data['DAY_OF_WEEK'] = data['OCCURRED_ON_DATE'].dt.day_name()

    crime_by_day = data['DAY_OF_WEEK'].value_counts()

    st.bar_chart(crime_by_day,color='#F9B700',height=600, width=800,use_container_width=True)

    max_crime_day = crime_by_day.idxmax()
    st.write(f'The day with the highest crime rate is: {max_crime_day}')


    chart_data = pd.DataFrame({'CrimeCount': crime_by_day})
    st.table(chart_data)
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
def highest_crime_month():
    st.title("Highest crime month in 2023")
    crime_by_month = data['MONTH'].value_counts()

    # Plot the crime occurrences by month
    st.bar_chart(crime_by_month, color='#F9B700', height=600, width=800)

    # Find the month with the highest crime count
    max_crime_month = crime_by_month.idxmax()
    st.write("The Month with the highest crime rate is",month_dict[max_crime_month])
    st.link_button("Why temperature increase the crime rate?","https://www.forbes.com/sites/ariannajohnson/2023/07/06/heres-why-warm-weather-causes-more-violent-crimes-from-mass-shootings-to-aggravated-assault/?sh=4f5cae925ab3")


# Title and Subheader
def createslider():
    highest_crime_week()
    highest_crime_month()
    st.title("Crime happened within range of chosen months")
    st.subheader("Select your time range")




    month_range = st.slider("Double-ended slider", 1,12, value=(1, 12))
    st.write("You select to see the crime between",month_dict[month_range[0]],"and",month_dict[month_range[1]])
    filtered_data = data[(data['MONTH'] >= month_range[0]) & (data['MONTH'] <= month_range[1])]
    sorted_data = filtered_data.sort_values(by='MONTH')
    columns_to_display = ["MONTH", "INCIDENT_NUMBER", "OFFENSE_DESCRIPTION", "DISTRICT", "OCCURRED_ON_DATE"]
    st.dataframe(sorted_data[columns_to_display])
    st.write("Filtered Data Table:")


page_names= {"Crime in Specific District": display_crime_statistics,"Highest crime time":createslider}


code = st.sidebar.selectbox("Choose a topic you want to discover", page_names.keys())
page_names[code]()