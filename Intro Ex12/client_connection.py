###################################################################
# FILE: client_connection.py
# WRITERS: Eldan Chodorov, eldan, 201335965
#          and Keren Meron, keren.meron, 200039626
# EXERCISE: intro2cs ex12 2016-2016
# DESCRIPTION: connects to a server, and sends and receives data.
###################################################################

import socket
import select
from constants import *

class Client():
    '''This class holds all information for the Client object.'''

    def __init__(self, host, port, user_name, group_name):
        '''Initializes all of the containers needed for this class to work.
        Connects to server.'''

        self.__name = user_name
        self.__group = group_name
        self.__host = host
        self.__port = port
        self.__bond = socket.socket()
        self.__group_members = []
        self.__interrupted_msg = ""
        self.connection()


    def connection(self):
        '''Connects socket with server and sends message of joining.'''

        self.__bond.connect((self.__host,self.__port))
        msg = MSG_JOIN, SEP1, self.__name, SEP1, self.__group, MSG_DELIMITER
        self.send(msg)


    def receive(self):
        '''Receives messages from server, which assumes separated by line
        delimiters. Returns a list of messages.'''

        r, w, x = select.select([self.__bond], [], [], SELECT_RCV_TIMER)
        #if len(r) != 0:
        for sock in r:
            if sock == self.__bond:
                data = self.__bond.recv(BUFF_SIZE)
                data = bytes.decode(data)
                return self.msg_split(data)
        #else:
          #  return


    def msg_split(self, data):
        '''Receives a string containing messages separated by a delimiter,
        and returns a list of the messages.'''

        prev_index = 0
        orderly_msg = []

        if self.__interrupted_msg:
            del_index = data.find(MSG_DELIMITER)
            concatenated = self.__interrupted_msg + data[:del_index]
            orderly_msg.append(self.msg_handler(concatenated))
            self.__interrupted_msg = ""
            prev_index = del_index + 1

        for index, char in enumerate(data):
            if index < prev_index:
                continue
            if char == MSG_DELIMITER:
                msg = data[prev_index:index]
                if len(msg) == 0 or len(msg.replace(MSG_DELIMITER, "")) == 0:
                    continue
                orderly_msg.append(self.msg_handler(msg))
                prev_index = index + 1

            elif index == len(data) - 1:
                self.__interrupted_msg = data[prev_index:]
                break

        return orderly_msg


    def msg_handler(self, msg):
        '''
        Receives msg(str) from server and handles according to first word:
        users/leave/join - updates group list.
        shape - draws on board.
        error - opens an error box.
        '''

        msg_split = msg.split(SEP1, maxsplit=1)
        type = msg_split[0]
        sep = SEP2

        while MSG_DELIMITER in type:
            type = type[1:]
        if type == MSG_SHAPE:
            sep = SEP1
        elif type == MSG_ERROR:
            return type, msg_split[1]
        details = msg_split[1].split(sep)

        return type, details


    def send(self, msg):
        '''Sends a message to server.'''

        msg = ''.join(list(msg)) + MSG_DELIMITER
        encoded_msg = str.encode(msg)
        self.__bond.sendall(encoded_msg)


    def close_connection(self):
        '''Disconnects from server.'''
        self.__bond.close()

