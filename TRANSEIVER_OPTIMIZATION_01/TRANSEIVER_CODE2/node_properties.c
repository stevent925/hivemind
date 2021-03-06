#include "node_properties.h"

void process_uart_input(){
	uint8_t pipe = 0;
	printf("data: %c\n", data_buffer[0]);
	switch(data_buffer[0]){
		case '0': {
				  left_shift(data_buffer);
				  nrf24_send(data_buffer); //maybe I should edit esto instead
				  while(nrf24_isSending())
					NOOP;
				  } 
				  break;
		
		case '1': setAddress(TX_ADDR_VAL,data_buffer, TRUE, -1);
				  break;
		case '2': pipe = data_buffer[1] - '0';
				  left_shift(data_buffer);
				  setAddress(RX_ADDR_P_VAL[pipe],data_buffer, FALSE, pipe);	
				  break;
		case '3': print_address(TX_ADDR_VAL);	
				  break;
		case '4': pipe = data_buffer[1] - '0';
				  print_address(RX_ADDR_P_VAL[pipe]);
				  break;
		case '5': toggle_success_mode(success_mode);
				  break;
		case '6': { //get success mode
					printf("STATE:");
					USART_Transmit(success_mode + '0');
					USART_Transmit('\n');
				  }
				  break;
		case '7': PORTD ^= 1 << 5;    //getting the state of whether a port is on would be cool, this is where stron designing of the c code will come on
				  break;
		case '8': 
				  break;
		case '9': // in python program this is for finding mode, again not to be implemented
				  break; // will add a polling mode I think a separate pipe should be dedicated for that
		  
		default:  printf("INVALID STATE\n");
		
	}
}

void process_recieved(){
	static char success[32] = "<<<success>>>";
	switch(receive_buffer[0]){
		case '0': PORTD ^= 1 << 5;
				  break;
		case '1': toggle_success_mode(success_mode);
		          break;
		case '2': //send to other node propogation
				  break;
		default :
			      break; //dummy statement need to make a new return statement
	}
	if(success_mode){
		if(is_success(receive_buffer, success)){
			printf("SUCCESS:%s\n",success);
		}else{
			printf("RECEIVED:%s\n",receive_buffer); //bytes 0-9 need to be removed by program
			nrf24_send(success);
			receiving = FALSE;
		}
	}
	else{
		printf("RECEIVED:%s\n",receive_buffer);
	}
}


uint8_t is_success(uint8_t * receive, uint8_t * success){
	uint8_t i;
	for(i = 0; i < 13; i++){
		if(receive[i] != success[i]){
			return FALSE;
		}
	}
	return TRUE;
}

uint8_t print_address(uint8_t * address){
	printf("STATE:");
	for(uint8_t i = 0; i < 5; i++){
		USART_Transmit(address[i]);
	}
	USART_Transmit('\n');
}

void setAddress(uint8_t * address_buffer, uint8_t * new_address, uint8_t mode, uint8_t pipe){
	for(uint8_t i = 0; i < 5; i++){
		address_buffer[i] = new_address[i + 1];
	}
	if(mode){
		nrf24_tx_address(address_buffer);
	}
	else{
		nrf24_rx_address(address_buffer, pipe);
	}
}


void left_shift(uint8_t * data_buffer){
	for(int i = 1; i < 32; i++){
		data_buffer[i - 1] = data_buffer[i];
	}
}
