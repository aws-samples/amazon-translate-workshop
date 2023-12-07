import boto3
import json

translate = boto3.client('translate')

with open('custom_terminology.csv', 'rb') as ct_file:
    translate.import_terminology(
        Name='custom-terminology-demo',
        MergeStrategy='OVERWRITE',
        Description='Terminology for Demo through boto3',
        TerminologyData={
            'File': ct_file.read(),
            'Format': 'CSV',
            'Directionality': 'MULTI'
        }
    )

response = translate.list_terminologies()
terminology_names = [tag["Name"] for tag in response["TerminologyPropertiesList"]]
print(str(terminology_names))

response = translate.get_terminology(
    Name='custom-terminology-demo',
    TerminologyDataFormat='CSV'
)

print("Name:{}".format(response["TerminologyProperties"]["Name"]))
print("Description:{}".format(response["TerminologyProperties"]["Description"]))
print("ARN:{}".format(response["TerminologyProperties"]["Arn"]))
print("Directionality:{}".format(response["TerminologyProperties"]["Directionality"]))

SOURCE_TEXT = ("Amazon a présenté aujourd'hui Echo Show 15, un nouvel ajout à la famille Echo Show qui est conçu pour être le cœur numérique de votre maison")

OUTPUT_LANG_CODE = 'en'

result = translate.translate_text(
    Text=SOURCE_TEXT,
    TerminologyNames=['custom-terminology-demo'],
    SourceLanguageCode='auto',
    TargetLanguageCode=OUTPUT_LANG_CODE
)

print("Translated Text:{}".format(result['TranslatedText']))