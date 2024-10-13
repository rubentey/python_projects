from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from pytube import YouTube

async def link_handler(update: Update, context):
    video_url = update.message.text
    print(f"Enlace recibido: {video_url}")

    try:
        yt = YouTube(video_url)
        print(f"Formato elegido: audio")
        print(f"Descargando: {yt.title}")

        # Intentar obtener el stream de audio
        stream = yt.streams.filter(only_audio=True).first()
        
        if stream is None:
            print("No se pudo encontrar un stream de audio.")
            await update.message.reply_text("No se pudo encontrar un stream de audio.")
            return

        # Asegúrate de que la ruta de descarga es válida
        output_path = '/home/minisforum/Descargas'  # Cambia esto a tu ruta de descarga
        print(f"Descargando a: {output_path}")
        
        stream.download(output_path=output_path)
        await update.message.reply_text("Descarga completa.")
    except Exception as e:
        await update.message.reply_text(f"Ocurrió un error: {str(e)}")
        print(f"Ocurrió un error: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token('7640110713:AAFQsHCkW0lGZa8W830OSrWIfq-bGWqoQXw').build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_handler))
    print("Bot iniciado.")
    application.run_polling()
