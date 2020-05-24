import pandas as pd
import environ
import pathlib
import yaml

ROOT = pathlib.Path(environ.Path(__file__) - 2)

def parse_data():
    data_file_path = ROOT / "csv" / "raw_language_data.csv"
    df = pd.read_csv(data_file_path)
    
    #flags_path = ROOT / "csv" / "flag_emoticons.csv"
    #df = pd.read_csv(flags_path)
    
    synonyms_fp = ROOT / "csv" / "synonyms_file.md"
    lookup_table_lc_fp = ROOT / "csv" / "lookups" / "language_codes.txt"
    examples_lc = ROOT / "csv" / "language_codes.csv"
    examples_ln = ROOT / "csv" / "language_names.csv"

    with open(synonyms_fp, "w+") as sf, open(lookup_table_lc_fp, "w+") as table_lc:
    #if True:
        for index, each_row in df.iterrows():
            # Write language codes lookup table
            table_lc.write(f"{each_row['Language Code']}\n")
            # Write synonyms to the language code
            synonym = f"## synonym:{each_row['Language Code']}\n"
            for each in each_row:
                # Drop 'NaN' values
                if type(each) != str:
                    continue
                lower = each.lower()
                upper = each.upper()
                synonym += f"- {each}\n"
                if each != lower:
                    synonym += f"- {lower}\n"
                if each != upper:
                    synonym += f"- {upper}\n"
            synonym += "\n\n"
            sf.write(synonym)
            #print(synonym, end="")
    
    with open(examples_ln, "w+") as x_ln, open(examples_lc, "w+") as x_lc:
        # Create examples for training the NLU model
        # .2 means 20% of the data to be used in samples
        for index, sample_row in df.sample(frac = .2).iterrows():
            x_lc.write(f"{sample_row['Language Code']}\n")
            x_ln.write(f"{sample_row['Language Name']}\n")


if __name__ == "__main__":
    parse_data()
