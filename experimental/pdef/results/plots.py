import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

runs=2
# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# List of file numbers
file_numbers = range(runs)

# Create an empty list to store the DataFrames
dfs_P0 = []
dfs_P1 = []
dfs_P2 = []
dfs_P3 = []

# Iterate over the file numbers
for number in file_numbers:
    # Generate the CSV file name
    P0 = os.path.join(current_directory, f"{number}_P0_plant_results.csv")

    # Read the CSV file into a temporary DataFrame
    P0_def = pd.read_csv(P0)

    # Add a new column for the "number" starting from 1
    P0_def['time'] = range(1, len(P0_def) + 1)

    # Add the temporary DataFrame to the list of DataFrames
    dfs_P0.append(P0_def)

# Concatenate the DataFrames in the list
P0 = pd.concat(dfs_P0, ignore_index=True)

# Calculate mean and standard deviation of each column by 'time'
P0_mean_values = P0.groupby('time').mean()
P0_std_values = P0.groupby('time').std()

# Reset the index of mean_values
P0_mean_values = P0_mean_values.reset_index()
P0_std_values = P0_std_values.reset_index()

# Iterate over the file numbers
for number in file_numbers:
    # Generate the CSV file name
    P1 = os.path.join(current_directory, f"{number}_P1_plant_results.csv")

    # Read the CSV file into a temporary DataFrame
    P1_def = pd.read_csv(P1)

    # Add a new column for the "number" starting from 1
    P1_def['time'] = range(1, len(P1_def) + 1)

    # Add the temporary DataFrame to the list of DataFrames
    dfs_P1.append(P1_def)

# Concatenate the DataFrames in the list
P1 = pd.concat(dfs_P1, ignore_index=True)

# Calculate mean and standard deviation of each column by 'time'
P1_mean_values = P1.groupby('time').mean()
P1_std_values = P1.groupby('time').std()

# Reset the index of mean_values
P1_mean_values = P1_mean_values.reset_index()
P1_std_values = P1_std_values.reset_index()

# Iterate over the file numbers
for number in file_numbers:
    # Generate the CSV file name
    P2 = os.path.join(current_directory, f"{number}_P2_plant_results.csv")

    # Read the CSV file into a temporary DataFrame
    P2_def = pd.read_csv(P2)

    # Add a new column for the "number" starting from 1
    P2_def['time'] = range(1, len(P2_def) + 1)

    # Add the temporary DataFrame to the list of DataFrames
    dfs_P2.append(P2_def)

# Concatenate the DataFrames in the list
P2 = pd.concat(dfs_P2, ignore_index=True)

# Calculate mean and standard deviation of each column by 'time'
P2_mean_values = P2.groupby('time').mean()
P2_std_values = P2.groupby('time').std()

# Reset the index of mean_values
P2_mean_values = P2_mean_values.reset_index()
P2_std_values = P2_std_values.reset_index()


# Iterate over the file numbers
for number in file_numbers:
    # Generate the CSV file name
    P3 = os.path.join(current_directory, f"{number}_P3_plant_results.csv")

    # Read the CSV file into a temporary DataFrame
    P3_def = pd.read_csv(P3)

    # Add a new column for the "number" starting from 1
    P3_def['time'] = range(1, len(P3_def) + 1)

    # Add the temporary DataFrame to the list of DataFrames
    dfs_P3.append(P3_def)

# Concatenate the DataFrames in the list
P3 = pd.concat(dfs_P3, ignore_index=True)

# Calculate mean and standard deviation of each column by 'time'
P3_mean_values = P3.groupby('time').mean()
P3_std_values = P3.groupby('time').std()

# Reset the index of mean_values
P3_mean_values = P3_mean_values.reset_index()
P3_std_values = P3_std_values.reset_index()

