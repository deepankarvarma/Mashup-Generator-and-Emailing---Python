# Mashup Generator From Youtube Video And Emailing<br>
This is a command-line tool that helps you to download multiple music videos from YouTube, convert them to audio, trim them to a specified duration, and merge them into a single audio file.<br>
## Getting Started
### Prerequisites
1. Python 3.x <br>
2. Pytube (`pip install pytube`)<br>
3. MoviePy (`pip install moviepy`)<br>
4. Requests (`pip install requests`)<br>
### Installation
1. Clone the repository: `git clone https://github.com/username/repo.git` <br>
2. Change directory to the project: `cd youtube-music-downloader`<br>
3. Install the required dependencies: `pip install -r requirements.txt`<br>
### Usage
Run the following command to start downloading music videos from YouTube: <br>
`python youtube-music-downloader.py <singer-name> <seconds> <number-of-songs> <output-filename>`<br>
singer-name: Name of the singer or band.<br>
seconds: Duration in seconds for the final audio file.<br>
number-of-songs: Number of songs to download and merge.<br>
output-filename: Name of the final audio file.<br><br>
Example: `python youtube-music-downloader.py "Ed Sheeran" 60 5 result.mp3`
<br>
This command will download 5 music videos of Ed Sheeran from YouTube, convert them to audio, trim them to 60 seconds each, merge them into a single audio file, and save it as "result.mp3".
<br>
### Sending Email
The tool also includes an email feature that sends the final audio file to a specified email address. To use this feature, you need to provide your email address and the Gmail App password in the code.
