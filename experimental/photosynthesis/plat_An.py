import pandas as pd
import matplotlib.pyplot as plt
import sys;



# Read the CSV file
df = pd.read_csv('../../experimental/photosynthesis/results/photo_P_wet.csv', sep =';')

print(df)
# Plot Q as a line plot
plt.plot(df['q'], df['P0_q'], label = 'P0')
plt.plot(df['q'], df['P1_q'], label = 'P1')
plt.plot(df['q'], df['P2_q'], label = 'P2')
plt.plot(df['q'], df['P3_q'], label = 'P3')

plt.xlabel('Photosynthetic active radiation ($mol$ $m^{-2} s^{-1})$')
plt.ylabel('single plant An ($µmol$ $CO_2$ $m^{-2} s^{-1}$)')
plt.legend()
# plt.show()


# Plot Cs as a line plot
plt.plot(df['cs'], df['P0_cs'], label = 'P0')
plt.plot(df['cs'], df['P1_cs'], label = 'P1')
plt.plot(df['cs'], df['P2_cs'], label = 'P2')
plt.plot(df['cs'], df['P3_cs'], label = 'P3')

plt.xlabel('CO$_2$ concentration ($mol$ $mol^{-1}$)')
plt.ylabel('single plant An ($µmol$ $CO_2$ $m^{-2} s^{-1}$)')
plt.legend()
# plt.show()

# Plot Temp as a line plot
plt.plot(df['temp'], df['P0_temp'], label = 'P0')
plt.plot(df['temp'], df['P1_temp'], label = 'P1')
plt.plot(df['temp'], df['P2_temp'], label = 'P2')
plt.plot(df['temp'], df['P3_temp'], label = 'P3')

plt.xlabel('Temp. (°C)')
plt.ylabel('single plant An ($µmol$ $CO_2$ $m^{-2} s^{-1}$)')
plt.legend()
# plt.show()

ti = pd.read_csv('../../experimental/photosynthesis/results/photo_P_time_wet.csv', sep =';')

print(ti)
plt.close()
plt.plot(ti['time'], ti['P0'], label = 'P0')
plt.plot(ti['time'], ti['P1'], label = 'P1')
plt.plot(ti['time'], ti['P2'], label = 'P2')
plt.plot(ti['time'], ti['P3_2'], label = 'P3')

plt.xlabel('time (h)')
plt.ylabel('single plant An ($µmol$ $CO_2$ $s^{-1}$)')
plt.legend()
plt.show()