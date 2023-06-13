import praw
import time
from config import reddit
#based on https://www.reddit.com/r/ModCoord/comments/147b4n9/heres_a_python_modmail_auto_responder_to/
# Create a Reddit instance
import questionary 

sub_name = questionary.ask("What subreddit would you like to run the script on?")
keywords = ['private', 'blackout', 'dark', 'closed', 'join',  'shut down']
response_message = "Hello and thank you for your message.  It appears that you are writing in about the Reddit wide blackout to protest API changes. We would like to direct you to [this post](https://www.reddit.com/r/Save3rdPartyApps/comments/1476ioa/reddit_blackout_2023_save_3rd_party_apps/) where you can find, among other information, a list of participating subreddits. \n\nWe will remain closed until further notice, and cannot make exceptions"



processed_mail = []

while True:
try:
    print("Fetching modmail conversations...")
    conversations = reddit.subreddit(sub_name).mod.stream.modmail_conversations(skip_existing=True)

    for conv in conversations:
        if len([author for author in conv.authors if author.is_admin]) > 0:
                reddit.redditor("mod_mailer").message(subject=f"{conv.owner}", message =f"New Admin modmail in r/{conv.owner}\n\n---\n\nNew modmail message from admins https://mod.reddit.com/mail/all/{conv.id}\n\nSubject: {conv.subject}")
                conv.archive()

        if conv.id not in processed_mail:       
            for message in conv.messages:
                body = message.body_markdown.lower()
                if any(keyword in body for keyword in keywords):
                    print(f"Found modmail in r/{conv.owner} - keyword in message with ID {conv.id} from user {conv.user.name}")

                    conv.reply(body=response_message, author_hidden=True)
                    conv.archive()
                    processed_mail.append(conv.id)
                    print(f"Replied to message ID {conv.id} from user {conv.user.name} with the preset response\n")
                    #print(processed_mail)
except Exception as e:
    print(f"An error occurred: {e}")
    print("Sleeping for 60 seconds before retrying...")
    time.sleep(60)