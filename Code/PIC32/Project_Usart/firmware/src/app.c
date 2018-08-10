/*******************************************************************************
  MPLAB Harmony Application Source File
  
  Company:
    Microchip Technology Inc.
  
  File Name:
    app.c

  Summary:
    This file contains the source code for the MPLAB Harmony application.

  Description:
    This file contains the source code for the MPLAB Harmony application.  It 
    implements the logic of the application's state machine and it may call 
    API routines of other MPLAB Harmony modules in the system, such as drivers,
    system services, and middleware.  However, it does not call any of the
    system interfaces (such as the "Initialize" and "Tasks" functions) of any of
    the modules in the system or make any assumptions about when those functions
    are called.  That is the responsibility of the configuration-specific system
    files.
 *******************************************************************************/

// DOM-IGNORE-BEGIN
/*******************************************************************************
Copyright (c) 2013-2014 released Microchip Technology Inc.  All rights reserved.

Microchip licenses to you the right to use, modify, copy and distribute
Software only when embedded on a Microchip microcontroller or digital signal
controller that is integrated into your product or third party product
(pursuant to the sublicense terms in the accompanying license agreement).

You should refer to the license agreement accompanying this Software for
additional information regarding your rights and obligations.

SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF
MERCHANTABILITY, TITLE, NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.
IN NO EVENT SHALL MICROCHIP OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER
CONTRACT, NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR
OTHER LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE OR
CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT OF
SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY CLAIMS BY THIRD PARTIES
(INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.
 *******************************************************************************/
// DOM-IGNORE-END


// *****************************************************************************
// *****************************************************************************
// Section: Included Files 
// *****************************************************************************
// *****************************************************************************

#include "app.h"
#include <p32xxxx.h>

#define SYSCLK      40000000
// *****************************************************************************
// *****************************************************************************
// Section: Global Data Definitions
// *****************************************************************************
// *****************************************************************************
char character = 'a';
float j = 0;
// *****************************************************************************
/* Application Data

  Summary:
    Holds application data

  Description:
    This structure holds the application's data.

  Remarks:
    This structure should be initialized by the APP_Initialize function.
    
    Application strings and buffers are be defined outside this structure.
*/

APP_DATA appData;

// *****************************************************************************
// *****************************************************************************
// Section: Application Callback Functions
// *****************************************************************************
// *****************************************************************************

/* TODO:  Add any necessary callback functions.
*/

// *****************************************************************************
// *****************************************************************************
// Section: Application Local Functions
// *****************************************************************************
// *****************************************************************************
void adcConfigureManual(){
    ANSELBbits.ANSB0 = 1;   // set RB3 (AN5) to analog
    TRISBbits.TRISB0 = 1;   // set RB3 as an input
    TRISBbits.TRISB5 = 0;   // set RB5 as an output (note RB5 is a digital only pin)
    AD1CON1CLR = 0x8000;    // disable ADC before configuration
 
    AD1CON1 = 0x00E0;       // internal counter ends sampling and starts conversion (auto-convert), manual sample
    AD1CON2 = 0;            // AD1CON2<15:13> set voltage reference to pins AVSS/AVDD
    AD1CON3 = 0x0f01;       // TAD = 4*TPB, acquisition time = 15*TAD
    AD1CON1SET = 0x8000;    // Enable ADC
} // END adcConfigureManual()

int analogRead(char analogPIN){
    AD1CHS = analogPIN << 16;       // AD1CHS<16:19> controls which analog pin goes to the ADC
 
    AD1CON1bits.SAMP = 1;           // Begin sampling
    while( AD1CON1bits.SAMP );      // wait until acquisition is done
    while( ! AD1CON1bits.DONE );    // wait until conversion done
 
    return ADC1BUF0;                // result stored in ADC1BUF0
}

void WriteByte(char c){
    DRV_USART0_WriteByte(c);
    //while(!DRV_USART0_ReceiverBufferIsEmpty()){DRV_USART0_ReadByte();}//to ignore garbage when transmitting
}


//This function is to write the AT messages that must be dealt with by the WiFi module.
void WriteString(char charArray[]){
    int index = 0;
    
    while (charArray[index] != '\0'){
        WriteByte(charArray[index]);
        index++;
    }
}
//This function is to write the message that must be received on the server
void WriteString2(char charArray[]){
    int boolean = 0;
    int index = 0;
    do{
        WriteByte(charArray[index]);
        index++;
        if(charArray[index] == '\0' && boolean == 1){
            WriteByte('\0');
            WriteByte('\r');
            WriteByte('\n');
        }
        boolean = 1;
    }while(charArray[index]!='\0');
}

