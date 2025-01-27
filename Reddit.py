import os
import praw
import ast
from dotenv import load_dotenv
from ContentGeneration import generateComments
import logging

# Setup logging
logging.basicConfig(
    filename='reddit_bot.log',
    level=logging.DEBUG,  # Set to DEBUG to capture all messages, adjust as needed
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def load_reddit_credentials():
    try:
        load_dotenv(dotenv_path=".env")
        reddit_client_id = os.environ.get("Client_ID")
        reddit_client_secret = os.environ.get("Reddit_API-KEY")
        reddit_username = os.environ.get("rdt_username")
        reddit_password = os.environ.get("rdt_password")

        if not all([reddit_client_id, reddit_client_secret, reddit_username, reddit_password]):
            logging.error("Reddit API credentials not found in environment variables.")
            raise ValueError("Reddit API credentials not found in environment variables.")

        logging.info("Reddit API credentials loaded successfully.")
        return {
            "client_id": reddit_client_id,
            "client_secret": reddit_client_secret,
            "username": reddit_username,
            "password": reddit_password,
        }

    except Exception as e:
        logging.error(f"Error loading Reddit credentials: {e}")
        raise

def create_reddit_instance(credentials):
    try:
        reddit_instance = praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            username=credentials["username"],
            password=credentials["password"],
            user_agent="EngagementBot by Ayushi Lanjewar",
        )
        logging.info("Reddit instance created successfully.")
        return reddit_instance
    except Exception as e:
        logging.error(f"Failed to create Reddit instance: {e}")
        raise

def post_to_reddit(generatedContent):
    try:
        # Parse the engagement post string into a dictionary
        generatedContent = ast.literal_eval(generatedContent)
        
        logging.info("Parsed generated content: %s", generatedContent)

        # Load Reddit API credentials
        credentials = load_reddit_credentials()

        # Create a Reddit instance
        reddit_instance = create_reddit_instance(credentials)

        # Post to a subreddit
        subreddit = reddit_instance.subreddit("testingground4bots")
        post = subreddit.submit(title=generatedContent["title"], selftext=generatedContent["post"])
        
        logging.info(f"Posted to Reddit: {post.url}")
        print("*" * 100)
        print(f"Posted to Reddit: {post.url}\n")
        print("*" * 100)
        return post

    except Exception as e:
        logging.error(f"Error posting to Reddit: {e}")
        return {"error": f"An error occurred: {e}"}

def comment_on_post(subreddit_name):
    try:
        # Load Reddit API credentials
        credentials = load_reddit_credentials()

        # Create a Reddit instance
        reddit = create_reddit_instance(credentials)

        # Get the subreddit
        subreddit = reddit.subreddit(subreddit_name)

        # Fetch the top post (e.g., from 'hot', 'new', or 'top')
        top_post = next(subreddit.new(limit=1))  # Get the top post in the subreddit

        logging.info(f"Top post retrieved: {top_post.title}")
        print("*" * 100)
        print(f"Top post: {top_post.title}")
        print(top_post.selftext)
        print("*" * 100)

        # Send the top post to Groq, analyze it, and generate a comment and post it
        if top_post.selftext:
            comment = generateComments(top_post.selftext)
            if comment.startswith('"') and comment.endswith('"'):
                comment = comment[1:-1]
            top_post.reply(comment)
            logging.info(f"Commented on the top post in r/{subreddit_name}: {comment}")
            print(f"Commented on the top post in r/{subreddit_name} with comment: \n {comment}")
            print("link to the comment: ", top_post.permalink)
        else:
            logging.warning(f"No text found in the top post of r/{subreddit_name}.")
            return {"error": "No text in the top post."}

        return {"success": True}

    except Exception as e:
        # Detailed error logging
        error_message = f"An error occurred: {e}"
        logging.error(f"Error in comment_on_post for {subreddit_name}: {error_message}")
        print(error_message)
        return {"error": error_message}

