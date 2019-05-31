import os
import subprocess
from pytube import YouTube
from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from textblob import TextBlob


#Specify path to store transcript file
path = "Path to store transcript file"

#Specify path to Google Application Ccredentials File
credential_path = "path to Google Application Credentials File"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


#Download video
def video_download(url):
	yt = YouTube(url).streams.first().download(path)


#Convert video to .flac format with mono channel
def video_convert():
	mylist = os.listdir(path)
	for filename in mylist:
		if "flac" not in filename:
			f = os.path.splitext(filename)[0]
			fin = f + ".mp4"
			fout = f + ".flac"
			os.chdir(path)
			subprocess.call(['ffmpeg', '-i', fin, '-c:a', 'flac', fout])
			subprocess.call(['ffmpeg', '-i', fout,'-ac', '1', f+"_mono.flac"])
			os.remove(fin)
	return f+"_mono.flac"


#Upload file to Google Storage Bucket
def upload_file(bucket_name,filename, bucket_filename):
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(bucket_filename)
	blob.upload_from_filename(filename)


#Call Google Speech-to-Text API and perform conversion
def audio_to_text(bucket_name, filename):
	client = speech.SpeechClient()
	gcs_uri = "gs://"+bucket_name + "/" + filename
	audio = types.RecognitionAudio(uri=gcs_uri)
	config = types.RecognitionConfig(
		encoding=enums.RecognitionConfig.AudioEncoding.FLAC,  #LINEAR16
		    #sample_rate_hertz=48000,
		language_code='en-US')

	# Detects speech in the audio file
	operation = client.long_running_recognize(config, audio)
	response = operation.result(timeout=90)

	#print transcript
	transcript = ""
	for result in response.results:
		transcript += result.alternatives[0].transcript

	return transcript


#Get Sentiment Analysis
def sentiment_analysis():
	with open('transcript_input.txt', 'r') as transcript_file:
		lines = transcript_file.readlines()
		sentiment = TextBlob(lines[0])
		pol = sentiment.sentiment.polarity
		if pol > 0:
			sent = 'Positive'
		elif pol < 0:
			sent = 'Negative'
		else:
			sent = 'Neutral'
	
	transcript_file.close()
	print("Polarity = "+ str(pol))
	return sent


#Download video from given url
url = input("Enter the url: ")
print("Video Download Begins...")
video_download(url)
print ("Video Downloaded!")

#Convert to flac format with mono channel
audio_file = video_convert()
print ("Conversion complete!!")


#Upload file to Google Storage Bucket
bucket_name = "videos_upload"
upload_file(bucket_name,path+audio_file,audio_file)
print ("Video Uploaded!")

#Convert audio to text
print("Speech-to-Text Conversion Begins...")
transcript = audio_to_text(bucket_name, audio_file)
print ("Conversion complete!")

#Prints the transcript
print("\nTranscript:\n")
print(transcript)

#Stores the transcript into a file
with open('transcript_input.txt', 'w') as transcript_file:
	transcript_file.write(transcript)
transcript_file.close


#Sentiment of transcript
sentiment_value = sentiment_analysis()
print("Sentiment Analysis: "+ str(sentiment_value))

