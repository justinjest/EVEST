import pyperclip


def array_to_clipboard(array):
    string = "\n".join(map(str, array))
    pyperclip.copy(string)
    print("Copied to clipboard:", pyperclip.paste())
