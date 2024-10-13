import yt_dlp as youtube_dl
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

async def download_video(update: Update, video_url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/home/minisforum/Descargas/%(title)s.%(ext)s',  # Cambia esto a tu ruta de descarga
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print(f"Descargando: {video_url}")
            await update.message.reply_text(f"Descargando: {video_url}...")  # Mensaje de progreso
            ydl.download([video_url])
            await update.message.reply_text("Descarga completa.")
    except Exception as e:
        await update.message.reply_text(f"Ocurrió un error: {str(e)}")
        print(f"Ocurrió un error: {e}")

async def link_handler(update: Update, context):
    video_url = update.message.text
    print(f"Enlace recibido: {video_url}")
    await download_video(update, video_url)

if __name__ == '__main__':
    application = ApplicationBuilder().token('7640110713:AAFQsHCkW0lGZa8W830OSrWIfq-bGWqoQXw').build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_handler))
    print("Bot iniciado.")
    application.run_polling()
