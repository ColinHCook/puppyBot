import requests
from twilio.rest import Client
import random
import schedule
import time

# Twilio configuration
twilio_account_sid = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your Twilio SID 
twilio_auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Your Twilio Auth Token 
twilio_phone_number = 'xxxxxxxxxx'  # Your Twilio phone number 
recipient_number = 'xxxxxxxxxx'  # Recipient's phone number

last_sent_quote = ""
quotes = []

def read_quotes():
    with open('quotes.txt', 'r') as file:
        quotes = file.readlines()
        return [quote.strip() for quote in quotes]
    
# Function to fetch a puppy image using The Dog API
def fetch_puppy_image():
    url = "https://api.thedogapi.com/v1/images/search?mime_types=jpg,png"
    headers = {
        "x-api-key": "insert the dog api key here"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        image_url = response.json()[0]['url']
        return image_url
    else:
        return "No image available right now."

# Twilio client
client = Client(twilio_account_sid, twilio_auth_token)

# Function to send message
def send_message():
    global last_sent_quote  # Ensure you're using the global variable
    quotes = read_quotes()
    if quotes:
        print("Quotes loaded successfully:", quotes)
        puppy_image = fetch_puppy_image()
        
        # Choose a random quote from the loaded quotes
        random_quote = random.choice(quotes)
        while random_quote == last_sent_quote:
            random_quote = random.choice(quotes)
        last_sent_quote = random_quote

        message_body = f"Good morning (name)! I love you so much: \n\n{random_quote}"

        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=recipient_number,
            media_url=puppy_image  # Attach image directly in the message
        )
        print(f"Message sent! SID: {message.sid}")
    else:
        print("No quotes available.")


send_message()


# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
