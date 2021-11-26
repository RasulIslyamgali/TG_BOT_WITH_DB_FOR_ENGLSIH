from multiprocessing import Process
from manually_english_bot import two_, one_


if __name__ == "__main__":
    Process(target=two_).start()
    Process(target=one_).start()