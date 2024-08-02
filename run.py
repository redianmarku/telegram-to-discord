import asyncio
from telethon.sync import TelegramClient
import discord


class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number, discord_token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.discord_token = discord_token
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)
        intents = discord.Intents.default()
        intents.messages = True
        self.discord_client = discord.Client(intents=intents)

    async def list_chats(self):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        # Get a list of all the dialogs (chats)
        dialogs = await self.client.get_dialogs()
        chats_file = open(f"chats_of_{self.phone_number}.txt", "w")
        # Print information about each chat
        for dialog in dialogs:
            print(f"Chat ID: {dialog.id}, Title: {dialog.title}")
            chats_file.write(f"Chat ID: {dialog.id}, Title: {dialog.title} \n")
          
        print("List of groups printed successfully!")

    async def forward_messages_to_channel(self, source_chat_id, discord_channel_id, keywords):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id

        while True:
            print("Checking for messages and forwarding them...")
            # Get new messages since the last checked message
            messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)

            for message in reversed(messages):
                # Check if the message text includes any of the keywords
                if keywords:
                    if message.text and any(keyword in message.text.lower() for keyword in keywords):
                        print(f"Message contains a keyword: {message.text}")

                        # Send the message to the specified Discord channel
                        channel = await self.discord_client.fetch_channel(discord_channel_id)
                        await channel.send(message.text)

                        print("Message forwarded")
                else:
                    # Send the message to the specified Discord channel

                    channel = await self.discord_client.fetch_channel(discord_channel_id)
                    await channel.send(message.text)

                    print("Message forwarded")

                # Update the last message ID
                last_message_id = max(last_message_id, message.id)

            # Add a delay before checking for new messages again
            await asyncio.sleep(5)  # Adjust the delay time as needed

    async def start_discord_client(self):
        await self.discord_client.start(self.discord_token)

# Function to read credentials from file
def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            if len(lines) < 4:
                raise ValueError("Credentials file is missing some values.")
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
            phone_number = lines[2].strip()
            discord_token = lines[3].strip()
            return api_id, api_hash, phone_number, discord_token
    except FileNotFoundError:
        print("Credentials file not found.")
        return None, None, None, None
    except ValueError as ve:
        print(ve)
        return None, None, None, None


# Function to write credentials to file
def write_credentials(api_id, api_hash, phone_number, discord_token):
    with open("credentials.txt", "w") as file:
        file.write(api_id + "\n")
        file.write(api_hash + "\n")
        file.write(phone_number + "\n")
        file.write(discord_token + "\n")

async def main():
    # Attempt to read credentials from file
    api_id, api_hash, phone_number, discord_token = read_credentials()

    # If credentials not found in file, prompt the user to input them
    if api_id is None or api_hash is None or phone_number is None or discord_token is None:
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API Hash: ")
        phone_number = input("Enter your phone number: ")
        discord_token = input("Enter your Discord bot token: ")
        # Write credentials to file for future use
        write_credentials(api_id, api_hash, phone_number, discord_token)

    forwarder = TelegramForwarder(api_id, api_hash, phone_number, discord_token)

    # Start the Discord client in the background
    discord_task = asyncio.create_task(forwarder.start_discord_client())
    
    while True:  # Keep looping until the user chooses to exit
        print("Choose an option:")
        print("1. List Chats")
        print("2. Forward Messages")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            await forwarder.list_chats()
        elif choice == "2":
            source_chat_id = int(input("Enter the source chat ID: "))
            destination_channel_id = int(input("Enter the destination Discord channel ID: "))
            print("Enter keywords if you want to forward messages with specific keywords, or leave blank to forward every message!")
            keywords = input("Put keywords (comma separated if multiple, or leave blank): ").split(",")
            
            await forwarder.forward_messages_to_channel(source_chat_id, destination_channel_id, keywords)
        elif choice == "3":
            print("Exiting...")
            break  # Exit the loop and end the program
        else:
            print("Invalid choice")

    # Wait for the Discord client task to finish
    await discord_task

# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())
