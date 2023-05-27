class WordWrap:
    """
    A utility class for wrapping and filling text to a specified width.

    This class provides methods to wrap text to a specified width and fill lines as needed.

    Attributes:
        width (int): The maximum width for wrapping the text.
        replace_whitespace (bool): If True, replaces consecutive whitespace characters with a single space.

    Methods:
        fill(text): Wraps the text to the specified width and fills lines as needed.
        wrap(text): Wraps the text to the specified width.

    """

    def __init__(self, width=120, replace_whitespace=False):
        """
        Initializes the WordWrap class.

        Args:
            width (int): The maximum width for wrapping the text (default: 120).
            replace_whitespace (bool): If True, replaces consecutive whitespace characters with a single space
            (default: False).
        """

        self.width = width
        self.replace_whitespace = replace_whitespace

    def fill(self, text):
        return fill(text, self.width, self.replace_whitespace)

    def wrap(self, text):
        return wrap(text, self.width, self.replace_whitespace)


def fill(text, width=120, replace_whitespace=False):
    """
    Wraps the text to the specified width and fills lines as needed.

    Args:
        text (str): The input text to be wrapped and filled.
        width (int): The maximum width for wrapping the text (default: 120).
        replace_whitespace (bool): If True, replaces consecutive whitespace characters with a single space
        (default: False).

    Returns:
        str: The wrapped and filled text.
    """

    i = 0
    while i < len(text) - 1:
        if text[i] == "\n":
            text = text[:i+1] + " " + text[i+1:]
        i += 1

    if replace_whitespace:
        text = text.replace('\n', '')

    new_string = ""
    split_string = text.split(' ')
    count = 0
    for c in split_string:
        if c.startswith('\n'):
            count = 0
            new_string += c
            continue
        if (count + len(c)) >= width:
            new_string += '\n'
            count = 0
        if len(c) > 0:
            new_string += c + ' '
            count += len(c) + 1

    return new_string


def wrap(text, width=120, replace_whitespace=False):
    """
    Wraps the text to the specified width.

    Args:
        text (str): The input text to be wrapped.
        width (int): The maximum width for wrapping the text (default: 120).
        replace_whitespace (bool): If True, replaces consecutive whitespace characters with a single space
        (default: False).

    Returns:
        list: A list of wrapped lines.
    """

    wrapped_string = fill(text, width, replace_whitespace).split('\n')
    return wrapped_string


def main():
    sample = """Thank you for providing the position description and the resume. After reviewing both documents, I would rate the candidate's suitability for the job as a 7 out of 10. 

    The candidate has relevant experience in the field and has demonstrated skills that match the requirements listed in the position description. However, there are a few areas where the candidate could improve their qualifications for the job. 
   
    For example, the position description mentions the need for experience with a specific software program, but the candidate does not list that software on their resume. Additionally, the candidate's experience in a related field is not as extensive as some other applicants may have. 

    Overall, the candidate has potential to be a strong fit for the job, but may need to further develop their skills and experience in certain areas."""

    w = WordWrap()
    print(fill(sample, 120, True))


if __name__ == "__main__":
    main()
