def read_file(file):
    """Reads a file and returns its contents."""
    with open(file, "r") as f:
        content = f.read()
        # add a newline at the end of the file if it doesn't have one
        if content and content[-1] != "\n":
            content += "\n"
        return content

