import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from faxta_utils import to_tuple
from golemail.providers import Google
from golemail.utils import (convert_email_date, convert_to_mime_msg,
                            decode_filename_header, get_attachments,
                            get_message_body)


class Google:
    formatter = None

    def __init__(self, creds=None):
        self.formatter = convert_to_mime_msg

        if creds is None:
            creds = get_creds()
        self._creds = creds

        self._api = self.get_gmail_api(self.creds)

    def latest_messages(self):
        messages = get_messages_list
        for message in messages:
            yield self.formatter(_get_message(message['id']))

    def _get_message(self, messageID):
        return self._api.users().messages().get(
            userId='me',
            id=messageID,
            format='raw').execute()


def get_creds():
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

    return creds


def get_gmail_api(creds=None):
    if creds is None:
        creds = get_creds()
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_messages_list(gmail=None):
    if gmail is None:
        gmail = get_gmail_api()
    results = gmail.users().messages().list(userId='me', labelIds='INBOX').execute()

    return results['messages']


def write_attachments_to_files(message, gmail=None):
    if gmail is None:
        gmail = get_gmail_api()
    messageID = message['id']
    message = gmail.users().messages().get(userId='me', id=messageID, format='raw').execute()
    mime_msg = convert_to_mime_msg(message)
    body = get_message_body(mime_msg)
    attachments = get_attachments(mime_msg)
    for filename, data in attachments:
        if data is not None:
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(data))
