# parser file

import struct

class Parser():
    """
    FUNCTION
        takes a string and parses it
    """
    def parse_data(self, data):
        data_list = data.decode().split(" ")

        print("PARSER nonce " + data_list[0])
        # print("PARSER id " + data_list[1])

        return data_list
