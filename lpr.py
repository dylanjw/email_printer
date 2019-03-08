import subprocess


def print_file_to_pdf(filename):
    if not isinstance(filename, (str,)):
        raise ValueError("filename must be a string")
    subprocess.Popen(['lpr', filename])

def print_contents_to_pdf(filename):
    ...
