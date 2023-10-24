import sys, getopt

import boto3
import json

REGION='us-east-1'
translate = boto3.client(service_name='translate', region_name=REGION, use_ssl=True)

def list_languages():    
    response = translate.list_languages()
    languages = response['Languages']

    for language in languages:
        print(language['LanguageName']+"-"+language['LanguageCode'])


def translate_text_synchronously():
    text = 'Amazon Translate is a text translation service that uses advanced machine learning technologies to provide high-quality translation on demand. You can use Amazon Translate to translate unstructured text documents or to build applications that work in multiple languages'

    sourceLanguage = 'en'
    targetLanguage = 'de'

    result = translate.translate_text(Text=text, SourceLanguageCode=sourceLanguage, TargetLanguageCode=targetLanguage)
    print('SourceText: ' + text+'\n')
    print('TranslatedText: ' + result.get('TranslatedText')+'\n')
    print('SourceLanguageCode: ' + result.get('SourceLanguageCode') + ' ----> ' + 'TargetLanguageCode: ' + result.get('TargetLanguageCode'))

def translate_file_synchronously(inputfile, outputfile):
    sourceLanguage = 'en'
    targetLanguage = 'fr'

    if outputfile is None or outputfile == '':
        outputfile = inputfile + '.translated'

    # read text fromf file
    with open(inputfile, 'rt', encoding='utf-8') as fileObject:
        textString = fileObject.read()

    # invoke translation API
    translate = boto3.client(service_name='translate', use_ssl=True)
    result = translate.translate_text(Text=textString, SourceLanguageCode=sourceLanguage, TargetLanguageCode=targetLanguage)
    outputText = result.get('TranslatedText')

    # write out translated text
    with open(outputfile, 'wt', encoding='utf-8') as fileObject:
        fileObject.write(outputText)
    print('Please take a look at the output file {} to consult the translated text:'.format(outputText))


def translate_file_asynchronously(job_config_file):
    
    f = open(job_config_file)
    job_config = json.load(f)
    print(job_config)
    response = translate.start_text_translation_job(
        JobName=job_config['job_name'],
        InputDataConfig={
            'S3Uri': job_config['input_data_s3_uri'],
            'ContentType': job_config['content_type']
        },
        OutputDataConfig={
            'S3Uri': job_config['output_data_s3_uri'],
        },
        DataAccessRoleArn=job_config['data_access_role'],
        SourceLanguageCode=job_config['source_language'],
        TargetLanguageCodes=[job_config['target_language']]
    )

def main(argv):
    inputfile = ''
    outputfile = ''
    mode = ''
    configfile = ''

    opts, args = getopt.getopt(argv,"lsafh",["input_file=","output_file=","config_file="])
    
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -lsa -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt == "-l":
            mode = "list"
            list_languages()
            sys.exit()
        elif opt == "-s":
            mode = "sync"
        elif opt == "-f":
            mode = "sync_file"
        elif opt == "-a":
            mode = "async"
        elif opt in ("-i", "--input_file"):
            inputfile = arg
        elif opt in ("-o", "--output_file"):
            outputfile = arg
        elif opt in ("-c", "--config_file"):
            configfile = arg
   
    if mode == 'sync':
        translate_text_synchronously()
    elif mode == 'sync_file':
        if inputfile == '' or inputfile == None:
            print('Input file is mandatory for file mode')
            sys.exit()
        translate_file_synchronously(inputfile, outputfile)
    elif mode == 'async':
        if configfile == '' or configfile == None:
            print('Config file is mandatory for file mode')
        else:
            translate_file_asynchronously(configfile)
if __name__ == "__main__":
   main(sys.argv[1:])