import subprocess


def get_output():
    # Run the command and get its output
    result = subprocess.run(
        ["python", "main.py", "-A", "-odds=fanduel", "-kc"], stdout=subprocess.PIPE
    )

    encodings = ["ascii", "latin-1", "cp1252", "utf-8-sig"]

    for encoding in encodings:
        try:
            output = result.stdout.decode(encoding)
            print(output)
            # print(f"Decoded with {encoding}")
            return output
        except UnicodeDecodeError:
            print(f"Failed to decode with {encoding}")
            print("hello world")
            print("hello world")
