import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import pydeck as pdk

#getting latest data
@st.cache
def get_data(url):
    return pd.read_csv(url)

df_confirmed = get_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df_deaths = get_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
# df_recovered = get_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = get_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')

#data manipulation
country_df = country_df.sort_values("Confirmed", ascending = False).reset_index(drop=True)

#title and introduction
# st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
st.title("Covid 19 Dashboard")
st.markdown("Built using python streamlit wtih live data from Johns Hopkins CSSE ")
st.markdown("Last data update :" + str(country_df['Last_Update'].min()))
st.header("Quote : PM Muhyiddin tells Malaysians")
st.markdown("> Just stay at home. No need to go out anywhere. With this, everyone can avoid and help stop the spread of the Covid-19 outbreak and Insyallah, it will be stopped. - 18 Mar 2020")

#Top 10 - Most impacted Country Scatter Graph with Slot
n = 10

st.header("Top 10 - Most Impacted Country")
fig = px.scatter(country_df.head(n), x="Country_Region", y="Confirmed", size="Confirmed", color="Country_Region",
               hover_data=['Deaths', 'Recovered', 'Active'], size_max=60)
fig.update_layout(
    title=str(n) +" Countries - Confirmed",
    xaxis_title="Countries",
    yaxis_title="Confirmed Cases",
    width = 700
    )
st.plotly_chart(fig)

#Global Counter
confirmed_total = country_df['Confirmed'].sum()
death_total = country_df['Deaths'].sum()
recovered_total = country_df['Recovered'].sum()
active_total = country_df['Active'].sum()
# st.markdown('<h1 style="color:blue;">This is a heading</h1>' + str(confirmed_total), unsafe_allow_html=True)

#Malaysia Counter
malaysia_value = country_df[country_df['Country_Region'] == 'Malaysia']
confirmed_malaysia = malaysia_value['Confirmed'].sum()
death_malaysia = malaysia_value['Deaths'].sum()
recovered_malaysia = malaysia_value['Recovered'].sum()
active_malaysia = malaysia_value['Active'].sum()

st.header("Malaysia Compared to Global")
st.markdown("Confirmed: "  + str(confirmed_malaysia) + "  [Global: "  + str(confirmed_total) + "]")
st.markdown("Deaths: " + str(death_malaysia) + "  [Global: " + str(death_total) + "]")
st.markdown("Recovered: " + str(recovered_malaysia) + "  [Global: " + str(recovered_total) + "]")
st.markdown("Active: " + str(active_malaysia) + "  [Global: " + str(active_total) + "]")

#Data at a glance with slider
st.header("Info : Data at a glance")
x = st.slider("Slide to change data count to view", min_value=5, max_value=50, value=10)
df_summary = country_df.sort_values("Confirmed", ascending = False)[["Country_Region", "Confirmed", "Deaths", "Recovered", "Active"]].reset_index(drop=True)
st.dataframe(df_summary.head(x).style.highlight_max(axis=0))

#Bar graph - Confirmed
st.header("Top 10 Confirmed Cases by Country")
fig = px.bar(country_df.head(n), x='Country_Region', y='Confirmed',
             hover_data=['Deaths', 'Recovered', 'Active'], color='Deaths',
             labels={'Confirmed':'Confirmed Counts'}, height=400)

st.plotly_chart(fig)

st.header("Top 10 Deaths Cases by Country")
fig = px.bar(country_df.sort_values("Deaths", ascending = False).head(n), x='Country_Region', y='Deaths',
             hover_data=['Confirmed', 'Recovered', 'Active'], color='Deaths',
             labels={'Deaths':'Deaths Counts'}, height=400)

st.plotly_chart(fig)

st.header("Top 10 Active Cases by Country")
fig = px.bar(country_df.sort_values("Active", ascending = False).head(n), x='Country_Region', y='Active',
             hover_data=['Confirmed', 'Deaths', 'Recovered'], color='Deaths',
             labels={'Active':'Active Counts'}, height=400)

st.plotly_chart(fig)

st.header("Top 10 Recovered Cases by Country")
fig = px.bar(country_df.sort_values("Recovered", ascending = False).head(n), x='Country_Region', y='Recovered',
             hover_data=['Confirmed', 'Deaths', 'Active'], color='Deaths',
             labels={'Recovered':'Recovered Counts'}, height=400)

