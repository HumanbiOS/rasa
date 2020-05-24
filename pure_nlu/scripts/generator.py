import environ
import pathlib
import shutil
import yaml
import os


ROOT = pathlib.Path(environ.Path(__file__) - 2)

def parse_data():
    with open(ROOT / "generator-config.yml") as config:
        config = yaml.safe_load(config)
    
    intents = config['intents']
    path = ROOT / 'data' / 'nlu.md'
    with open(path, 'w+') as nlu:
        # All intents from config
        for intent_name, intents_configs in config['intents'].items():
            # Write name of the intent
            nlu.write(f'## intent:{intent_name}\n')
            for intent_config in intents_configs:
                # Entity name to extract line as
                extract_as = intent_config.get('extract_as')
                # For each line in source, write to nlu.md
                source_path = ROOT / 'csv' / intent_config['source']
                with open(source_path) as source:
                    for line in source:
                        line = line.strip('\n')
                        # Empty line safe-check
                        if line:
                            if extract_as:
                                nlu.write(f"- [{line}]({extract_as})\n")
                            else:
                                nlu.write(f"- {line}\n")
            # Empty line in the end
            nlu.write("\n")
        
        for misc_files in config['misc']:
            source_path = ROOT / 'csv' / misc_files
            with open(source_path) as source:
                for line in source:
                    nlu.write(line)
    lookups_path = ROOT / "data" / "lookups"
    if not os.path.exists(lookups_path):
        os.mkdir(lookups_path)
    lookups_src = ROOT / "csv" / "lookups"
    for each in os.listdir(lookups_src):
        shutil.copyfile(lookups_src / each, lookups_path / each)


if __name__ == "__main__":
    parse_data()