void ReadByte(void){
    if(!DRV_USART0_ReceiverBufferIsEmpty()){
        //If the app should not decipher the incoming characters, just read them but don't do anything
        if(appData.readMode==0){
            DRV_USART0_ReadByte();
        }else if(appData.readMode==1){
            appData.rx_byte = DRV_USART0_ReadByte();
            DRV_USART1_WriteByte(appData.rx_byte);
            if(appData.rx_byte == 60){
                appData.readMode=0;
                appData.state = APP_STATE_WRITE_TO_WIFI;
            }
        }
    }
}

/* TODO:  Add any necessary local functions.
*/


// *****************************************************************************
// *****************************************************************************
// Section: Application Initialization and State Machine Functions
// *****************************************************************************
// *****************************************************************************

/*******************************************************************************
  Function:
    void APP_Initialize ( void )

  Remarks:
    See prototype in app.h.
 */

void APP_Initialize ( void )
{
    /* Place the App state machine in its initial state. */
    appData.state = APP_STATE_INIT;

    
    /* TODO: Initialize your application's state machine and other
     * parameters.
     */
}


/******************************************************************************
  Function:
    void APP_Tasks ( void )

  Remarks:
    See prototype in app.h.
 */

void APP_Tasks ( void )
{

    /* Check the application's current state. */
    switch ( appData.state )
    {
        /* Application's initial state. */
        case APP_STATE_INIT:
        {
            bool appInitialized = true;
       
        
            if (appInitialized)
            {
            
                appData.state = APP_STATE_CONNECT_TO_WIFI;
                appData.receivedCorrectByte=0;
                appData.storeBytePosition=0;
                appData.readMode=0;
                DRV_USART0_Initialize();
                adcConfigureManual();

                SYS_INT_SourceDisable(INT_SOURCE_USART_2_TRANSMIT);

                //SYS_INT_SourceDisable(interruptTransmit);
            }
            break;
        }

        case APP_STATE_CONNECT_TO_WIFI:
        {
            int i = 0;
            //Initiate connection
            for(i = 0; i< 80000000; i++){}
            WriteString("AT\r\n\0"); for(i = 0; i < 10000000; i++){}       
            WriteString("AT+CWMODE=1\r\n\0");    for(i = 0; i < 10000000; i++){}   
            WriteString("AT+CIPMODE=0\r\n\0"); for(i = 0; i < 10000000; i++){}   
            WriteString("AT+CWJAP=\"ESP Access Point 1\"\r\n\0"); for(i = 0; i < 10000000; i++){}   
            WriteString("AT+CIPSTART=\"TCP\",\"192.168.4.1\",333\r\n\0"); for(i = 0; i < 10000000; i++){}   

            appData.state = APP_STATE_WRITE_TO_WIFI;
            break;
        }
        case APP_STATE_WRITE_TO_WIFI:
        {
            //Code to convert sensor float to character
            char buffer[20] = "";
            appData.readMode=0;
            int sensorArray[5];
            int k = 0;
            int i = 0;
            int charPosition = 0;
            //j = j+0.01;
            //if (j >= 100.0){j = 0.0;}
            
            //j *= 100.0;
            for(i = 0; i < 16; i++){
                k += analogRead(0);//(int) j;
            }
            k = k/16;
            //j /= 100.0;
            for(charPosition=0; buffer[charPosition] != '\0'; charPosition++){}
            for(i = 0; i < 5; i++){sensorArray[i] = k%10; k/=10;}
            for (i = 4; i >= 0; i--){buffer[charPosition+i] = sensorArray[4-i] + '0';}
            //End of code that changes sensor float to character and puts it in the buffer to be sent
            //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            //Start of code to determine the correct length 
            //The following code initiates a TCP connection (even if one already exists))
            //then sends a send command with the length of the message (length array) to be sent)
            //It then sends the message (buffer))

            char length1[2]; char length2[3];
            WriteString("AT+CIPSTART=\"TCP\",\"192.168.4.1\",333\r\n\0"); for(i = 0; i < 1000000; i++){}
            WriteString("AT+CIPSEND=\0");
            for(i = 0; buffer[i] != '\0'; ++i){}            
            if(i > 10){
                length2[1] = (i%10)+'0'; 
                length2[0] = (i/10)+'0'; 
                WriteString(length2);
            }
            else{
                length1[0] = i + '0'; 
                length1[1] = '\0';
                WriteString(length1);
            }
            WriteString("\r\n\0"); for(i = 0; i < 1000000; i++){}
            WriteString2(buffer);
            appData.state = APP_STATE_READ_FROM_WIFI;
            appData.readMode = 1;
            break;
        }
        
        case APP_STATE_READ_FROM_WIFI:
        {
            
            break;
        }

        /* TODO: implement your application state machine.*/
        

        /* The default state should never be executed. */
        default:
        {
            /* TODO: Handle error in application's state machine. */
            break;
        }
    }
}

 

/*******************************************************************************
 End of File
 */
