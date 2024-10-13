import youtube_dl

def download_video(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/home/minisforum/Descargas/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    download_video("https://youtu.be/dQw4w9WgXcQ?si=4s75wOveeO2g39Ic")  # Cambia por el enlace que desees
