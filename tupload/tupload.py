#!/usr/bin/env python

import telepot
import time
import os
import sys
import argparse

try:
    import configparser
except:
    from six.moves import configparser


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Telegram bot to fetch files from the client')

    parser.add_argument(
        '-d',
        '--directory',
        help="directory to store files in",
        default='.')

    return parser


def get_config():
    conf = configparser.SafeConfigParser()

    home = os.path.expanduser('~')
    folder_name = '.tupload'
    folder_path = os.path.join(home, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = 'tupload.ini'
    half_path = os.path.join(folder_name, file_name)
    file_path = os.path.join(home, half_path)
    user_path = os.path.join('~', half_path)

    if not os.path.isfile(file_path):
        print('writing raw config file to ' + user_path)
        conf.add_section('tupload')
        conf.set('tupload', 'token', '')
        conf.set('tupload', 'allowed_ids', '')

        with open(file_path, 'w') as configfile:
            conf.write(configfile)

    conf.read(file_path)
    token = conf.get('tupload', 'token')
    allowed = conf.get('tupload', 'allowed_ids')

    if token == '':
        print('edit ' + user_path + ' to include your telegram token')
        sys.exit(1)

    allowed = allowed.replace(' ', '')
    allowed = allowed.split(',')

    return token, allowed


def handle(msg):
    chat_id = msg['chat']['id']
    id_known = allowed == [''] or str(chat_id) in allowed

    downloadable = ['document', 'photo', 'video', 'audio', 'voice']
    ignore = ['chat', 'date', 'from', 'message_id']

    for item in list(msg):
        if not item in ignore:
            msg_type = item
            break

    if msg_type == 'text':
        result = msg['text']
        if id_known:
            bot.sendChatAction(chat_id, 'typing')
            if result == '/start':
                bot.sendMessage(chat_id, 'tupload is online')
            else:
                bot.sendMessage(chat_id, 'Talk is cheap. Send me the files.')

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

    if id_known and msg_type in downloadable:
        bot.sendChatAction(chat_id, 'typing')
        bot.sendMessage(chat_id, 'Downloading ' + result)
        local_path = os.path.join(local_directory, result)
        bot.download_file(file_id, local_path)

    current_time = time.strftime('[%d %b, %y %r]')
    string = '\n' + current_time + ': '
    string += str(chat_id) + ' [@' + msg['from']['username'] + ']'

    if not id_known:
        string += ' (unrecognized id)'

    string += ':\n' + msg_type + ': ' + result
    print(string)


def command_line():
    global local_directory
    global bot
    global allowed

    args = get_arguments()
    parsed_args = args.parse_args()
    local_directory = parsed_args.directory

    if os.path.exists(local_directory):
        token, allowed = get_config()

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
