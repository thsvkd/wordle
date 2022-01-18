import os
from socket import timeout
import sys
import json
from threading import Thread, Lock, Event
from queue import Queue
from msvcrt import getch
from typing import *


class InputManager():
    def __init__(self) -> None:
        self.handle_input_lock = Lock()
        self.handle_input_event = Event()
        self.handle_input_thread = Thread()
        self.handle_output_lock = Lock()
        self.handle_output_event = Event()
        self.handle_output_thread = Thread()

        self.handle_input_quque = Queue()
        self.handle_output_quque = Queue()

        self.key = None

    def handle_user_input(self) -> None:
        while not self.handle_input_event.wait(timeout=0.1):
            self.key = ord(getch().lower())
            if self.key > ord('a') and self.key < ord('z'):
                self.key = None
            else:
                self.handle_input_quque.put(self.key)

    def handle_output(self) -> None:
        while not self.handle_output_event.wait(timeout=0.1):
            if not self.handle_output_quque.empty():
                print(self.handle_output_quque.get(), end='')

    def run(self):
        self.handle_input_thread = Thread(
            target=self.handle_user_input, daemon=True, )
        self.handle_input_thread.start()


class PrintManager():
    def __init__(self) -> None:
        self.handle_print_lock = Lock()
        self.handle_print_event = Event()
        self.handle_print_thread = Thread()

        self.handle_print_quque = Queue()

    def handle_print(self) -> None:
        while not self.handle_print_event.wait(timeout=0.1):
            pass

    def run(self):
        self.handle_input_thread = Thread(
            target=self.handle_print, daemon=True, )
        self.handle_input_thread.start()


class WordleClient():
    def __init__(self) -> None:
        self.word_dic = []
        self.load_word_list()
        if not os.path.exists('./5_letter_word.txt'):
            self._extract_5_letter_words(self.word_dic)

        self.input_manager = InputManager()
        self.print_manager = PrintManager()
        self.input_manager.run()
        self.print_manager.run()

    def _extract_5_letter_words(self, word_list, path='./5_letter_word.txt'):
        word_list = [word for word in word_list if len(word) == 5]
        with open(path, 'w') as f:
            for word in word_list:
                f.write(word + '\n')

    def load_word_list(self):
        with open('./google-10000-english/20k.txt', 'r') as f:
            for line in f:
                self.word_dic.append(line.strip())

            f.close()

    def check_word_exist(self, word):
        for i in self.word_dic:
            if i == word:
                return True


if __name__ == '__main__':
    input_manager = InputManager()
    wordle_client = WordleClient()
    wordle_client.load_word_list()
    result = wordle_client.check_word_exist('hello')
