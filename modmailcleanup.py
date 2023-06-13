import praw
from datetime import datetime, timedelta
from config import reddit

import questionary
subreddit_name = questionary.text("What sub fam").ask()
subreddit = reddit.subreddit(subreddit_name )
modmail_conversations = subreddit.modmail.conversations(state="new")

def process_modmail():


# Check if it has been three days



    for message in subreddit.modmail.conversations():

        if message.unread and message.num_messages < 2:
            timestamp = (message.last_updated)
            timestamp_datetime = datetime.fromisoformat(timestamp[:-6])
            current_datetime = datetime.utcnow()
            time_difference = current_datetime - timestamp_datetime
            if time_difference >= timedelta(days=3):
                continue
                #print("It has been three days since the timestamp.")
            else:
                print(f"replied to {message.authors}")

                # Archive the modmail
            

                # Send a message
                subject = "We are closed until further notice. Read more -> https://www.reddit.com/r/Save3rdPartyApps/comments/147cksa/why_the_blackouts_happening_from_the_beginning/"
                body = "Read more https://www.reddit.com/r/Save3rdPartyApps/comments/147cksa/why_the_blackouts_happening_from_the_beginning/"
                message.reply(subject, body)
                message.archive()
                #print(message.body)

# Run the function to process modmail


process_modmail()