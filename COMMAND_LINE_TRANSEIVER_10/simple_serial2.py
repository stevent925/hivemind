import serial
import glob
import multiprocessing

class CentralNode:
	__MESSAGING = 0
	__SET_TX_ADDRESS = 1
	__SET_RX_ADDRESS = 2
	__GET_TX_ADDRESS = 3
	__GET_RX_ADDRESS = 4
	
	def __init__(self, TXaddress = "00000", RXaddress = "11111", SERIAL_PORT_NAME = None, BAUD_RATE = 9600):
		self.__serial_port = None
		self.TXaddress = TXaddress
		self.RXaddress = RXaddress
		self.__fetchMessagesProcess = None
		if SERIAL_PORT_NAME != None:
			self.__setConnection(SERIAL_PORT_NAME, BAUD_RATE)
	
	def __setConnection(self, SERIAL_PORT_NAME, BAUD_RATE):
		self.serial_port = serial.Serial(SERIAL_PORT_NAME, BAUD_RATE)
		self.serial_port.write(bytes(CentralNode.__SET_TX_ADDRESS + self.TXaddress,encoding = 'utf-8'))
		self.serial_port.write(bytes(CentralNode.__GET_TX_ADDRESS, encoding = 'utf-8'))
		self.TXaddress = str(self.serial_port.readline())
		print(self.TXaddress)
		self.serial_port.write(bytes(CentralNode.__SET_RX_ADDRESS + self.RXaddress,encoding = 'utf-8'))
		self.serial_port.write(bytes(CentralNode.__GET_RX_ADDRESS, encoding = 'utf-8'))
		self.RXaddress = str(self.serial_port.readline())
		print(self.RXaddress)
		


def main():
	greet()
	instructions()
	ser = None
	p1 = None
	try:
		ser = getSerialPort()
		p1 = multiprocessing.Process(target = printing, args = (ser,)) #running in parallel to main process this function, function processing in parallel
		p1.start()		#starts parallel process
		while True:
			word = input("Enter a message to write:")  #gets user input
			ser.write(bytes(word + "\r", encoding ='utf-8')) #writes bytes to serial port for board to pick up and use
	except Exception as e:
		print(e)
	finally:
		p1.terminate() #closes parallel process
		ser.close() #closes port

def getSerialPort():   #handling exception handling of the port is also a good idea
	SERIAL_RATE = 9600
	ports = getAvailablePorts()
	print(ports)
	choice = int(input("choose port to open (enter index from 0 to " + str(len(ports) - 1)   + "):"))
	#need to add some code to prevent opening a port if its already in use
	SERIAL_PORT = ports[choice]
	ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
	return ser	

def printing(ser):         #gets the receiving messages in a parallel process
	cant_decode = False
	while True:
		reading = ser.readline()
		reading = str(reading)
		try:                                          #if you remove the try except and type clear, the INVALID state message will cause reading.index(':') to throw an exception
			l = reading.index(':') + 1
			if "\\x" in reading:
				reading = reading[l:len(reading) - 3]
			else:
				r = reading.index('\\')
				reading = reading[l:r]
		except:
			pass
		print("\r" + str(reading) + (" " * 50))
		print("\nEnter a message to write:",end="")

def getAvailablePorts():
	ports = glob.glob("/dev/tty.wchusbserial*")  #gets a list of ports
	while(len(ports) == 0):
		end = input("Enter 0 if you want to exit the program, otherwise plug in a board and enter a different value: ")
		if(end == '0'):
			exit()
		ports = glob.glob("/dev/tty.wchusbserial*")
	return ports

def greet():
	print("Welcome to the NRF24L01 Playground")

def instructions():
	print("preceeding 0 with input (ex. 0hello) will send hello")
	print("preceeding 1 with 5 characters following it will set the transmitting address (ex. 1abcde will set TXaddress to abcde")
	print("preceeding 2 with 5 characters following it will set the receiving address (ex. 2abcde will set RXaddress to abcde")
	print("preceeding 3 with any message (or just typing 3 by itself) returns the current transmitting address")
	print("preceeding 4 with any message (or just typing 4 by itself) returns the current receiving address")	
			
    	

if __name__ == "__main__":
	main()