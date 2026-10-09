import csv
import random
import datetime as dt
import argparse
from urllib.request import urlretrieve
from pathlib import Path


def cli():
    examples_url = 'https://raw.githubusercontent.com/cldf-datasets/wals/refs/heads/master/cldf/examples.csv'
    languages_url = 'https://raw.githubusercontent.com/cldf-datasets/wals/refs/heads/master/cldf/languages.csv'

    cache_dir = Path.home() / '.cache' / 'cross_ling'
    cache_dir.mkdir(parents=True, exist_ok=True)
    examples_csv = cache_dir / 'languages.csv'
    languages_csv = cache_dir / 'examples.csv'

    if not examples_csv.exists():
        urlretrieve(examples_url, examples_csv)
    if not languages_csv.exists():
        urlretrieve(languages_url, languages_csv)

    parser = argparse.ArgumentParser(description="Prints cross-linguistic example of the day")
    parser.add_argument("--date",
                        type=str,
                        help="Manually enter date in format [YYYY-MM-DD]")

    args = parser.parse_args()
    date = str(dt.date.today())
    tomorrow = str(dt.date.today() + dt.timedelta(days=1))
    yesterday = str(dt.date.today() - dt.timedelta(days=1))

    with open(examples_csv) as example_file:
        reader = csv.DictReader(example_file)
        if args.date == 'tomorrow':
            random.seed(tomorrow)
            print("Cross-linguistic example of tomorrow:")
        elif args.date == 'yesterday':
            random.seed(yesterday)
            print("Cross-linguistic example of yesterday:")
        elif args.date and args.date not in ('tomorrow', 'yesterday'):
            arg_date = date.replace(date[-2:], args.date[-2:])
            random.seed(arg_date)
            print(f"Cross-linguistic example of {arg_date}: ")
        else:
            random.seed(date)
            print(f"Cross-linguistic example of today:")
        row = random.choice(list(reader))
        print(
            f"Language ID: {row['Language_ID']}\n"
            f"Primary Text: {row['Primary_Text']}\n"
            f"Analyzed word: {row['Analyzed_Word']}\n"
            f"Gloss: {row['Gloss']}\n"
            f"Translation: {row['Translated_Text']}\n"
        )
        lang_ID = row['Language_ID']
        with open(languages_csv) as language_file:
            reader_lang = csv.DictReader(language_file)
            for row in reader_lang:
                if lang_ID == row['ID']:
                    print(f"Name: {row['Name']}")
                    print(f"Family: {row['Family']}")
                    if row['Subfamily']:
                        print(f"Subfamily: {row['Subfamily']}")
                    print(f"Genus: {row['Genus']}")

if __name__ == '__main__':
    cli()
