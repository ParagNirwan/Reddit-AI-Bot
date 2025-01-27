import os
from dotenv import load_dotenv
from groq import Groq, GroqError
import praw
import logging

# Setup logging
logging.basicConfig(
    filename='reddit_bot.log',
    level=logging.DEBUG,  # Set to DEBUG to capture all messages, adjust as needed
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Load environment variables
def loadKey():
    try:
        load_dotenv(dotenv_path=".env")
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logging.error("GROQ_API_KEY not found in .env file.")
        return api_key
    except Exception as e:
        logging.error(f"Error loading environment variables: {e}")
        raise

def generate_reddit_post():
    try:
        logging.info("Starting Reddit post generation.")
        
        # Initialize the Groq client
        client = Groq(api_key=loadKey())

        # Define the chat messages
        messages = [
            {
                "role": "user",
                "content": "Generate a short engaging post for Reddit about a random topic with a title and subreddit name and give me in dictionary format not a string. It should not be NSFW content.The keys should be title, subreddit and post. dont give me r/ in subreddit name",
            }
        ]

        # Attempt to get chat completion
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile"
        )

        # Extract and validate the content
        response_content = chat_completion.choices[0].message.content
        logging.info("Reddit post generated successfully.")
        
        print("Content to be posted: ", response_content)
        return response_content

    except GroqError as e:
        logging.error(f"Failed to generate a response from Groq: {e}")
        raise RuntimeError(f"Failed to generate a response from Groq: {e}")
    except (KeyError, IndexError, AttributeError) as e:
        logging.error(f"Unexpected response format from Groq API: {e}")
        raise ValueError("Unexpected response format from Groq API.")
    except Exception as e:
        logging.error(f"An error occurred in generate_reddit_post: {e}")
        raise RuntimeError(f"An error occurred: {e}")

def generateComments(top_post):
    try:
        logging.info(f"Starting comment generation for the top post in {top_post}.")

        # Initialize the Groq client
        client = Groq(api_key=loadKey())

        # Define the chat messages
        messages = [
            {
                "role": "user",
                "content": f"Generate a comment for the top post in the subreddit {top_post}.",
            }
        ]

        # Attempt to get chat completion
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile"
        )

        # Extract and validate the content
        response_content = chat_completion.choices[0].message.content
        logging.info(f"Comment generated for the top post in {top_post}.")
        
        print("Comment to be posted: ", response_content)
        return response_content

    except GroqError as e:
        logging.error(f"Failed to generate a response from Groq for {top_post}: {e}")
        raise RuntimeError(f"Failed to generate a response from Groq: {e}")
    except Exception as e:
        logging.error(f"An error occurred in generateComments for {top_post}: {e}")
        raise RuntimeError(f"An error occurred: {e}")
