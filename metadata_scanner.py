import sys

def scan_file(filename):
    return ("Sandstorm", "Darude")

if __name__ == "__main__":
    if(len(sys.argv) < 1):
        print("Please specify a file.")
        exit()

    filename = sys.argv[1]
    data = scan_file(filename)
    print(f"This file contains the song {data[0]} by {data[1]}.")