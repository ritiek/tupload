#!/usr/bin/env python

import telepot
import time
import os
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Telegram bot to fetch files from the client')

    parser.add_argument(
        '-d',
        '--directory',
        help="directory to store files in",
        default='.')

    return parser


def handle(msg):
    #print(msg)
    chat_id = msg['chat']['id']
    bot.sendChatAction(chat_id, 'typing')

    downloadable = ['document', 'photo', 'video', 'audio', 'voice']
    ignore = ['chat', 'date', 'from', 'message_id']

    for item in list(msg):
        if not item in ignore:
            msg_type = item
            break

    if msg_type == 'text':
        result = msg['text']
        bot.sendMessage(chat_id, "Talk is cheap. Send me the files.")

    elif msg_type == 'document':
        result = msg[msg_type]['file_name']
        file_id = msg[msg_type]['file_id']

    elif msg_type == 'photo':
        result = str(msg['date']) + '.jpg'
        file_id = msg[msg_type][0]['file_id']

    elif msg_type == 'video':
        file_type = msg[msg_type]['mime_type'].split('/')[-1]
        result = str(msg['date']) + '.' + file_type
        file_id = msg[msg_type]['file_id']

    elif msg_type == 'audio':
        file_type = msg[msg_type]['mime_type'].split('/')[-1]
        result = msg['audio']['title'] + '.' + file_type
        file_id = msg[msg_type]['file_id']

    elif msg_type == 'voice':
        file_type = msg[msg_type]['mime_type'].split('/')[-1]
        result = str(msg['date']) + '.' + file_type
        file_id = msg[msg_type]['file_id']

    elif msg_type == 'contact':
        name = msg['contact']['first_name']
        number = msg['contact']['phone_number']
        result = name + ' (' + number + ')'

    elif msg_type == 'location':
        result = '{0}, {1}'
        result = result.format(msg['location']['latitude'], msg['location']['longitude'])

    else:
        result = 'This media type is not currently supported'

    if msg_type in downloadable:
        bot.sendMessage(chat_id, 'Downloading ' + result)
        local_path = os.path.join(local_directory, result)
        bot.download_file(file_id, local_path)

    current_time = time.strftime('[%d %b, %y %r]')
    string = '\n' + current_time + ': '
    string += str(chat_id) + ' (' + msg['from']['username'] + '):'
    string += '\n' + msg_type + ': ' + result
    print(string)


def command_line():
    global local_directory
    global bot

    args = get_arguments()
    parsed_args = args.parse_args()
    local_directory = parsed_args.directory

    if os.path.exists(local_directory):
        environ_token = os.environ.get('TELEGRAM_TOKEN')

        if environ_token is not None:
            token = environ_token

        bot = telepot.Bot(token)
        bot.message_loop(handle)
        print('Bot is online')

        while True:
            time.sleep(10)

    else:
        print(args.print_help())
        print('The expected directory path does not exist')


if __name__ == '__main__':

    command_line()
