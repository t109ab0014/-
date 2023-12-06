# -*- coding: utf-8 -*-


#@markdown # **Install libraries** 🏗️
#@markdown This cell will take a little while to download several libraries, including Faster Whisper.

#@markdown ---
#! pip install faster-whisper
#! pip install yt-dlp


import sys
import warnings 
from faster_whisper import WhisperModel
from pathlib import Path
import yt_dlp
import subprocess
import torch
import shutil
import numpy as np
#from IPython.display import display, Markdown, YouTubeVideo

device = torch.device('mps')
print('Using device:', device, file=sys.stderr)

#@markdown # **Optional:** Save data in Google Drive 💾
#@markdown Enter a Google Drive path and run this cell if you want to store the results inside Google Drive.

# Uncomment to copy generated images to drive, faster than downloading directly from colab in my experience.
# from google.colab import drive (Removed for local execution)
drive_mount_path = Path("/") # Modified for local execution #@param {type:"string"}
# drive.mount(str(drive_mount_path)) (Removed for local execution)
# drive_mount_path /= "My Drive" (Removed for local execution)
#@markdown ---
drive_path = "/Users/ro9air/VScode/static/testwav2/國立臺北科技大學.wav" # Modified for local execution #@param {type:"string"}
#@markdown ---
#@markdown **Run this cell again if you change your Google Drive path.**

drive_whisper_path = Path("/Users/ro9air/VScode/static/testwav2/output")
drive_whisper_path.mkdir(parents=True, exist_ok=True)

#@markdown # **Model selection** 🧠

#@markdown As of the first public release, there are 4 pre-trained options to play with:

#@markdown |  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
#@markdown |:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
#@markdown |  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~0.8 GB     |      ~32x      |
#@markdown |  base  |    74 M    |     `base.en`      |       `base`       |     ~1.0 GB     |      ~16x      |
#@markdown | small  |   244 M    |     `small.en`     |      `small`       |     ~1.4 GB     |      ~6x       |
#@markdown | medium |   769 M    |    `medium.en`     |      `medium`      |     ~2.7 GB     |      ~2x       |
#@markdown | large-v1  |   1550 M   |        N/A         |      `large-v1`       |    ~4.3 GB     |       1x       |
#@markdown | large-v2  |   1550 M   |        N/A         |      `large-v2`       |    ~4.3 GB     |       1x       |

#@markdown ---
model_size = 'large-v2' #@param ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large-v1', 'large-v2']
device_type = "cpu" #@param {type:"string"} ['cuda', 'cpu']
compute_type = "float32" #@param {type:"string"} ['float16', 'int8_float16', 'int8']
#@markdown ---
#@markdown **Run this cell again if you change the model.**

model = WhisperModel(model_size, device=device_type, compute_type=compute_type)

#@markdown # **Video selection** 📺

#@markdown Enter the URL of the Youtube video you want to transcribe, wether you want to save the audio file in your Google Drive, and run the cell.

Type = "Google Drive" #@param ['Youtube video or playlist', 'Google Drive']
#@markdown ---
#@markdown #### **Youtube video or playlist**
URL = "https://youtu.be/5RF-tOLoTo0" #@param {type:"string"}
# store_audio = True #@param {type:"boolean"}
#@markdown ---
#@markdown #### **Google Drive video, audio (mp4, wav), or folder containing video and/or audio files**
video_path = "/Users/ro9air/VScode/local_fastWhisper/2023-11-30-110244_139328.mp3" #@param {type:"string"}
#@markdown ---
#@markdown **Run this cell again if you change the video.**

#@markdown # **Run the model** 🚀

#@markdown You can change the language, the initial prompt, and the VAD filter parameters.
#@markdown #### 語言
language = "zh" #@param ["auto", "en", "zh", "ja", "fr", "de"] {allow-input: true}



#@markdown #### initial prompt
initial_prompt = "Please do not translate, only transcription be allowed.  Here are some English words you may need: Cindy. And Chinese words: \u7206\u7834" #@param {type:"string"}
#@markdown ---
#@markdown #### Word-level timestamps
word_level_timestamps = False #@param {type:"boolean"}
#@markdown ---
#@markdown #### VAD filter
vad_filter = True #@param {type:"boolean"}
vad_filter_min_silence_duration_ms = 50 #@param {type:"integer"}
#@markdown ---
#@markdown #### Output(Default is srt, txt if `text_only` be checked )
text_only = False #@param {type:"boolean"}