# Plot An 
plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['An_tot'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['An_tot'].values - P0_std_values['An_tot'].values,
                     P0_mean_values['An_tot'].values + P0_std_values['An_tot'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['An_tot'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['An_tot'].values - P1_std_values['An_tot'].values,
                     P1_mean_values['An_tot'].values + P1_std_values['An_tot'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['An_tot'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['An_tot'].values - P2_std_values['An_tot'].values,
                     P2_mean_values['An_tot'].values + P2_std_values['An_tot'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['An_tot'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['An_tot'].values - P3_std_values['An_tot'].values,
                     P3_mean_values['An_tot'].values + P3_std_values['An_tot'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('An plant')
plt.legend()
plt.show()
plt.close()
# Plot An mean

plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['An_mean'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['An_mean'].values - P0_std_values['An_mean'].values,
                     P0_mean_values['An_mean'].values + P0_std_values['An_mean'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['An_mean'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['An_mean'].values - P1_std_values['An_mean'].values,
                     P1_mean_values['An_mean'].values + P1_std_values['An_mean'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['An_mean'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['An_mean'].values - P2_std_values['An_mean'].values,
                     P2_mean_values['An_mean'].values + P2_std_values['An_mean'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['An_mean'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['An_mean'].values - P3_std_values['An_mean'].values,
                     P3_mean_values['An_mean'].values + P3_std_values['An_mean'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('An_mean')
plt.legend()
plt.show()
plt.close()

# Plot fw

plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['Fw_mean'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['Fw_mean'].values - P0_std_values['Fw_mean'].values,
                     P0_mean_values['Fw_mean'].values + P0_std_values['Fw_mean'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['Fw_mean'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['Fw_mean'].values - P1_std_values['Fw_mean'].values,
                     P1_mean_values['Fw_mean'].values + P1_std_values['Fw_mean'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['Fw_mean'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['Fw_mean'].values - P2_std_values['Fw_mean'].values,
                     P2_mean_values['Fw_mean'].values + P2_std_values['Fw_mean'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['Fw_mean'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['Fw_mean'].values - P3_std_values['Fw_mean'].values,
                     P3_mean_values['Fw_mean'].values + P3_std_values['Fw_mean'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('Fw')
plt.legend()
plt.show()
plt.close()

# Plot Vj

plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['Vj'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['Vj'].values - P0_std_values['Vj'].values,
                     P0_mean_values['Vj'].values + P0_std_values['Vj'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['Vj'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['Vj'].values - P1_std_values['Vj'].values,
                     P1_mean_values['Vj'].values + P1_std_values['Vj'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['Vj'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['Vj'].values - P2_std_values['Vj'].values,
                     P2_mean_values['Vj'].values + P2_std_values['Vj'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['Vj'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['Vj'].values - P3_std_values['Vj'].values,
                     P3_mean_values['Vj'].values + P3_std_values['Vj'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('Vj')
plt.legend()
plt.show()
plt.close()

plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['Vp'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['Vp'].values - P0_std_values['Vp'].values,
                     P0_mean_values['Vp'].values + P0_std_values['Vp'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['Vp'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['Vp'].values - P1_std_values['Vp'].values,
                     P1_mean_values['Vp'].values + P1_std_values['Vp'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['Vp'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['Vp'].values - P2_std_values['Vp'].values,
                     P2_mean_values['Vp'].values + P2_std_values['Vp'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['Vp'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['Vp'].values - P3_std_values['Vp'].values,
                     P3_mean_values['Vp'].values + P3_std_values['Vp'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('Vp')
plt.legend()
plt.show()
plt.close()

plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['Vc'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['Vc'].values - P0_std_values['Vc'].values,
                     P0_mean_values['Vc'].values + P0_std_values['Vc'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['Vc'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['Vc'].values - P1_std_values['Vc'].values,
                     P1_mean_values['Vc'].values + P1_std_values['Vc'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['Vc'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['Vc'].values - P2_std_values['Vc'].values,
                     P2_mean_values['Vc'].values + P2_std_values['Vc'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['Vc'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['Vc'].values - P3_std_values['Vc'].values,
                     P3_mean_values['Vc'].values + P3_std_values['Vc'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('Vc')
plt.legend()
plt.show()
plt.close()

plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['Rd'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['Rd'].values - P0_std_values['Rd'].values,
                     P0_mean_values['Rd'].values + P0_std_values['Rd'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['Rd'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['Rd'].values - P1_std_values['Rd'].values,
                     P1_mean_values['Rd'].values + P1_std_values['Rd'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['Rd'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['Rd'].values - P2_std_values['Rd'].values,
                     P2_mean_values['Rd'].values + P2_std_values['Rd'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['Rd'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['Rd'].values - P3_std_values['Rd'].values,
                     P3_mean_values['Rd'].values + P3_std_values['Rd'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('Rd')
plt.legend()
plt.show()
plt.close()

plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['Rd_ref'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['Rd_ref'].values - P0_std_values['Rd_ref'].values,
                     P0_mean_values['Rd_ref'].values + P0_std_values['Rd_ref'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['Rd_ref'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['Rd_ref'].values - P1_std_values['Rd_ref'].values,
                     P1_mean_values['Rd_ref'].values + P1_std_values['Rd_ref'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['Rd_ref'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['Rd_ref'].values - P2_std_values['Rd_ref'].values,
                     P2_mean_values['Rd_ref'].values + P2_std_values['Rd_ref'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['Rd_ref'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['Rd_ref'].values - P3_std_values['Rd_ref'].values,
                     P3_mean_values['Rd_ref'].values + P3_std_values['Rd_ref'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('Rd_ref')
plt.legend()
plt.show()
plt.close()


plt.figure()
plt.plot(P0_mean_values['time'].values, P0_mean_values['Ci'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['Ci'].values - P0_std_values['Ci'].values,
                     P0_mean_values['Ci'].values + P0_std_values['Ci'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['Ci'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['Ci'].values - P1_std_values['Ci'].values,
                     P1_mean_values['Ci'].values + P1_std_values['Ci'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['Ci'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['Ci'].values - P2_std_values['Ci'].values,
                     P2_mean_values['Ci'].values + P2_std_values['Ci'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['Ci'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['Ci'].values - P3_std_values['Ci'].values,
                     P3_mean_values['Ci'].values + P3_std_values['Ci'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('Ci')
plt.legend()
plt.show()
plt.close()
plt.figure()

plt.plot(P0_mean_values['time'].values, P0_mean_values['cics'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['cics'].values - P0_std_values['cics'].values,
                     P0_mean_values['cics'].values + P0_std_values['cics'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['cics'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['cics'].values - P1_std_values['cics'].values,
                     P1_mean_values['cics'].values + P1_std_values['cics'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['cics'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['cics'].values - P2_std_values['cics'].values,
                     P2_mean_values['cics'].values + P2_std_values['cics'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['cics'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['cics'].values - P3_std_values['cics'].values,
                     P3_mean_values['cics'].values + P3_std_values['cics'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('ci/cs')
plt.legend()
plt.show()
plt.close()


plt.plot(P0_mean_values['time'].values, P0_mean_values['Ev'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['Ev'].values - P0_std_values['Ev'].values,
                     P0_mean_values['Ev'].values + P0_std_values['Ev'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['Ev'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['Ev'].values - P1_std_values['Ev'].values,
                     P1_mean_values['Ev'].values + P1_std_values['Ev'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['Ev'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['Ev'].values - P2_std_values['Ev'].values,
                     P2_mean_values['Ev'].values + P2_std_values['Ev'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['Ev'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['Ev'].values - P3_std_values['Ev'].values,
                     P3_mean_values['Ev'].values + P3_std_values['Ev'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('E')
plt.legend()
plt.show()
plt.close()

plt.plot(P0_mean_values['time'].values, P0_mean_values['gco2'].values, label = 'P0')

plt.fill_between(P0_mean_values['time'].values, P0_mean_values['gco2'].values - P0_std_values['gco2'].values,
                     P0_mean_values['gco2'].values + P0_std_values['gco2'].values, alpha=0.3)

plt.plot(P1_mean_values['time'].values, P1_mean_values['gco2'].values,label = 'P1')

plt.fill_between(P1_mean_values['time'].values, P1_mean_values['gco2'].values - P1_std_values['gco2'].values,
                     P1_mean_values['gco2'].values + P1_std_values['gco2'].values, alpha=0.3)

plt.plot(P2_mean_values['time'].values, P2_mean_values['gco2'].values,label = 'P2')

plt.fill_between(P2_mean_values['time'].values, P2_mean_values['gco2'].values - P2_std_values['gco2'].values,
                     P2_mean_values['gco2'].values + P2_std_values['gco2'].values, alpha=0.3)

plt.plot(P3_mean_values['time'].values, P3_mean_values['gco2'].values,label = 'P3')

plt.fill_between(P3_mean_values['time'].values, P3_mean_values['gco2'].values - P3_std_values['gco2'].values,
                     P3_mean_values['gco2'].values + P3_std_values['gco2'].values, alpha=0.3)

plt.xlabel('time')
# plt.ylabel('Values')
plt.title('gco2')
plt.legend()
plt.show()
plt.close()

print(P0_mean_values)
print(P0_std_values)


x= [1.8,3.2,4.7,7.7]
blade = [P0_mean_values['blade'].mean(),P1_mean_values['blade'].mean(),P2_mean_values['blade'].mean(),P3_mean_values['blade'].mean()]
root = [P0_mean_values['root_length'].mean(),P1_mean_values['root_length'].mean(),P2_mean_values['root_length'].mean(),P3_mean_values['root_length'].mean()]
blade_std = [P0_std_values['blade'].mean(),P1_std_values['blade'].mean(),P2_std_values['blade'].mean(),P3_std_values['blade'].mean()]
root_std = [P0_std_values['root_length'].mean(),P1_std_values['root_length'].mean(),P2_std_values['root_length'].mean(),P3_std_values['root_length'].mean()]


print(blade,blade_std, root, root_std)


# Create figure and axes
fig, ax1 = plt.subplots()

# Plot blade data
ax1.plot(x, blade, color='blue', marker='o', label='blade')
ax1.fill_between(x, np.subtract(blade, blade_std), np.add(blade, blade_std),
                 color='blue', alpha=0.3)

# Set the labels and title for the first y-axis
ax1.set_xlabel('x')
ax1.set_ylabel('blade')
ax1.tick_params(axis='y', labelcolor='blue')

# Create second y-axis
ax2 = ax1.twinx()

# Plot root data
ax2.plot(x, root, color='red', marker='s', label='root')
ax2.fill_between(x, np.subtract(root, root_std), np.add(root, root_std),
                 color='red', alpha=0.3)

# Set the labels and title for the second y-axis
ax2.set_ylabel('root')
ax2.tick_params(axis='y', labelcolor='red')

# Display the legend
lines = ax1.get_lines() + ax2.get_lines()
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='best')
ax1.set_ylim(420,650)

ax2.set_ylim(600,2500)


# Display the plot
plt.show()

