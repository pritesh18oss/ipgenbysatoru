import requests
import os
from multiprocessing.dummy import Pool
from faker import Faker
import telebot
from telebot import types
from io import BytesIO

TOKEN = '6412344085:AAHQ4iMcfMuwPix3lwmIygb7qpKJaMewW3M'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    bot.reply_to(message, "Welcome to the IP Tools bot!\n\n"
                          "Use the following commands:\n"
                          "/ipgen - Generate random IP addresses\n"
                          "/liveip - Check if IP addresses are live")

@bot.message_handler(commands=['ipgen'])
def send_ipgen_request(message):
    sent_msg = bot.reply_to(message, "How many IP addresses do you want to generate?")
    bot.register_next_step_handler(sent_msg, generate_ip)

def generate_ip(message):
    try:
        num_ip = int(message.text)
        if num_ip > 0:
            ips = []
            faker = Faker()
            for _ in range(num_ip):
                ips.append(faker.ipv4())
            ip_file = open('ip.txt', 'w')
            ip_file.write('\n'.join(ips))
            ip_file.close()

            # Send file to the user
            with open('ip.txt', 'rb') as file:
                bot.send_document(message.chat.id, file)

            # Delete file from local storage
            os.remove('ip.txt')

            bot.reply_to(message, "IP addresses generated successfully!")
        else:
            bot.reply_to(message, "Please enter a valid number of IP addresses.")
    except ValueError:
        bot.reply_to(message, "Invalid input. Please enter a number.")

# @bot.message_handler(commands=['iprange'])
# def send_iprange_request(message):
#     sent_msg = bot.reply_to(message, "Please send the IP list file for range.")
#     bot.register_next_step_handler(sent_msg, range_ip)

# def range_ip(message):
#     try:
#         ip_list = message.document.file_name
#         ip_list_file = bot.get_file(message.document.file_id)
#         ip_list_path = os.path.join('temp', ip_list) # Assuming 'temp' is the directory to store temporary files
        
#         # Download the file
#         ip_list_file.download(ip_list_path)

#         with open(ip_list_path, 'r') as f:
#             ip_addresses = f.read().splitlines()
        
#         # Perform IP range processing
#         ranged_file = open('range.txt', 'w')
#         for ip_address in ip_addresses:
#             parts = ip_address.split('.')
#             start = 0
#             end = 244
#             for j in range(start, end + 1):
#                 for k in range(start, end + 1):
#                     ale = parts[0] + '.' + parts[1] + '.' + str(j) + '.' + str(k)
#                     ranged_file.write(ale + '\n')
#         ranged_file.close()

#         # Send file to the user
#         with open('range.txt', 'rb') as file:
#             bot.send_document(message.chat.id, file)

#         # Delete temporary files
#         os.remove(ip_list_path)
#         os.remove('range.txt')

#         bot.reply_to(message, "IP addresses ranged successfully!")
#     except:
#         bot.reply_to(message, "An error occurred while processing the file.")


@bot.message_handler(commands=['liveip'])
def send_liveip_request(message):
    bot.reply_to(message, "Please send a text file containing the IP addresses.")

@bot.message_handler(content_types=['document'])
def check_liveip(message):
    try:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        ip_list = downloaded_file.decode().splitlines()

        liveip_result = []

        def valid(ip):
            try:
                r = requests.get('http://{}'.format(ip), timeout=3)
                if r.status_code == 200:
                    liveip_result.append(f"LIVE {ip}")
                elif '<title>' in r.text:
                    liveip_result.append(f"LIVE {ip}")
                else:
                    liveip_result.append(f"DEAD {ip}")
            except Exception:
                liveip_result.append(f"DEAD {ip}")

        p = Pool(500)
        p.map(valid, ip_list)
        p.close()
        p.join()

        result_text = '\n'.join(liveip_result)
        
        # Save result_text as a .txt file
        txt_file = BytesIO(result_text.encode('utf-8'))
        txt_file.name = 'liveip_results.txt'

        bot.send_document(message.chat.id, txt_file)
        
    except:
        bot.reply_to(message, "An error occurred while checking the IP addresses.")
bot.polling()