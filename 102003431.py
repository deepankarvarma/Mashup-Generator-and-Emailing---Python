import smtplib
import sys
import smtplib
import requests
import re
import os
from pytube import YouTube
from moviepy.editor import *
from moviepy.audio.io import AudioFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from pathlib import Path


def get_links(query):
    query = query.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(url)
    html = response.text
    links = re.findall('"/watch\?v=(.{11})"', html)
    return [f"https://www.youtube.com/watch?v={link}" for link in links]


def downloading_videos(link, folder):
    yt = YouTube(link)
    stream = yt.streams.first()
    stream.download(folder)
    print("Video downloaded successfully")

def to_audio(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".3gpp"):
            video = VideoFileClip(os.path.join(folder, filename))
            audio = video.audio
            audio.write_audiofile(os.path.join(folder, filename.split(".")[0] + ".mp3"))
            print("Converted {} to audio successfully".format(filename))

def trim_audio(folder, seconds):
    for audio_file in os.listdir(folder):
        if audio_file.endswith(".mp3"):
            audio_path = os.path.join(folder, audio_file)
            cut_audio_path = os.path.join(folder, audio_file)
        # Load the audio file
            audio = AudioFileClip(audio_path)

        # Cut the audio to the specified duration
            #cut_audio = audio.subclip(seconds, audio.duration)
            cut_audio = audio.subclip(0,seconds)

        # Save the cut audio to a file
            cut_audio.write_audiofile(cut_audio_path)
            
def joining_audio_files(folder, output_filename):
    audio_clips = []
    for filename in os.listdir(folder):
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            audio_clips.append(AudioFileClip(os.path.join(folder, filename)))
    final_audio = concatenate_audioclips(audio_clips)
    final_audio.write_audiofile(output_filename)
    print("Merged all audio files in the folder successfully")
    return output_filename



def folderz(folder,links):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for link in links:
        downloading_videos(link, folder)


def main():


    if len(sys.argv)!=5:
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python 102003431.py <singer-name> <seconds> <number-of-songs> result.mp3 ")
        exit(1)
    # if st.button("Submit"):
    singer=sys.argv[1]
    seconds=sys.argv[2]
    seconds=int(seconds)
    num=sys.argv[3]
    folder="videos"
    num=int(num)
    links= get_links(singer)[:num]
    folderz(folder,links)
    to_audio(folder)
    trim_audio(folder, seconds)
    sys.argv[4]=joining_audio_files(folder, sys.argv[4])
    
    message=MIMEMultipart()
    message["from"]="Your Name"
    message["to"]="Your email"
    message["subject"]="This is a test"
    message.attach(MIMEText("Body"))
    message.attach(MIMEAudio(Path(os.path.realpath(sys.argv[4])).read_bytes(),_subtype="mpeg"))
    
    with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login("Your email","Gmail App password")
        smtp.send_message(message)
        print("Sent...")

if __name__ == "__main__":
    main()