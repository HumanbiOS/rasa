from itertools import product
from math import floor
import pandas as pd
import environ
import pathlib
import random
import yaml
import os


ROOT = pathlib.Path(environ.Path(__file__) - 1)

with open(ROOT / "generator-config.yml") as config:
    config = yaml.safe_load(config)

RAW_DATA = ROOT / "csv"
DATA = ROOT / "data"

with open(DATA / "nlu.md", 'w+') as nlu:
    all_lookups = {}
    # All intents from config
    for intent_name, intent_config in config['intents'].items():
        # Write name of the intent
        nlu.write(f'## intent:{intent_name}\n')
        for config_item in intent_config:
            folder = config_item.get('folder')
            if folder is None:
                raise ValueError(f"You have to add 'folder' to the intent {intent_name} ({config_item})")
            path = RAW_DATA / folder
            
            source = config_item.get('source')
            # Pickup source files
            if source is None:
                # TODO: Add later
                raise NotImplementedError(f"Generator should pickup all 'data_*.csv' files. Not implemented yet.")
            
            lookup = config_item.get('lookup', False)
            if lookup and not os.path.exists(DATA / "lookups"):
                os.mkdir(DATA / "lookups")
            extract = config_item.get('extract', False)
            if (extract and not lookup) or (not extract and lookup):
                raise ValueError(f"You must have both or none extract-lookup values, you have:\n    extract: {extract}\n    lookup: {lookup}")
            
            prefixes = config_item.get('prefixes', 'prefixes.csv')
            suffixes = config_item.get('suffixes', 'suffixes.csv')
            random_percentage = float(config_item.get("random_percentage", "45")) / 100

            # Prepare examples context parts
            # Prefixes
            training_prefixes = list()
            p_path = path / prefixes
            if os.path.exists(p_path):
                with open(p_path) as tp:
                    for each_prefix in tp:
                        training_prefixes.append(each_prefix.strip())
            # Suffixes
            training_suffixes = list()
            s_path = path / suffixes
            if os.path.exists(s_path):
                with open(s_path) as ts:
                    for each_suffix in ts:
                        training_suffixes.append(each_suffix.strip())
            context_parts = list(product(training_prefixes, training_suffixes))
                
            df = pd.read_csv(path / source)
            _key = [_ for _ in df][0]
            
            # Writing lookups
            if extract and lookup:
                lookup_fp = DATA / 'lookups' / f"{extract}.txt"
                with open(lookup_fp, "w+") as lookup_file:
                    for index, row in df.iterrows():
                        lookup_file.write(f'{row[_key]}\n')
                all_lookups[extract] = pathlib.Path("data", "lookups", f"{extract}.txt")

            # Writing data          
            for index, sample_row in df.sample(frac = random_percentage).iterrows():
                if extract:
                    # writing the examples
                    nlu.write(f"- [{sample_row[_key]}]({extract})\n")
                    for p, s in random.sample(context_parts, floor(len(context_parts) * random_percentage)):
                        nlu.write("- " + f"{p} [{sample_row[_key]}]({extract}) {s}".strip() + "\n")
                else:
                    nlu.write(f"- {sample_row[_key]}\n")
        nlu.write("\n\n")

    inconsistency = dict()
    errors = dict()
    for folder, column in config['synonyms'].items():
        path = RAW_DATA / folder / 'synonyms.csv'
        synonyms = pd.read_csv(path, na_filter=False)
        keys = [k for k in synonyms]
        for index, synonym_row in synonyms.iterrows():
            nlu.write(f"## synonym:{synonym_row[column]}\n")
            _synonyms = set()
            for each in keys:
                each_v = synonym_row[each]
                _synonyms.add(each_v)
                _synonyms.add(each_v.upper())
                _synonyms.add(each_v.lower())
            for each_syn in _synonyms:
                if each_syn not in inconsistency:
                    inconsistency[each_syn] = column
                    nlu.write(f'- {each_syn}\n')
                else:
                   #print(f"Found repeating value: (column={inconsistency[each_syn]}, value={each_syn}); existing value: (column={column}, value={each_syn})")
                   errors[each_syn] = column
            nlu.write("\n")
    print(f"Found {len(errors)} repeating values.")
    del inconsistency
    del errors

    for each in all_lookups:
        nlu.write(f"## lookup:{each}\n")
        nlu.write(str(all_lookups[each]) + "\n\n")

    # Writing raw files from misc category
    for misc_files in config['misc']:
        with open(RAW_DATA / misc_files) as misc_file:
            for line in misc_file:
                nlu.write(line)

