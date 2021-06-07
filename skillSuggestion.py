import pandas as pd
import ast


def suggestSkills(skills):
    suggestions = []

    t_h = 25 #change this threashold value

    df = pd.read_csv('./stack_network_links.csv', header=0)
    # print(df.columns)
    # print(df)
    for index, row in df.iterrows():
        if df.empty:
            print("Row #"+ str(index) +" is Blank")

        if (row['source'].lower() in ast.literal_eval(str(skills).lower())) and (row['target']).lower() not in ast.literal_eval(str(skills).lower()) and (int(row['value']) >= t_h):
            suggestions.append({"suggest": str(row['target']), "for": str(row['source']), "value": str(row['value'])})

    print("Suggesting skills Done")
    # print(suggestions)
    return suggestions