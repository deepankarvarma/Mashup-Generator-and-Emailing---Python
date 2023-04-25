import smtplib
import sys
import os
import smtplib
import requests
import re
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

from pytube import YouTube
from moviepy.editor import *

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip

def get_links(query):
    query = query.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(url)
    html = response.text
    links = re.findall('"/watch\?v=(.{11})"', html)
    return [f"https://www.youtube.com/watch?v={link}" for link in links]

def download_video(link, folder):
    yt = YouTube(link)
    stream = yt.streams.first()
    stream.download(folder)
    print("Video Downloaded")
    
def convert_to_audio(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".3gpp"):
            video = VideoFileClip(os.path.join(folder, filename))
            audio = video.audio
            audio.write_audiofile(os.path.join(folder, filename.split(".")[0] + ".mp3"))
            print("Converted {} file to audio successfully".format(filename))
            
def cutting_audio(folder, seconds):
    for audio_file in os.listdir(folder):
        if audio_file.endswith(".mp3"):
            audio_path = os.path.join(folder, audio_file)
            cut_audio_path = os.path.join(folder, audio_file)
            audio = AudioFileClip(audio_path)
            cutting_audio = audio.subclip(0,seconds)
            cutting_audio.write_audiofile(cut_audio_path)
            
def merge_audio(folder, output_filename):
    audio_clips = []
    for filename in os.listdir(folder):
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            audio_clips.append(AudioFileClip(os.path.join(folder, filename)))
    final_audio = concatenate_audioclips(audio_clips)
    final_audio.write_audiofile(output_filename)
    print("Merge Successful")
    return output_filename

def folder1(folder,links):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for link in links:
        download_video(link, folder)

def main():
    if len(sys.argv)!=5:
        print("ERROR : PARAMETERS")
        print("USAGE : python mashupwithoutemail.py <singer-name> <seconds> <number-of-songs> result.mp3")
        exit(1)
    singer=sys.argv[1]
    seconds=sys.argv[2]
    seconds=int(seconds)
    num=sys.argv[3]
    num=int(num)
    folder="vid"
    links= get_links(singer)[:num]
    folder1(folder,links)
    convert_to_audio(folder)
    cutting_audio(folder, seconds)
    sys.argv[4]=merge_audio(folder, sys.argv[4])

if _name_ == "_main_":
    main()