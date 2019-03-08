import base64
import datetime
import email


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
