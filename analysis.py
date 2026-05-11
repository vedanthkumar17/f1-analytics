import pandas as pd

df = pd.read_csv("merged.csv")

print("Average pit stop by team:")

print(df.groupby("team_name")["stop_duration"].mean(skipna = True).sort_values())

print("\nFastest individual pit stop:")
fastest_average_pit_stop = df.nsmallest(1, "stop_duration")[["team_name", "stop_duration"]]
print(fastest_average_pit_stop)

print(df.groupby("full_name")["stop_duration"].mean(skipna=True).sort_values(ascending = False))