TRANSMIT = 0
SET_TX_ADDRESS = 1
SET_RX_ADDRESS = 2
GET_TX_ADDRESS = 3
GET_RX_ADDRESS = 4
TOGGLE_SUCCESS_MODE = 5
GET_SUCCESS_MODE = 6
TOGGLE_LED = 7
FINDING = chr(8)
FINDING_ADDRESS = "\x00!!"
MESSAGE = "0"
ADDRESS_RETURN = ord("3")
FILE_LINE_SEND = ord("6")
FLUSH = '\r'   #should use something different
PERSONAL_MESSAGE = ord("0") #should change to actual 0 soon
MESSAGE_LENGTH = 26