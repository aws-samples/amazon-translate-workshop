import boto3
import json

translate = boto3.client(service_name='translate', region_name='us-east-1')

result = translate.translate_text(Text="How are you?", SourceLanguageCode="en", TargetLanguageCode="hi", Settings={"Formality": "INFORMAL"})
print('TranslatedText: ' + result.get('TranslatedText'))
print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
print('AppliedSettings: ' + json.dumps(result.get('AppliedSettings')))

print('')

result = translate.translate_text(Text="How are you?", SourceLanguageCode="en", TargetLanguageCode="hi", Settings={"Formality":"FORMAL"})
print('TranslatedText: ' + result.get('TranslatedText'))
print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
print('AppliedSettings: ' + json.dumps(result.get('AppliedSettings')))