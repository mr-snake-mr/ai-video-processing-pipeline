import yt_dlp

def download_youtube_video(url):
    print("Starting download...")

    ydl_opts = {
        # Force best 16:9 MP4
        'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
        
        # Save as horizontal_input.mp4
        'outtmpl': 'horizontal_input.%(ext)s',

        # Merge video + audio
        'merge_output_format': 'mp4',

        # Quiet output (optional)
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Download complete!")

if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ")
    download_youtube_video(video_url)