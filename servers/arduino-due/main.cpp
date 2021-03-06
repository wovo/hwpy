// ==========================================================================
//
// Arduino Due remote GPIO server
//
// ==========================================================================

#include "hwlib.hpp"
#include "../commands.hpp"

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
   
   auto p24 = hwlib::target::pin_in_out( hwlib::target::pins::a0 );
   auto p25 = hwlib::target::pin_in_out( hwlib::target::pins::a1 );
   auto p26 = hwlib::target::pin_in_out( hwlib::target::pins::a2 );
   auto p27 = hwlib::target::pin_in_out( hwlib::target::pins::a3 );
   auto p28 = hwlib::target::pin_in_out( hwlib::target::pins::a4 );
   auto p29 = hwlib::target::pin_in_out( hwlib::target::pins::a5 );
   auto p30 = hwlib::target::pin_in_out( hwlib::target::pins::a6 );
   auto p31 = hwlib::target::pin_in_out( hwlib::target::pins::a7 );

   hwlib::pin_in_out * pin_table[ 32 ] = {
      &p00, &p01, &p02, &p03, &p04, &p05, &p06, &p07, &p08, &p09,
      &p10, &p11, &p12, &p13, &p14, &p15, &p16, &p17, &p18, &p19,
      &p20, &p21, &p22, &p23, &p24, &p25, &p26, &p27, &p28, &p29,
      &p30, &p31
   };
   
   hwlib::wait_ms( 10 );

   for(;;){	   
      char c = hwlib::cin.getc();	  
      int pin_nr = c & 0x1F;
      auto & pin = * pin_table[ pin_nr ];
      command cmd = (command) (( c >> 5 ) & 0x7 );
     //hwlib::cout << "p=" << pin_nr << " c=" << int(cmd) << "\n";
     do_command( pin, cmd );
   }   
}   