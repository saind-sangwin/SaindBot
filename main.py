import os
import telebot
import speech_recognition
import emoji
from pydub import AudioSegment
from PIL import Image
from telebot import types

# Пример: token = '2007628239:AAEF4ZVqLiRKG7j49EC4vaRwXjJ6DN6xng8'
tokenFile = open('token.txt')  # <<< Ваш токен
token = tokenFile.readline()
tokenFile.close()

bot = telebot.TeleBot(token)


def transform_image(filename):
    source_image = Image.open(filename)
    enhanced_image = source_image.convert('RGB')
    enhanced_image.save(filename)
    return filename


def oga2wav(filename):
    # Конвертация формата файлов
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):
    # Перевод голоса в текст + удаление использованных файлов
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    text = recognizer.recognize_google(wav_audio, language='ru')

    return text


def download_file(tele_bot, file_id):
    # Скачивание файла, который прислал пользователь
    file_info = tele_bot.get_file(file_id)
    downloaded_file = tele_bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


def compress_photo(input_path, compression_factor):
    image = Image.open(input_path)
    compressed_image = image.resize(
        (int(image.width // compression_factor), int(image.height // compression_factor)))
    output_path = 'compressed_photo.jpg'  # Replace with the desired output image path
    compressed_image.save(output_path)
    return output_path


def create_compress_button():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Сжать изображение", callback_data='compress')
    keyboard.add(button)
    return keyboard


@bot.message_handler(commands=['start'])
def say_hi(message):
    # Функция, отправляющая "Привет" в ответ на команду /start
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    try:
        text = recognize_speech(filename)
        bot.send_message(message.chat.id, text)
    except:
        text = '_Не удалось распознать голос в аудио-сообщении_'
        bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    # Функция, отправляющая стикер в ответ на команду
    try:
        sticker = open('stickers/2.webp', 'rb')
        bot.send_sticker(message.chat.id, sticker)
        sticker.close()
    except:
        text = '_Я не нашёл для тебя подходящего стикера, попробуй позже _' + emoji.emojize(":winking_face:")
        bot.send_message(message.chat.id, text, parse_mode="Markdown")


compression_requests = {}


@bot.message_handler(content_types=['photo'])
def resend_photo(message):
    # Функция отправки обработанного изображения
    file_id = message.photo[-1].file_id
    filename = download_file(bot, file_id)
    print(filename)

    # Трансформируем изображение
    transform_image(filename)

    image = open(filename, 'rb')
    bot.send_photo(message.chat.id, image, reply_markup=create_compress_button())
    image.close()

    if os.path.exists(filename):
        os.remove(filename)


@bot.callback_query_handler(func=lambda call: call.data == 'compress')
def compress_image(call):
    chat_id = call.message.chat.id
    compression_requests[chat_id] = True
    bot.register_next_step_handler(call.message, handle_compression, call.message.photo[-1].file_id)
    bot.send_message(chat_id,
                     "Во сколько раз сжать изображение? Введите целое положительное число или /cancel для отмены.")


def handle_compression(message, file_id):
    chat_id = message.chat.id

    if message.text == '/cancel':
        if chat_id in compression_requests:
            del compression_requests[chat_id]
            bot.send_message(chat_id, "Сжатие изображения отменено.")
        else:
            bot.send_message(chat_id, "Нет активных запросов на сжатие изображения.")
        return

    if not message.text.isdigit():
        bot.send_message(chat_id, "Пожалуйста, введите целое положительное число или /cancel для отмены.")
        return

    compression_factor = int(message.text)
    if compression_factor <= 0:
        bot.send_message(chat_id, "Пожалуйста, введите положительное число или /cancel для отмены.")
        return

    filename = download_file(bot, file_id)
    image = open(filename, 'rb')
    compressed_image = compress_photo(image, compression_factor)
    image.close()

    # Отправляем сжатое изображение
    with open(compressed_image, 'rb') as file_id:
        bot.send_photo(chat_id, file_id)

    # Удаляем сжатое изображение с сервера
    if os.path.exists(filename):
        os.remove(filename)

    if os.path.exists(compressed_image):
        os.remove(compressed_image)

    # Удаляем завершенный запрос из compression_requests
    del compression_requests[chat_id]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Запускаем бота. Он будет работать до тех пор, пока работает ячейка (крутится значок слева).
    # Остановим ячейку - остановится бот
    bot.polling()
