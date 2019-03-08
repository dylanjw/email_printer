import base64
import datetime
import email
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from golemail.utils import (convert_email_date, convert_to_mime_msg,
                            decode_filename_header)
from utils import to_tuple

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']



@to_tuple
def get_attachments(mime_msg):
    if mime_msg.is_multipart:
        for part in mime_msg.walk():
            part_type = part.get_content_maintype()
            if part_type == 'application' or part_type == 'image':
                filename = decode_filename_header(part.get_filename())
                data = part.get_payload()
                yield filename, data

def get_message_body(mime_msg):
    if mime_msg.is_multipart:
        for part in mime_msg.walk():
            part_type = part.get_content_type()
            if part_type == 'text/html':
                return part.get_payload()
    elif mime_msg.get_content_maintype() == 'text':
        return mime_msg.get_payload()

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
    messages = results['messages']

    for message in messages:
        messageID = message['id']
        message = service.users().messages().get(userId='me', id=messageID, format='raw').execute()
        mime_msg = convert_to_mime_msg(message)
        body = get_message_body(mime_msg)
        print(mime_msg['Subject'])
        attachments = get_attachments(mime_msg)
        for filename, data in attachments:
            print(filename)
            if data is not None:
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(data))

if __name__ == '__main__':
    main()
