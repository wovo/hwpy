// ==========================================================================
//
// remote GPIO server
//
// This application implements a GPIO server that can be used to control
// its GPIO pins over a serial line nusing a simple but fast protocol.
//
// The main purpose is to test Python code that manipulates GPIO pins
// without having to run the Python code on an embedded system.
// Additionally, it is easier to swap one Arduino due with peripheral
// hardware for anotrher one, than swapping the  peripherals connected
// to a Raspberry Pi.
//   
// Protocol:
// - 115k2 baud
// - one-byte commands to this server
// - high 3 bits == command, as per enum class command
// - low 5 bits == pin, as per pin_table
// - digital read sends back '0' or '1'
// - other commands are silent
//
// Notes:
// - only 32 pins can be used this way
// - only GPIO supported
// - the server doesn't do any checking
//
// ==========================================================================

#include "hwlib.hpp"

enum class command { 
   input   = 0, 
   output  = 1, 
   high    = 2, 
   low     = 3, 
   read    = 4 
};   

void do_command( hwlib::pin_in_out & pin, command cmd ){

   if ( cmd == command::input ){
HWLIB_TRACE;
//      pin.direction_set_input();
      pin.direction_flush();
	  
   } else if ( cmd == command::output ){
HWLIB_TRACE;
      pin.direction_set_output();
      pin.direction_flush();

   } else if( cmd  == command::high ){
HWLIB_TRACE;
      pin.write( 1 );
	  pin.flush();

   } else if( cmd  == command::low ){
HWLIB_TRACE;
      pin.write( 0 );
      pin.flush();
	  
   } else if( cmd  == command::read ){
HWLIB_TRACE;
	 pin.refresh();
     hwlib::cout << ( pin.read() ? '1' : '0' );
	  
   }	  	
}

int main(){

   auto p00 = hwlib::target::pin_in_out( hwlib::target::pins::d2  );
   auto p01 = hwlib::target::pin_in_out( hwlib::target::pins::d3  );
   auto p02 = hwlib::target::pin_in_out( hwlib::target::pins::d4  );
   auto p03 = hwlib::target::pin_in_out( hwlib::target::pins::d5  );
   auto p04 = hwlib::target::pin_in_out( hwlib::target::pins::d6  );
   auto p05 = hwlib::target::pin_in_out( hwlib::target::pins::d7  );
   auto p06 = hwlib::target::pin_in_out( hwlib::target::pins::d8  );
   auto p07 = hwlib::target::pin_in_out( hwlib::target::pins::d9  );
   auto p08 = hwlib::target::pin_in_out( hwlib::target::pins::d10 );
   auto p09 = hwlib::target::pin_in_out( hwlib::target::pins::d11 );
   auto p10 = hwlib::target::pin_in_out( hwlib::target::pins::d12 );
   auto p11 = hwlib::target::pin_in_out( hwlib::target::pins::d13 );
   auto p12 = hwlib::target::pin_in_out( hwlib::target::pins::d14 );
   auto p13 = hwlib::target::pin_in_out( hwlib::target::pins::d15 );
   auto p14 = hwlib::target::pin_in_out( hwlib::target::pins::d16 );
   auto p15 = hwlib::target::pin_in_out( hwlib::target::pins::d17 );
   auto p16 = hwlib::target::pin_in_out( hwlib::target::pins::d18 );
   auto p17 = hwlib::target::pin_in_out( hwlib::target::pins::d29 );
   auto p18 = hwlib::target::pin_in_out( hwlib::target::pins::d20 );
   auto p19 = hwlib::target::pin_in_out( hwlib::target::pins::d21 );
   auto p20 = hwlib::target::pin_in_out( hwlib::target::pins::d22 );
   auto p21 = hwlib::target::pin_in_out( hwlib::target::pins::d23 );
   auto p22 = hwlib::target::pin_in_out( hwlib::target::pins::d24 );
   auto p23 = hwlib::target::pin_in_out( hwlib::target::pins::d25 );
   auto p24 = hwlib::target::pin_in_out( hwlib::target::pins::d26 );
   auto p25 = hwlib::target::pin_in_out( hwlib::target::pins::d27 );
   auto p26 = hwlib::target::pin_in_out( hwlib::target::pins::d28 );
   auto p27 = hwlib::target::pin_in_out( hwlib::target::pins::d29 );
   auto p28 = hwlib::target::pin_in_out( hwlib::target::pins::d30 );
   auto p29 = hwlib::target::pin_in_out( hwlib::target::pins::d31 );
   auto p30 = hwlib::target::pin_in_out( hwlib::target::pins::d32 );
   auto p31 = hwlib::target::pin_in_out( hwlib::target::pins::d33 );

   hwlib::pin_in_out * pin_table[ 32 ] = {
      &p00, &p01, &p02, &p03, &p04, &p05, &p06, &p07, &p08, &p09,
      &p10, &p11, &p12, &p13, &p14, &p15, &p16, &p17, &p18, &p19,
      &p20, &p21, &p22, &p23, &p24, &p25, &p26, &p27, &p28, &p29,
	  &p30, &p31
   };
   
   hwlib::wait_ms( 10 );
   
if(0){
   auto & pin = p11;
   do_command( pin, command::input );
   do_command( pin, command::output );
   for(;;){
      do_command( pin, command::high );
      hwlib::wait_ms( 500 );	  
      do_command( pin, command::low );
      hwlib::wait_ms( 500 );	  
   }
}

      //do_command( p11, command::output );	  
HWLIB_TRACE;

   for(;;){
HWLIB_TRACE;	   
      char c = hwlib::cin.getc();
HWLIB_TRACE;	  
      int pin_nr = c & 0x1F;
      auto & pin = p11;
	  (void)pin_table[ pin_nr ];
      command cmd = (command) (( c >> 5 ) & 0x7 );
	  
	  hwlib::cout << "p=" << pin_nr << " c=" << int(cmd) << "\n";
//      do_command( pin, command::output );	  
	  do_command( pin, cmd );

  
   }   
}   