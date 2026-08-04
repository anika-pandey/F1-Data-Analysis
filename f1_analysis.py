import fastf1
import matplotlib.pyplot as plt

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2024, 'Bahrain', 'R')
session.load()

verstappen = session.laps.pick_driver('VER')
perez = session.laps.pick_driver('PER')
sainz = session.laps.pick_driver('SAI')

plt.figure(figsize=(12, 6))

plt.plot(verstappen['LapNumber'], verstappen['LapTime'].dt.total_seconds(), label='Verstappen', color='blue')
plt.plot(perez['LapNumber'], perez['LapTime'].dt.total_seconds(), label='Perez', color='orange')
plt.plot(sainz['LapNumber'], sainz['LapTime'].dt.total_seconds(), label='Sainz', color='red')

plt.xlabel('Lap Number')
plt.ylabel('Lap Time (seconds)')
plt.title('Lap Time Comparison - 2024 Bahrain GP')
plt.legend()
plt.grid(True)
plt.savefig('lap_comparison.png')
plt.show()