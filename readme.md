# xliff translate
Automatically translate .xlf files.
Use case for me: translate generated .xlf files from Angular (i18n attribute).

## Dependencies
```bash
# if you want to use google translate https://pypi.org/project/googletrans/
# https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group
# bulk request did not work with version 4 
pip install googletrans==3.1.0a0

# if you want to use chatGPT as translator
pip install openai
pip install python-dotenv

```

## Usage
1. Put your xliff files with ending `.xlf` into the folder (may have to create the folder) `xliff-files`.
2. In `xliff-translate.py` choose translator by instantiating at comment `# create the translator you want here` either the Google translator `TranslatorGoogle` or the chatGPT translator `TranslatorChatGPT`.
3. Run `python3 xliff-translate.py`
4. Find results in folder `xliff-results`