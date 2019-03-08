import hypothesis
import pytest

from golemail.utils import (convert_email_date, convert_to_mime_msg,
                            decode_filename_header)


@hypothesis.given(hypothesis.strategies.text())
def test_decode_filename_header(val):
    decode_filename_header(val)


@hypothesis.given(hypothesis.strategies.dates())
def test_convert_email_date(date):
    val = convert_email_date(date.isoformat())
    import pdb; pdb.set_trace()
