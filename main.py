import os
from dotenv import load_dotenv
from bot_logic import process_chat

# Force Python to read the .env file immediately
load_dotenv()

def start_bot():
    print("\n=======================================================")
    print("🗳️ Welcome to the Voter-Ready Bot!")
    print("Did you know? The first Indian election took 4 months to complete.")
    print("Today, the power is in your hands in seconds.")
    print("=======================================================\n")
    
    print("Bot: Let's make sure you are legal to vote. Do you currently have your Voter ID (EPIC card)?")
    print("(Type 'exit' at any time to quit)\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower().strip() in ['exit', 'quit']:
            print("Bot: Thanks for preparing to vote. See you at the polling booth!")
            break
            
        # Send the user's message to our logic handler
        response = process_chat(user_input)
        print(f"\nBot: {response}\n")

if __name__ == "__main__":
    start_bot()