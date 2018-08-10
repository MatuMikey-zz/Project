//#include <plib.h>
#include <p32xxxx.h>
 
// Config Bits
#pragma config FNOSC = FRCPLL       // Internal Fast RC oscillator (8 MHz) w/ PLL
#pragma config FPLLIDIV = DIV_2     // Divide FRC before PLL (now 4 MHz)
#pragma config FPLLMUL = MUL_20     // PLL Multiply (now 80 MHz)
#pragma config FPLLODIV = DIV_2     // Divide After PLL (now 40 MHz)
                                    // see figure 8.1 in datasheet for more info
#pragma config FWDTEN = OFF         // Watchdog Timer Disabled
#pragma config ICESEL = ICS_PGx1    // ICE/ICD Comm Channel Select (pins 4,5)
#pragma config JTAGEN = OFF         // Disable JTAG
#pragma config FSOSCEN = OFF        // Disable Secondary Oscillator
 
// Defines
#define SYSCLK (40000000)
 
int analogRead(char analogPIN){
    AD1CHS = analogPIN << 16;       // AD1CHS<16:19> controls which analog pin goes to the ADC
 
    AD1CON1bits.SAMP = 1;           // Begin sampling
    while( AD1CON1bits.SAMP );      // wait until acquisition is done
    while( ! AD1CON1bits.DONE );    // wait until conversion done
 
    return ADC1BUF0;                // result stored in ADC1BUF0
}
 
void delay_us( unsigned t)          // See Timers tutorial for more info on this function
{
    T1CON = 0x8000;                 // enable Timer1, source PBCLK, 1:1 prescaler
 
    // delay 100us per loop until less than 100us remain
    while( t >= 100){
        t-=100;
        TMR1 = 0;
        while( TMR1 < SYSCLK/10000);
    }
 
    // delay 10us per loop until less than 10us remain
    while( t >= 10){
        t-=10;
        TMR1 = 0;
        while( TMR1 < SYSCLK/100000);
    }
 
    // delay 1us per loop until finished
    while( t > 0)
    {
        t--;
        TMR1 = 0;
        while( TMR1 < SYSCLK/1000000);
    }
 
    // turn off Timer1 so function is self-contained
    T1CONCLR = 0x8000;
} // END delay_us()
 
void adcConfigureManual(){
    AD1CON1CLR = 0x8000;    // disable ADC before configuration
 
    AD1CON1 = 0x00E0;       // internal counter ends sampling and starts conversion (auto-convert), manual sample
    AD1CON2 = 0;            // AD1CON2<15:13> set voltage reference to pins AVSS/AVDD
    AD1CON3 = 0x0f01;       // TAD = 4*TPB, acquisition time = 15*TAD
} // END adcConfigureManual()
 
int main( void)
{
	//SYSTEMConfigPerformance(SYSCLK);
 
        // Configure pins as analog inputs
        ANSELBbits.ANSB0 = 1;   // set RB3 (AN5) to analog
        TRISBbits.TRISB0 = 1;   // set RB3 as an input
        TRISBbits.TRISB5 = 0;   // set RB5 as an output (note RB5 is a digital only pin)
 
        adcConfigureManual();   // Configure ADC
        AD1CON1SET = 0x8000;    // Enable ADC
 
        int foo;
	while ( 1)
	{
            foo = analogRead( 0); // note that we call pin AN5 (RB3) by it's analog number
            delay_us( foo);       // delay according to the voltage at RB3 (AN5)
            LATBINV = 0x0020;     // invert the state of RB5
	}
 
	return 0;
}