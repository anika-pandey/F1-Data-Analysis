# F1 Driver Season Performance Dashboard
 
An interactive Streamlit dashboard for exploring real Formula 1 race data. Pick any driver, race, and year, and see their lap times, tire strategy, and pit stops, all pulled from real F1 telemetry using the FastF1 API.
 
## Features
 
- **Year, race, and driver selection.** The dropdowns are built from real F1 data, so they update automatically based on who actually raced that season.
- **Lap time and tire chart.** Shows a driver's pace lap by lap, color coded by tire compound, so you can actually see pit stops and tire wear happening.
- **Pit stop time loss calculator.** Estimates how much time each pit stop cost by comparing the in and out laps to the driver's normal pace. It also flags laps affected by Safety Car, VSC, or yellow flags so those numbers don't get mixed in with real pit stop time.
- **Track Dominance Map.** An interactive map comparing two drivers around the actual track, built from real telemetry data. You can hover over any part of the track and see who was faster there and by how much.
- **Gap to Leader chart.** Shows how far behind the race winner a driver was, lap by lap, with pit stops marked directly on the chart.
## Tech stack
 
- Python
- [FastF1](https://github.com/theOehrly/Fast-F1) for the actual F1 timing and telemetry data
- Streamlit for the interactive app
- Plotly for the track map and hover tooltips
- pandas for all the data processing
- matplotlib for the lap time and tire charts
## How to run it
 
1. Clone this repo
2. Install dependencies:
```
   pip3 install fastf1 pandas matplotlib streamlit plotly
```
3. Run it:
```
   streamlit run app.py
```
4. It'll open in your browser at `localhost:8501`
## What I learned
 
This started as one static chart and turned into a full dashboard. Along the way I learned how Streamlit's caching works, how to rebuild a track's actual shape from raw telemetry data, and how to compare two drivers using small sections of the track instead of just the 3 official sectors. I also ran into a bunch of real data problems, like telemetry not being available yet for very recent races, tire compound names being different in older seasons, and realizing that pit stop laps affected by a Safety Car shouldn't count the same as a normal stop.
 
## Known issues
 
- The Gap to Leader chart can be a little off around Safety Car periods or pit stop cycles since it's based on total race time and not live position data.
- The Track Dominance Map's telemetry isn't available for every race/driver combination, particularly some races from the 2018-2019 seasons. The app detects this and shows a message instead of crashing, but the comparison just won't be available for those pairs.
- Tire degradation is treated as a simple average per compound right now rather than modeled as a rate over the stint, so early/late stint laps can slightly skew the picture for very long stints.
## About this project
 
I'm building this over the summer because I have been a huge Formula 1 fan since a young age. I am very interested in motorsport engineering and want to understand how race strategy and car performance data actually get analyzed. I'm hoping to keep building on this as I explore opportunities in motorsport engineering going forward.
