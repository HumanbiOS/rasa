import pandas as pd


df = pd.read_csv("countries.csv")
base_df = pd.read_csv("data_countries.csv")

countries = list()
for index, base_row in base_df.iterrows():
    countries.append(base_row['Country Name'])

i = 0
with open("data_country_codes.csv", "w+") as cc, open("data_country_flags.csv", "w+") as cf:
    cc.write("Country Code\n")
    cf.write("Country Flag\n")
    for index, each_row in df.iterrows():
        if each_row['Country Name'] in countries:
            #print(i, each_row['Country Name'], each_row['Country Code'], each_row['Country Flag'], sep=" " * 10 + "\t")
            #i += 1
            cc.write(f"{each_row['Country Code']}\n")
            cf.write(f"{each_row['Country Flag']}\n")
