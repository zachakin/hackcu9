import yt_dlp
import requests
import openai
from keys import MY_API_KEY

def link_to_file(url, file_path):
    options = {
        "format": "bestaudio/best",
        "outtmpl": file_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "96"
        }],
    }
    ydl = yt_dlp.YoutubeDL(options)
    try:
        ydl.download([url])
    except:
        print("issue downloading file")
        return False
    return True

def file_to_text(filename):

    openai.api_key = MY_API_KEY

    with open(filename, 'rb') as f:
        transcript = openai.Audio.transcribe("whisper-1", f)

    return transcript['text']

def chatbot(messages):
    openai.api_key = MY_API_KEY

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content
    # print(f'ChatGPT: {chat_response}')
    messages.append({"role": "assistant", "content": chat_response})

    return messages