from pytube import YouTube

def yt_video_dl(url,output):
    YouTube(url).streams.get_highest_resolution().download(output)
