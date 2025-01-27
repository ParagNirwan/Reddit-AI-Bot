import sys
import schedule
import time
from datetime import datetime
from Reddit import post_to_reddit, comment_on_post
from ContentGeneration import generate_reddit_post


def get_user_input():
    while True:
        try:
            post_time = input("Enter the time for posting (24-hour format HH:MM): ")
            # Validate time format
            time.strptime(post_time, "%H:%M")

            print("*"*100)
            comment_option = input("Do you want to comment on posts? (Y/N): ").strip().upper()
            if comment_option not in ('Y', 'N'):
                raise ValueError("Invalid input. Please enter 'Y' or 'N'.")

            subreddit_name = None
            if comment_option == 'Y':
                subreddit_name = input("Enter the name of the subreddit (without '/r/'): ").strip()
                print("*"*100)
                if not subreddit_name:
                    raise ValueError("Subreddit name cannot be empty.")

            return post_time, comment_option == 'Y', subreddit_name
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def schedule_post(post_time, comment, subreddit_name):
    # Schedule the main post at the specified time
    schedule.every().day.at(post_time).do(lambda: post_to_reddit(generate_reddit_post()))

    if comment:
        # Use a lambda or functools.partial to pass arguments to the comment_on_post function
        schedule.every(1).minutes.do(lambda: comment_on_post(subreddit_name=subreddit_name))
    print("Tasks scheduled successfully.")

def main():
    print("*"*100)
    print("Welcome to the Reddit Bot CLI!")
    
    # Get user input
    post_time, comment, subreddit_name = get_user_input()
    
    # Schedule the post with optional subreddit commenting
    schedule_post(post_time, comment, subreddit_name)
    print("*"*100)
    print("Bot is now running 24x7. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Prevent CPU overuse
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
        print("*"*100)
        sys.exit(0)
        
if __name__ == "__main__":
    main()