st.plotly_chart(fig)

# def dfT (country):
#     dftest1 = df_confirmed[df_confirmed['Country/Region'] == country].transpose()
#     dftest1.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], inplace = True)
#     newcol1 = country + " Confirmed"
#     dftest1[newcol1] = dftest1.sum(axis=1)
#     dftest1 = dftest1.iloc[:,-1:]

#     dftest2 = df_deaths[df_deaths['Country/Region'] == country].transpose()
#     dftest2.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], inplace = True)
#     newcol2 = country + " Deaths"
#     dftest2[newcol2] = dftest2.sum(axis=1)
#     dftest2 = dftest2.iloc[:,-1:]

#     result = dftest1.join(dftest2)

#     fig = px.scatter(result, y = newcol1)

#     # fig.add_scatter(result, y=newcol2)

#     st.plotly_chart(fig)

# dfT("Australia")


def plot_cases_of_a_country(country):
    df_confirmed_average = df_confirmed.mean(axis=0).to_frame().transpose()
    df_deaths_average = df_deaths.mean(axis=0).to_frame().transpose()
    
    label1 = ['confirmed', 'deaths']
    label2 = ['confirmed_avg', 'deaths_avg']

    
    df_list1 = [df_confirmed, df_deaths]#, df_confirmed_average, df_deaths_average]
    df_list2 = [df_confirmed_average, df_deaths_average]

    fig = go.Figure()
    
    for i, df in enumerate(df_list1):
        x_data = np.array(list(df.iloc[:, -30:].columns))
        y_data = np.sum(np.asarray(df[df['Country/Region'] == country].iloc[:,-30:]),axis = 0)
            
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines',#'lines+markers',
        name=label1[i],
        text = "Total " + str(label1[i]) +": "+ str(y_data[-1])
        ))

    for i, df in enumerate(df_list2):
        x_data = np.array(list(df.iloc[:, -30:].columns))
        y_data = np.sum(np.asarray(df.iloc[:,-30:]),axis = 0)
            
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines',#'lines+markers',
        name=label2[i],
        text = "Average " + str(label2[i]) +": "+ str(y_data[-1])
        ))
    
    fig.update_layout(
        title="COVID 19 cases of " + country,
        xaxis_title='Date',
        yaxis_title='No. of Confirmed Cases'
    )
    
    st.plotly_chart(fig)


st.header("Cases by country compared to world average")
country_list = country_df['Country_Region'].tolist()

country_sel_box = st.selectbox("Country", country_list, 0)
plot_cases_of_a_country(country_sel_box)

df_map = country_df[['Country_Region', 'Lat', 'Long_', 'Confirmed']]
df_map.rename({'Lat': 'lat', 'Long_': 'lon'}, axis='columns', inplace=True)
df_map = df_map.dropna()
  
# Visualization Section
st.subheader("Map")
# st.map(df_map)


#map using pydeck
# Adding code so we can have map default to the center of the data
# midpoint = (np.average(df_map['lat']), np.average(df_map['lon']))

layer = pdk.Layer(
    "ScatterplotLayer",
    df_map,
    # pickable=True,
    # opacity=0.8,
    # stroked=True,
    # filled=True,
    # radius_scale=6,
    # radius_min_pixels=1,
    # radius_max_pixels=100,
    # line_width_min_pixels=1,
    get_position=['lon', 'lat'],
    get_radius="Confirmed",
    get_fill_color=[255, 140, 0],
    # get_line_color=[0, 0, 0],
)

# Set the viewport location
view_state = pdk.ViewState(7.3291, 49.6178, zoom=5, bearing=0, pitch=0)

# Render
# r = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', layers=[layer], initial_view_state=view_state, tooltip={"text": "{Country_Region}\n Confirmed : {Confirmed}"})
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{Country_Region}\n Confirmed Cases: {Confirmed}"})
r.to_html("scatterplot_layer.html", notebook_display=False)
st.pydeck_chart(r)

st.markdown('<small>© Copyright 2019, Masri Mustaman</small>', unsafe_allow_html=True)
st.markdown('<small>https://github.com/masrimustaman</small>', unsafe_allow_html=True)