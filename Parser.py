# parser file

import struct

class Parser():
    """
    FUNCTION
        takes a string and parses it
    """
    def parse_data(self, data):
    	print("DATA PARSER")
    	print(data)
    	data_list = data.decode().split(" ")
    	print("PARSER nonce " + data_list[0])
    	return data_list

    def parse_byte_string(self, data):
    	print("BYTES PARSER")
    	print(data)
    	data_list = data.decode().split(' b')
    	print("DATA LIST")
    	print(data_list)
    	parsed_byte_string = []
    	parsed_byte_string.append(data_list[0])
    	formatted_ciphertxt = data_list[1].replace("'", "")
    	parsed_byte_string.append(formatted_ciphertxt)
    	return parsed_byte_string

    def parse_response(self, data):
	    formatted_ciphertxt = data[1:].replace("'", "")
	    return formatted_ciphertxt

    def parse_plaintxt(self, plain):
    	print("PARSING PLAIN TEXT")
    	plaintxt_parts = plain[-32:]
    	try:
    		data_list = plaintxt_parts.decode().split(" ")
    	except:
    		data_list = plaintxt_parts.split(b' ')


    	print(data_list)
    	# message = b'acsdasadsadadsasdas 124661924 5'

    	return data_list