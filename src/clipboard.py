import pyperclip


def to_clipboard(array):
    string = "\n".join(map(str, array))
    pyperclip.copy(string)
    print("Copied to clipboard:", pyperclip.paste())


if __name__ == "__main__":
    to_clipboard([1, 2])
