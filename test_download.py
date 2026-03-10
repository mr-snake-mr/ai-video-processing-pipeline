import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'test_video.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    download_video(url)