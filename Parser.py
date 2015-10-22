# parser file

import struct

class Parser():
    """
    FUNCTION
        takes a string and parses it
    """
    def parse_data(self, data):
    	data_list = data.decode().split(" ")
    	return data_list

    def parse_byte_string(self, data):
    	data_list = data.decode().split(' b')
    	parsed_byte_string = []
    	parsed_byte_string.append(data_list[0])
    	formatted_ciphertxt = data_list[1].replace("'", "")
    	parsed_byte_string.append(formatted_ciphertxt)
    	return parsed_byte_string

    def parse_response(self, data):
    	formatted_ciphertxt = data[1:].replace("'", "")
    	return formatted_ciphertxt

    def parse_plaintxt(self, plain):
    	plaintxt_parts = plain[-32:]
    	try:
    		data_list = plaintxt_parts.decode().split(" ")
    	except:
    		data_list = plaintxt_parts.split(b' ')

    	return data_list