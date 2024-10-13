#!/bin/python
# Bot telegram @Proyecto_ASIR_Ruben_bot

import time
import os
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop

def action(msg):
   message = "Bienvenid@"

   chat_id = msg['chat']['id']
   cmd = msg['text']
   print ('Recibido: %s' % cmd)

# Mensaje inicio
   if 'start' in cmd:
      message = "Bienvenid@ al bot de Ruben en IES Serpis, para el proyecto de control de servicios en Raspberry Pi. \n\n Usa /help para dudas! \n\n Usa /habilitados para ver disponibles! \n\n Gracias por utilizar nuestro servicio! \n Usa /start para volver!"
      telegram_bot.sendMessage (chat_id, message)

# Mensaje ayuda
   if 'help' in cmd:
      message = "Opciones disponibles (en minuscula): \n on [servicio] \n off [servicio] \n on all \n off all \n /start \n /help \n /habilitados  \n\n Ejemplo de uso: \n Enviar: on cups \n Recibir: on cups service \n\n Usa /start para volver!"
      telegram_bot.sendMessage (chat_id, message)

# Servicios disponibles
   if 'habilitados' in cmd:
      #activos = os.system('sh /etc/servicios-con-LED.sh')
      #message = " Servicios disponibles: \n\n  " + activos
      message = "Servicios disponibles / habilitados: \n\n cups \n ssh \n smbd \n asterisk \n apache2 \n\n Usa /start para volver!"
      telegram_bot.sendMessage (chat_id, message)

# Enciende el servicio
   if 'on' in cmd:
      message = "on "
      if 'cups' in cmd:
         message = message + "cups "
         os.system('sudo systemctl start cups')

      if 'ssh' in cmd:
         message = message + "ssh "
         os.system('sudo systemctl start ssh')

      if 'smbd' in cmd:
         message = message + "smbd "
         os.system('sudo systemctl start smbd')

      if 'asterisk' in cmd:
         message = message + "asterisk "
         os.system('sudo systemctl start asterisk')

      if 'apache2' in cmd:
         message = message + "apache2 "
         os.system('sudo systemctl start apache2')

      if 'all' in cmd:
         os.system('sudo systemctl start cups')
         os.system('sudo systemctl start ssh')
         os.system('sudo systemctl start smbd')
         os.system('sudo systemctl start asterisk')
         os.system('sudo systemctl start apache2')
         message = message + "cups, ssh, smbd, asterisk y apache2 "

      message = message + "service"
      telegram_bot.sendMessage (chat_id, message)

# Apaga el servicio
   if 'off' in cmd:
      message = "off "
      if 'cups' in cmd:
         message = message + "cups "
         os.system('sudo systemctl stop cups')

      if 'ssh' in cmd:
         message = message + "ssh "
         os.system('sudo systemctl stop ssh')

      if 'smbd' in cmd:
         message = message + "smbd "
         os.system('sudo systemctl stop smbd')

      if 'asterisk' in cmd:
         message = message + "asterisk "
         os.system('sudo systemctl stop asterisk')

      if 'apache2' in cmd:
         message = message + "apache2 "
         os.system('sudo systemctl stop apache2')

      if 'all' in cmd:
         os.system('sudo systemctl stop cups')
         os.system('sudo systemctl stop ssh')
         os.system('sudo systemctl stop smbd')
         os.system('sudo systemctl stop asterisk')
         os.system('sudo systemctl stop apache2')
         message = message + "cups, ssh, smbd, asterisk y apache2 "

      message = message + "service"
      telegram_bot.sendMessage (chat_id, message)


telegram_bot = telepot.Bot('1747202663:AAHuywvDSUHV51shJ8bq0bd40LkGEbzDf3I')
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print ('Tamo ready....')

while 1:
   time.sleep(1)
