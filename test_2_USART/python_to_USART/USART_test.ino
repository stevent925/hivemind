#include <avr/io.h>
#include <util/delay.h>
#include <stdint.h>
#include <avr/interrupt.h>

extern "C"{
  #include <uart.h>
}
//^^^ this is important because .ino is technically C++, this is needed to link C file properly
//^^^ UART folder needs to be dragged into libraries folder in Arduino folder in documents
//copy code and paste it into a new arduino (within the IDE) file if forces to make  a folder

#define TRUE 1
#define FALSE 0

void setup(){
	USART_Init(); //sets up USART registers
	DDRB |= 1 << 5; //sets arduino pin 13 to output 
	sei();
}

void loop(){

}

ISR(USART_RX_vect){
	uint8_t receivedByte;
	receivedByte = (uint8_t) USART_Receive();
	if(receivedByte == 1){
		PORTB ^= 1 << 5; //toggles pin 13 
	}
	sei();
}

//receiving a byte from serial port, any programming language can send into the port
//in this case will be using python