video_path_local_list = []

def seconds_to_time_format(s):
    # Convert seconds to hours, minutes, seconds, and milliseconds
    hours = s // 3600
    s %= 3600
    minutes = s // 60
    s %= 60
    seconds = s // 1
    milliseconds = round((s % 1) * 1000)

    # Return the formatted string
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds):03d}"




if Type == "Youtube video or playlist":

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([URL])
        list_video_info = [ydl.extract_info(URL, download=False)]
    
    if video_info is not None:  
      video_path_local_list.append(Path(f"{video_info['id']}.wav"))

    for video_info in list_video_info:
        video_path_local_list.append(Path(f"{video_info['id']}.wav"))
    


elif Type == "Google Drive":
    # video_path_drive = drive_mount_path / Path(video_path.lstrip("/"))
    video_path = drive_mount_path / Path(video_path.lstrip("/"))
    if video_path.is_dir():
        for video_path_drive in video_path.glob("**/*"):
            if video_path_drive.is_file():
              print(f"**{str(video_path_drive)} selected for transcription.**")
            elif video_path_drive.is_dir():
              print(f"**Subfolders not supported.**")
            else:
              print(f"**{str(video_path_drive)}  does not exist, skipping.**")
            video_path_local = Path(".").resolve() / (video_path_drive.name)
            shutil.copy(video_path_drive, video_path_local)
            video_path_local_list.append(video_path_local)
    elif video_path.is_file():
        video_path_local = Path(".").resolve() / (video_path.name)
        shutil.copy(video_path, video_path_local)
        video_path_local_list.append(video_path_local)
        print(f"**{str(video_path) } selected for transcription.**")
    else:
      print(f"**{str(video_path)} does not exist, skipping.**")

else:
  raise(TypeError("Please select supported input type."))

for video_path_local in video_path_local_list:
    if video_path_local.suffix == ".mp4":
        video_path_local = video_path_local.with_suffix(".wav")
        result  = subprocess.run(["ffmpeg", "-i", str(video_path_local.with_suffix(".mp4")), "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(video_path_local)])
            
    segments, info = model.transcribe(str(video_path_local), beam_size=5,
                                    language=None if language == "auto" else language,
                                    initial_prompt=initial_prompt,
                                    word_timestamps=word_level_timestamps,
                                    vad_filter=vad_filter,
                                    vad_parameters=dict(min_silence_duration_ms=vad_filter_min_silence_duration_ms))
        
    print(f"Detected language '{info.language}' with probability {info.language_probability}")

    ext_name = '.txt' if text_only else ".srt"
    transcript_file_name = video_path_local.stem + ext_name
    sentence_idx = 1
    with open(transcript_file_name, 'w') as f:
        for segment in segments:
            if word_level_timestamps:
                for word in segment.words:
                    ts_start = seconds_to_time_format(word.start)
                    ts_end = seconds_to_time_format(word.end)
                    print(f"[{ts_start} --> {ts_end}] {word.word}")
                    if not text_only:
                        f.write(f"{sentence_idx}\n")
                        f.write(f"{ts_start} --> {ts_end}\n")
                        f.write(f"{word.word}\n\n")
                    else:
                        f.write(f"{word.word}")
                    f.write("\n")
                    sentence_idx = sentence_idx + 1
            else:
                ts_start = seconds_to_time_format(segment.start)
                ts_end = seconds_to_time_format(segment.end)
                print(f"[{ts_start} --> {ts_end}] {segment.text}")
                if not text_only:
                    f.write(f"{sentence_idx}\n")
                    f.write(f"{ts_start} --> {ts_end}\n")
                    f.write(f"{segment.text.strip()}\n\n")
                else:
                    f.write(f"{segment.text.strip()}\n")
                sentence_idx = sentence_idx + 1

    try:
        shutil.copy(video_path_local.parent / transcript_file_name,
                    drive_whisper_path / transcript_file_name
        )
        print(f"**Transcript file created: {drive_whisper_path / transcript_file_name}**")
    except:
        print(f"**Transcript file created: {video_path_local.parent / transcript_file_name}**")