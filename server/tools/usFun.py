from datetime import datetime
import random


def getCurrentTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message):
    text = f"[ {getCurrentTime()} ] {message}"
    print(text)
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")


def randomStudentId():
    return f"2020{random.randint(10000000, 99999999)}"


if __name__ == "__main__":
    print(randomStudentId())
