import boto3
import json

translate = boto3.client('translate')

SOURCE_TEXT = ("<Sample Input Text>")

OUTPUT_LANG_CODE = 'en'

result = translate.translate_text(
    Text=SOURCE_TEXT,
    SourceLanguageCode='auto',
    TargetLanguageCode=OUTPUT_LANG_CODE,
    Settings={'Profanity': 'MASK'}
)

print("Translated Text:{}".format(result['TranslatedText']))
