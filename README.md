Requirements:

sudo apt-get install cups-pdf
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


Currently this project is not in a working state. Don't run it.


Road Map:

1. Extract email body, and attachments.  Currently supports multipart emails, pdf, jpeg and png.
2. Build PDF or other format for printing.
3. Allow customization options via subject line tags: 
    \#attachmentsonly,  
    \#bodyonly, 
    \#portrait, 
    \#copies:5, 
    \#b&w, 
    \#color.
4. Send documents to printer via lpr wrapper.
5. Update gmail folder/tags. Remove from inbox.
6. Create daemon process.
7. Add event loop, with configurable email check period.
