# json2csv

**Tiny** utility that reads a JSON array (list of objects) and writes it as CSV.

## Usage
```bash
# From a file
python json2csv.py data.json > output.csv

# From stdin
cat data.json | python json2csv.py > output.csv

# Specify column order (optional)
python json2csv.py data.json --fields name,age,email > output.csv
```

## Install
Requires Python 3.7+.
```bash
pip install -r requirements.txt  # None needed, uses stdlib only
```

## How it works
- Loads JSON (expects a list of dictionaries).
- Determines column names from keys (or from `--fields`).
- Writes CSV using `csv.DictWriter`.

## License
MIT (see LICENSE file).