import base64
import datetime
import email

from faxta_utils import to_tuple


def convert_email_date(date):
    date_tuple = email.utils.parsedate_tz(date)
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(
            email.utils.mktime_tz(date_tuple))
        return local_date.strftime("%a, %d %b %Y %H:%M:%S")


def convert_to_mime_msg(message):
    msg_str = base64.urlsafe_b64decode(message['raw'].encode("ASCII"))
    return email.message_from_bytes(msg_str)


def decode_filename_header(val):
    decoded = email.header.decode_header(val)[0][0]
    if isinstance(decoded, bytes):
        return decoded.decode('utf-8')
    else:
        return decoded


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
