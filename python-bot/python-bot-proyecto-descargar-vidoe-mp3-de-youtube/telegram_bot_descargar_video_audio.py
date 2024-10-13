import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import yt_dlp

# Configuración inicial
DOWNLOAD_PATH = '/ruta/donde/se/descarga/'  # Ruta donde se guardarán los archivos descargados
BOT_TOKEN = 'EL_TOKEN_DEL_BOT'  # Cambia 'YOUR_BOT_TOKEN' por el token de tu bot


# Función para manejar el comando /start
async def start(update: Update, context):
    await update.message.reply_text("¡Hola! Bienvenido al bot. Compárteme tu enlace de Youtube. Y elige descargar audio o vídeo. Si ocupa menos de 20MB, te lo envío.")

async def info(update: Update, context):
    await update.message.reply_text("¡Tan solo admito enlaces de youtube.com, y de youtu.be! ¡Máximo 20MB cada Audio o Vídeo!")


# Función para limpiar el enlace de YouTube
def limpiar_enlace(url):
    # Convertir el enlace largo de YouTube en su versión corta si es necesario
    if 'youtube.com/watch?v=' in url:
        url = url.split('&')[0]  # Limpiar el enlace con parámetros adicionales
    return url

# Función para manejar el mensaje con el enlace de YouTube
async def link_handler(update: Update, context):
    video_url = update.message.text
    print(f"Enlace recibido: {video_url}")
    
    # Limpiar el enlace para procesarlo
    video_url = limpiar_enlace(video_url)
    print(f"Enlace procesado: {video_url}")
    
    # Verificar si el enlace es de YouTube
    if 'youtube.com' in video_url or 'youtu.be' in video_url:
        keyboard = [
            [
                InlineKeyboardButton("Descargar Audio (MP3)", callback_data=f"audio|{video_url}"),
                InlineKeyboardButton("Descargar Video (MP4)", callback_data=f"video|{video_url}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('¿Cómo te gustaría descargar el archivo?', reply_markup=reply_markup)
    else:
        await update.message.reply_text('Por favor, envía un enlace válido de YouTube.')

# Función para manejar la elección de formato (audio o video)
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    # Extraer el formato y el enlace desde el callback_data
    choice, video_url = query.data.split('|')
    
    if choice == 'audio':
        await query.edit_message_text(text="Descargando audio...")
        await download_audio(query, video_url)
    elif choice == 'video':
        await query.edit_message_text(text="Descargando video...")
        await download_video(query, video_url)

# Función para descargar audio (mp3)
async def download_audio(query, video_url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_title = info_dict.get('title', None)
            file_path = f"{DOWNLOAD_PATH}{file_title}.mp3"
            
            # Enviar el archivo de audio descargado
            with open(file_path, 'rb') as audio_file:
                await query.message.reply_document(document=audio_file, filename=f"{file_title}.mp3")
    
    except Exception as e:
        await query.message.reply_text(f"Ocurrió un error al descargar el audio: {str(e)}")
        print(f"Ocurrió un error al descargar el audio: {e}")

# Función para descargar video (mp4)
async def download_video(query, video_url):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_title = info_dict.get('title', None)
            file_path = f"{DOWNLOAD_PATH}{file_title}.mp4"
            
            # Enviar el archivo de video descargado
            with open(file_path, 'rb') as video_file:
                await query.message.reply_document(document=video_file, filename=f"{file_title}.mp4")
    
    except Exception as e:
        await query.message.reply_text(f"Ocurrió un error al descargar el video: {str(e)}")
        print(f"Ocurrió un error al descargar el video: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Manejador del comando /start
    application.add_handler(CommandHandler("start", start))

    # Manejador del comando /info
    application.add_handler(CommandHandler("info", info))

    # Manejador de mensajes con enlaces
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_handler))
    
    # Manejador de botones
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Bot iniciado.")
    application.run_polling()
