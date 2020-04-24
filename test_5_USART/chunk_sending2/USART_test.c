#include <avr/io.h>
#include <util/delay.h>
#include <stdint.h>
#include <avr/interrupt.h>
#include "../UART/uart.h"


//^^^relative file position to uart header
//use programmer.sh to program with avr-gcc compiler
//directly with "bash programmer.sh"
//go to https://www.linkedin.com/pulse/introduction-avr-c-programming-macos-finally-attiny85-jorge-salas/?trackingId=ZUBziTtZSbuvwqTwPRXbvw%3D%3D
//to learn more about AVR programming on MAC
//Use Atmel studio if you have a windows PC
//Linux may also have AVR crosspack tools as well
uint8_t equals(uint8_t * A, uint8_t * B);

#define TRUE 1
#define FALSE 0

uint8_t i = 0;
uint8_t success[] = {'s','u','c','c','e','s','s'};
uint8_t buffer[32];
void main(){
	USART_Init(); //sets up USART registers
	DDRB |= 1 << 5; //sets arduino pin 13 to output 
	sei(); //prepares the microncontroller for a USART intterupt
	while(TRUE){
		; // stand alone semicolon is a NOP operation
	}
	
}

ISR(USART_RX_vect){
	uint8_t receivedByte;
	receivedByte = (uint8_t) USART_Receive();
	buffer[i] = receivedByte;
	i++;
	if(i == 32){
		if(equals(success,buffer)){
			PORTB ^= 1 << 5; //toggles pin 13
		}
		i = 0;
	}
	sei();//every time its called, interrupt is cleared so need to set it again =
}

uint8_t equals(uint8_t * A, uint8_t * B){
	for(uint8_t j = 0; j < 7; j++){
		if(A[j] != B[j]){
			return FALSE;
		}
	}
	return TRUE;
}
//receiving a byte from serial port, any programming language can send into the port
//in this case will be using python