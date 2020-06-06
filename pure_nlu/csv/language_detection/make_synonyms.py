import pandas as pd


df_lc = pd.read_csv("data_language_codes.csv")
df_ln = pd.read_csv("data_language_names.csv")

lcodes = [row['Language Code'] for _, row in df_lc.iterrows()]
lnames = [row['Language Name'] for _, row in df_ln.iterrows()]

with open("synonyms.csv", "w+") as ss:
    ss.write(f"Language Code,Language Name\n")
    for lc, ln in zip(lcodes, lnames):
        ss.write(f"{lc},{ln}\n")

#with open("data.txt", "w+") as file_:
#    for each in lcodes + lnames:
#        file_.write(f"{each}\n")
