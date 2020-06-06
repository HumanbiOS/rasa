import pandas as pd


df = pd.read_csv("_synonyms.csv")
base_df = pd.read_csv("data_country_names.csv")

countries = list()
for index, base_row in base_df.iterrows():
    countries.append(base_row['Country Name'])

with open("synonyms.csv", "w+") as ss:
    keys = ["Country Name", "Country Flag"]
    ss.write(f"{','.join(keys)}\n")
    for index, row in df.iterrows():
        if row['Country Name'] in countries:
            try:
                if row['Country Name'] == "Namibia":
                    row['Country Code'] = "NA"
                ss.write(f"{','.join([row[key] for key in keys])}\n")
            except:
                print(row)
            
