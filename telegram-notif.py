#!/usr/bin/python3
import requests
from sys import argv
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('TG_TOKEN')
if not BOT_TOKEN:
    print("TELGRAM_BOT_TOKEN is not in .env file")
    exit(1)

TG_URL = os.getenv('TG_URL', 'api.telegram.org')

API_URL = f"https://{TG_URL}/bot{BOT_TOKEN}/sendMessage"

def split_message(text, max_length=4096):
    """Split message into chunks of max_length characters"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break
        
        split_point = text.rfind(' ', 0, max_length)
        if split_point == -1:
            split_point = max_length
        
        chunks.append(text[:split_point])
        text = text[split_point:].lstrip()
    
    return chunks

if len(argv) < 3:
    print("Usage: send_telegram <chat_id> <message>")
    exit(1)


chat_id = argv[1]
message = argv[2]

message_chunks = split_message(message)

for chunk in message_chunks:
    payload = {
        "chat_id": chat_id,
        "text": chunk,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        if len(message_chunks) > 1:
            print(f"Chunk sent successfully ({len(chunk)} characters)")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message chunk: {e}")
        exit(1)

print("All messages sent successfully.")