// ==========================================================================
//
// DB104 (LPC1114) remote GPIO server
//
// ==========================================================================

#include "hwlib.hpp"
#include "../commands.hpp"

int main(){

   auto p00 = hwlib::target::pin_in_out( 0, 4 );
   auto p01 = hwlib::target::pin_in_out( 0, 5 );
   auto p02 = hwlib::target::pin_in_out( 0, 6 );
   auto p03 = hwlib::target::pin_in_out( 0, 7 );
   auto p04 = hwlib::target::pin_in_out( 1, 0 );
   auto p05 = hwlib::target::pin_in_out( 1, 1 );
   auto p06 = hwlib::target::pin_in_out( 1, 2 );
   auto p07 = hwlib::target::pin_in_out( 1, 3 );
   auto p08 = hwlib::target::pin_in_out( 1, 4 );
   auto p09 = hwlib::target::pin_in_out( 1, 5 );
   auto p10 = hwlib::target::pin_in_out( 1, 8 );
   auto p11 = hwlib::target::pin_in_out( 1, 9 );

   hwlib::pin_in_out * pin_table[ 12 ] = {
      &p00, &p01, &p02, &p03, &p04, &p05, 
      &p06, &p07, &p08, &p09, &p10, &p11
   };
   
   hwlib::wait_ms( 10 );
   hwlib::cout << "Server\n";

   for(;;){	   
      char c = hwlib::cin.getc();	  
      int pin_nr = c & 0x1F;
      if( pin_nr > 11 ) continue;
      auto & pin = * pin_table[ pin_nr ];
      command cmd = (command) (( c >> 5 ) & 0x7 );
      //hwlib::cout << "p=" << pin_nr << " c=" << int(cmd) << "\n";
      do_command( pin, cmd );
   }   
}   