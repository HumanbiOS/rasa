import pandas as pd


#df_lc = pd.read_csv("data_country_codes.csv")
df_ln = pd.read_csv("data_country_names.csv")

total = list()
#ccodes = [row['Country Code'] for _, row in df_lc.iterrows()]
#total.extend(ccodes)
cnames = [row['Country Name'] for _, row in df_ln.iterrows()]
total.extend(cnames)

#with open("synonyms.csv", "w+") as ss:
#    ss.write(f"Language Code,Language Name\n")
#    for lc, ln in zip(lcodes, lnames):
#        ss.write(f"{lc},{ln}\n")

with open("data.txt", "w+") as file_:
    for each in total:
        file_.write(f"{each}\n")
