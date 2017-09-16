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
    chat_id = msg['chat']['id']

    if 'document' in msg:
        bot.sendChatAction(chat_id, 'typing')
        file_name = msg['document']['file_name']
        file_id = msg['document']['file_id']

        bot.sendMessage(chat_id, 'Downloading ' + file_name)
        local_path = os.path.join(local_directory, file_name)
        bot.download_file(file_id, local_path)

    else:
        bot.sendChatAction(chat_id, 'typing')
        bot.sendMessage(chat_id, "Talk is cheap. Send me the files.")

    print('')
    print(time.strftime('[%d %b, %y %r] ' + str(chat_id)) + ' : ' + str(file_name))


def command_line():
    args = get_arguments()
    parsed_args = args.parse_args()
    global local_directory
    local_directory = parsed_args.directory

    if os.path.exists(local_directory):
        environ_token = os.environ.get('TELEGRAM_TOKEN')

        if environ_token is not None:
            token = environ_token

        global bot
        bot = telepot.Bot(token)
        bot.message_loop(handle)
        print('Bot is ready to receive files...')

        while True:
            time.sleep(10)

    else:
        print(args.print_help())
        print('The expected directory path does not exist')


if __name__ == '__main__':

    command_line()
