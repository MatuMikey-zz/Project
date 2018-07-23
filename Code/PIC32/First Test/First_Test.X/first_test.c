#include <p32xxxx.h>                // include chip specific header file
//#include <plib.h>                   // include peripheral library functions

// Configuration Bits
#pragma config FNOSC = FRCPLL       // Internal Fast RC oscillator (8 MHz) w/ PLL
#pragma config FPLLIDIV = DIV_2     // Divide FRC before PLL (now 4 MHz)
#pragma config FPLLMUL = MUL_20     // PLL Multiply (now 80 MHz)
#pragma config FPLLODIV = DIV_2     // Divide After PLL (now 40 MHz)
                                    // see figure 8.1 in datasheet for more info
#pragma config FWDTEN = OFF         // Watchdog Timer Disabled
#pragma config ICESEL = ICS_PGx1    // ICE/ICD Comm Channel Select
#pragma config JTAGEN = OFF         // Disable JTAG
#pragma config FSOSCEN = OFF        // Disable Secondary Oscillator

#define SYSCLK 40000000L

int main(){

    ANSELB = 0;
    int i = 0;
    TRISBbits.TRISB5 = 0;

    while(1){

        for(i = 0; i < 1000000; i++){

        }
        LATBbits.LATB5 = 1;
        for(i = 0; i < 1000000; i++){

        }
        LATBbits.LATB5 = 0;
    }
}