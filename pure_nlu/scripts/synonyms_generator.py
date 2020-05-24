from itertools import product
import pandas as pd
import environ
import pathlib
import random
import yaml

ROOT = pathlib.Path(environ.Path(__file__) - 2)

def parse_data():
    data_file_path = ROOT / "csv" / "raw_language_data.csv"
    df = pd.read_csv(data_file_path)
    
    #flags_path = ROOT / "csv" / "flag_emoticons.csv"
    #df = pd.read_csv(flags_path)
    
    synonyms_fp = ROOT / "csv" / "synonyms_file.md"
    lookup_table_lc_fp = ROOT / "csv" / "lookups" / "language_codes.txt"
    lookup_table_ln_fp = ROOT / "csv" / "lookups" / "language_names.txt"
    examples_lc = ROOT / "csv" / "language_codes.csv"
    examples_ln = ROOT / "csv" / "language_names.csv"
    training_prefixes_fp = ROOT / "csv" / "context_prefixes.csv"
    training_suffixes_fp = ROOT / "csv" / "context_suffixes.csv"

    with open(synonyms_fp, "w+") as sf, open(lookup_table_lc_fp, "w+") as table_lc, open(lookup_table_ln_fp, "w+") as table_ln:
    #if True:
        for index, each_row in df.iterrows():
            
            # Write lookup tables
            table_lc.write(f"{each_row['Language Code']}\n")
            table_ln.write(f"{each_row['Language Name']}\n")
            
            # Write synonyms to the language code
            lc_synonym = f"## synonym:{each_row['Language Code']}\n"
            for each in [each_row['Language Code'], each_row['Country Flag']]:
                # Drop 'NaN' values
                if type(each) != str:
                    continue
                lower = each.lower()
                upper = each.upper()
                lc_synonym += f"- {each}\n"
                if each != lower:
                    lc_synonym += f"- {lower}\n"
                if each != upper:
                    lc_synonym += f"- {upper}\n"
            lc_synonym += "\n"
            sf.write(lc_synonym)
            
            # Write synonyms to the language name
            ln_synonym = f"## synonym:{each_row['Language Name']}\n"
            for each in [each_row['Language Name']]:
                # Drop 'NaN' values
                if type(each) != str:
                    continue
                lower = each.lower()
                upper = each.upper()
                ln_synonym += f"- {each}\n"
                if each != lower:
                    ln_synonym += f"- {lower}\n"
                if each != upper:
                    ln_synonym += f"- {upper}\n"
            ln_synonym += "\n"
            sf.write(ln_synonym)

            #print(synonym, end="")
    
    # Prepare examples context parts
    training_prefixes = list()
    with open(training_prefixes_fp) as tp:
        for each_prefix in tp.readlines():
            training_prefixes.append(each_prefix.strip())
    training_suffixes = list()
    with open(training_suffixes_fp) as ts:
        for each_suffix in ts.readlines():
            training_suffixes.append(each_suffix.strip())
    context_parts = list(product(training_prefixes, training_suffixes))

    # use only 45% of the permutated parts
    random_percentage = len(context_parts) * 45 // 100
    with open(examples_ln, "w+") as x_ln, open(examples_lc, "w+") as x_lc:
        # Create examples for training the NLU model
        # .45 means 45% of the data to be used in samples
        for index, sample_row in df.sample(frac = .45).iterrows():
            x_lc.write(f"[{sample_row['Language Code']}](language_code)\n")
            x_ln.write(f"[{sample_row['Language Name']}](language_name)\n")
            for p, s in random.sample(context_parts, random_percentage):
                x_lc.write(f"{p} [{sample_row['Language Code']}](language_code) {s}".strip() + "\n")
                x_ln.write(f"{p} [{sample_row['Language Name']}](language_name) {s}".strip() + "\n")

if __name__ == "__main__":
    parse_data()
