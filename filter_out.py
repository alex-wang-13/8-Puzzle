import sys
import re

# Check for text file argument.
if len(sys.argv) < 2:
    print("Requires 1 valid file name.")
else:
    filename = sys.argv[1]

data = []

with open(filename+".output", "r") as file:
    for line in file:
        matches = []
        matches.extend(re.findall(r"Nodes considered: (\d+)", line))
        matches.extend(re.findall(r"\bd: (\d+)", line))
        matches.extend(re.findall(r"--- (\d+\.\d+) seconds ---", line))
        if matches:
            data.extend(matches)

with open(filename+".csv","w") as file:
    file.write("Nodes Considered,Depth,Time Elapsed\n")
    for i in range(0, len(data), 3):
        line = ",".join(data[i:i+3])
        file.write(line+"\n")

import pandas as pd
dataframe = pd.read_csv(filename+".csv")
# Sort by depth.
dataframe.sort_values(["Depth", "Nodes Considered", "Time Elapsed"], inplace=True)
with open(filename+".stats", "w") as file:
    average_time = dataframe["Time Elapsed"].mean()
    average_nodes = dataframe["Nodes Considered"].mean()
    average_depth = dataframe["Depth"].mean()
    median_time = dataframe["Time Elapsed"].median()
    median_nodes = dataframe["Nodes Considered"].median()
    median_depth = dataframe["Depth"].median()
    file.write("Average/Median Time To Search: " + str(average_time) + "/" + str(median_time) + "\n")
    file.write("Average/Median Solution Depth: " + str(average_depth) + "/" + str(median_depth) + "\n")
    file.write("Average/Median Nodes Considered: " + str(average_nodes) + "/" + str(median_nodes) + "\n\n")

    # Average time by depth.
    file.write("Average Time by Depth\n")
    file.write(dataframe.groupby(["Depth"])["Time Elapsed"].mean().to_string(header=False) + "\n\n")

    # Number of puzzles solved under max_nodes.
    file.write("Puzzles Solved Considering Less Than n Nodes\n")
    file.write("Less than or equal to 10 nodes:    " + str(len(dataframe[dataframe["Nodes Considered"] <= 10])) + "\n")
    file.write("Less than or equal to 100 nodes:   " + str(len(dataframe[dataframe["Nodes Considered"] <= 100])) + "\n")
    file.write("Less than or equal to 1000 nodes:  " + str(len(dataframe[dataframe["Nodes Considered"] <= 1000])) + "\n")
    file.write("Less than or equal to 10000 nodes: " + str(len(dataframe[dataframe["Nodes Considered"] <= 10000])) + "\n")
    file.write("Greater than 10000 nodes:          " + str(len(dataframe[dataframe["Nodes Considered"] > 10000])) + "\n\n")

    # Data sorted by depth.
    file.write("Data Sorted by Ascending Solution Depth\n")
    dataframe.sort_values(["Depth", "Nodes Considered", "Time Elapsed"], inplace=True)
    dataframe.insert(0, "Depth", dataframe.pop("Depth"))
    file.write(dataframe.to_string())