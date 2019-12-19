// ==========================================================================
//
// remote GPIO server commands
//
// ==========================================================================

enum class command { 
   input   = 0, 
   output  = 1, 
   high    = 2, 
   low     = 3, 
   read    = 4 
};   

void do_command( hwlib::pin_in_out & pin, command cmd ){

   if ( cmd == command::input ){
      pin.direction_set_input();
      pin.direction_flush();
	  
   } else if ( cmd == command::output ){
      pin.direction_set_output();
      pin.direction_flush();

   } else if( cmd  == command::high ){
      pin.write( 1 );
	  pin.flush();

   } else if( cmd  == command::low ){
      pin.write( 0 );
      pin.flush();
	  
   } else if( cmd  == command::read ){
	 pin.refresh();
     hwlib::cout << ( pin.read() ? '1' : '0' );
	  
   }	  	
}