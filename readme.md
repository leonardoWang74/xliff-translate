# xliff translate
Automatically translate .xlf files.

## Dependencies
```bash
# google translate https://pypi.org/project/googletrans/
# https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group
pip install googletrans==4.0.0-rc1

# translate toolkit https://pypi.org/project/translate-toolkit/
pip install lxml
```

Go through steps in https://docs.translatehouse.org/projects/translate-toolkit/en/latest/installation.html

## Usage
1. Put your xliff files with ending `.xlf` into the folder (may have to create the folder) `xliff-files`.
2. Run `python3 xliff-translate.py`
3. Find results in folder `xliff-results`