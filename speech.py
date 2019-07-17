from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

client = speech_v1.SpeechClient.from_service_account_json('C:/Users/artur/Desktop/key.json')

encoding = enums.RecognitionConfig.AudioEncoding.FLAC
sample_rate_hertz = 16000
language_code = 'en-US'
config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code}
uri = "gs://cloud-samples-tests/speech/brooklyn.flac"
audio = {'uri': uri}

response = client.recognize(config, audio)
print(response)
