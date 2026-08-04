import streamlit as st
from datetime import datetime
import fastf1
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

fastf1.Cache.enable_cache('cache')

st.title("F1 Driver Season Performance Dashboard")
st.write("Hello! This is my first Streamlit app.")

current_year = datetime.now().year
years = list(range(2018, current_year + 1))

year = st.selectbox("Select a year", years)

@st.cache_data
def load_schedule(year):
    schedule = fastf1.get_event_schedule(year)
    schedule = schedule[schedule['RoundNumber'] > 0]
    return schedule['EventName'].tolist()

race_names = load_schedule(year)

race = st.selectbox("Select a race", race_names)

@st.cache_data
def load_drivers(year, race):
    session = fastf1.get_session(year, race, 'R')
    session.load(laps=False, telemetry=False, weather=False, messages=False)
    drivers = session.results['Abbreviation'].tolist()
    return drivers

with st.spinner(f"Loading drivers for {race} {year}..."):
    driver_list = load_drivers(year, race)

driver = st.selectbox("Select a driver", driver_list)

@st.cache_data
def load_laps(year, race, driver):
    session = fastf1.get_session(year, race, 'R')
    session.load(telemetry=False, weather=False, messages=False)
    laps = session.laps.pick_drivers(driver)
    return laps

with st.spinner(f"Loading lap times for {driver}..."):
    laps = load_laps(year, race, driver)

compound_colors = {
    'HYPERSOFT': '#FF1493',
    'ULTRASOFT': '#9400D3',
    'SUPERSOFT': '#FF4500',
    'SOFT': 'red',
    'MEDIUM': 'yellow',
    'HARD': 'white',
    'INTERMEDIATE': 'green',
    'WET': 'blue'
}

laps = laps.dropna(subset=['Compound', 'Stint'])

fig, ax = plt.subplots(figsize=(12, 6))

for stint_number in laps['Stint'].unique():
    stint_laps = laps[laps['Stint'] == stint_number]
    compound = stint_laps['Compound'].iloc[0]
    color = compound_colors.get(compound, 'gray')
    ax.plot(
        stint_laps['LapNumber'],
        stint_laps['LapTime'].dt.total_seconds(),
        color=color,
        marker='o',
        label=compound,
        markeredgecolor='black'
    )

ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time (seconds)")
ax.set_title(f"{driver} Lap Times by Tire Compound - {race} {year}")

handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

ax.grid(True)

st.pyplot(fig)

st.subheader("Track Dominance Map")

driver2_options = [d for d in driver_list if d != driver]

if len(driver2_options) > 0:
    driver2 = st.selectbox("Compare against", driver2_options)

    @st.cache_data
    def load_telemetry_comparison(year, race, driver1, driver2):
        session = fastf1.get_session(year, race, 'R')
        session.load(telemetry=True, weather=False, messages=False)

        lap1 = session.laps.pick_drivers(driver1).pick_fastest()
        lap2 = session.laps.pick_drivers(driver2).pick_fastest()

        tel1 = lap1.get_telemetry().add_distance()
        tel2 = lap2.get_telemetry().add_distance()

        num_minisectors = 25
        total_distance = tel1['Distance'].max()
        minisector_length = total_distance / num_minisectors

        tel1['Minisector'] = (tel1['Distance'] // minisector_length).astype(int)
        tel2['Minisector'] = (tel2['Distance'] // minisector_length).astype(int)

        avg_speed1 = tel1.groupby('Minisector')['Speed'].mean()
        avg_speed2 = tel2.groupby('Minisector')['Speed'].mean()

        comparison = pd.DataFrame({
            driver1: avg_speed1,
            driver2: avg_speed2
        })
        comparison['Fastest'] = comparison.idxmax(axis=1)

        tel1['Fastest'] = tel1['Minisector'].map(comparison['Fastest'])

        return tel1, comparison

    with st.spinner(f"Loading telemetry for {driver} vs {driver2}..."):
        tel1, comparison = load_telemetry_comparison(year, race, driver, driver2)

    fig2 = go.Figure()
    colors = {driver: 'blue', driver2: 'red'}

    for minisector_num in sorted(tel1['Minisector'].unique()):
        segment = tel1[tel1['Minisector'] == minisector_num]
        fastest_driver = comparison.loc[minisector_num, 'Fastest']
        speed1 = comparison.loc[minisector_num, driver]
        speed2 = comparison.loc[minisector_num, driver2]

        hover_text = (
            f"Minisector {minisector_num}<br>"
            f"Fastest: {fastest_driver}<br>"
            f"{driver}: {speed1:.1f} km/h<br>"
            f"{driver2}: {speed2:.1f} km/h"
        )

        fig2.add_trace(go.Scatter(
            x=segment['X'],
            y=segment['Y'],
            mode='lines',
            line=dict(color=colors[fastest_driver], width=4),
            showlegend=False,
            hovertext=hover_text,
            hoverinfo='text'
        ))

    for driver_name, color in colors.items():
        fig2.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='lines',
            line=dict(color=color, width=4),
            name=driver_name
        ))

    fig2.update_layout(
        title=f"Track Dominance: {driver} vs {driver2} - {race} {year}",
        xaxis_title="X position",
        yaxis_title="Y position",
        yaxis_scaleanchor="x"
    )

    st.plotly_chart(fig2)
else:
    st.write("Need at least two drivers in this race to compare.")