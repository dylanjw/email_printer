import base64
import datetime
import email

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class Email:
    provider = None


if __name__ == '__main__':
    gmail = get_gmail_api()
    for message in get_messages_list(gmail):
        print(message['Date'])
        write_attachments_to_files(message, gmail)
