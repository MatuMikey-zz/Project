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
// *****************************************************************************
char receiveBuffer[256] = "";
int receiveCount = 0;
bool messageReceived = false;
float sensorInput1, sensorInput2, time, R1, R2, T1, T2 = 0;
volatile int output = 0;
volatile float output1= 0;
float input[3] ={0};
volatile int j  = 0;
char buffer[20] = ""; //buffer that will send message
float weights[25] = {-0.488584, -0.487506, 0.257308, 0.535324, 0.072668, 0.971318, -0.256243, -0.150798, -0.801023, 0.166424, -0.799493, 0.242513, -0.998435, 0.4894, -0.81544, 0.703735, -0.232988, 0.376172, 0.889129, 0.636903, -0.414912, -0.387571, 0.447373, -0.822581, 0.822224};
volatile int weightCounter = 0;
volatile float outputs[6] = {0,0,0,0,0,0};


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
    ANSELBbits.ANSB0, ANSELBbits.ANSB1 = 1;   // set RB3 (AN5) to analog
    TRISBbits.TRISB0, TRISBbits.TRISB1 = 1;   // set RB3 as an input
    //TRISBbits.TRISB5 = 0;   // set RB5 as an output (note RB5 is a digital only pin)
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
        }else if(appData.readMode==1){//If the app should do something with incoming data
            appData.rx_byte = DRV_USART0_ReadByte();
            if (appData.rx_byte == 0x01){
                messageReceived = true;
            }
            if(messageReceived){
                receiveBuffer[receiveCount] = appData.rx_byte;
                receiveCount++;
            }

            //DRV_USART1_WriteByte(appData.rx_byte);
            if(receiveCount == receiveBuffer[1] && messageReceived){
                messageReceived = false;
                receiveCount = 0;
                appData.receivedData = true;
                appData.sensorData[0] = (int) receiveBuffer[2];
                appData.sensorData[1] = (int) receiveBuffer[3];
                appData.sensorData[2] = (int) receiveBuffer[4];
                appData.sensorData[3] = (int) receiveBuffer[5];
                appData.sensorData[4] = (int) receiveBuffer[6];
                appData.sensorData[5] = (int) receiveBuffer[7];
                
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
                appData.receivedData = false;
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
            for(i = 0; i< 120000000; i++){}     
            WriteString("AT+CWMODE=1\r\n\0");    for(i = 0; i < 10000000; i++){}   
            WriteString("AT+CIPMODE=0\r\n\0"); for(i = 0; i < 10000000; i++){}   
            //WriteString("AT+CWJAP_DEF=\"ESP Access Point 1\",\"\"\r\n\0"); for(i = 0; i < 80000000; i++){}   
            WriteString("AT+CIPSTART=\"TCP\",\"192.168.4.1\",333\r\n\0"); for(i = 0; i < 10000000; i++){}   

            appData.state = APP_STATE_WRITE_TO_WIFI;
            break;
        }
        case APP_STATE_WRITE_TO_WIFI:
        {
            //Necessary local variables
            char ID = 0x01; //ID of this module
            char CMD = 0x01; //Command ID
            buffer[0] = ID;
            buffer[1] = CMD;
            appData.readMode=0;
            int k,l = 0; //Variables to store analog sensor readings
            int i = 0;

            

            
            //Read sensors then get the average between them and then store them in buffer
            for(i = 0; i < 16; i++){
                k += analogRead(0);
                l += analogRead(1);
            }
            k = k/16;
            l = l/16;
            k = (k+l)/2;
            buffer[3] = k%256; //low byte
            k = k/256;
            buffer[2] = k;
            
            if(appData.receivedData){
                sensorInput1 = (float) appData.sensorData[0]*256 + appData.sensorData[1];
                R1 = 1000.0/((1023.0/(1023-sensorInput1))-1.0);
                T1 = (1.0/((1.0/298.15)+(1.0/3800.0)*(log(R1/1000.0)))-273.15)/45.0;
                sensorInput2 = (float)appData.sensorData[2]*256 + appData.sensorData[3];
                R2 = 1000.0/((1023.0/(1023-sensorInput2))-1.0);
                T2 = (1.0/((1.0/298.15)+(1.0/3800.0)*(log(R2/1000.0)))-273.15)/45.0;
                time = (float) (appData.sensorData[4]*256*256 + appData.sensorData[5]*256 + appData.sensorData[6])/86400.0;
                //Neural Network starts here
                input[0] = T1; input[1] = T2; input[2] = time;
                
                for(i = 0; i < 6; i++){//For every weight of an input node that must connect to a hidden node (except bias))
                    for (j = 0; j < 3; j++){ //For every input node
                        outputs[i] = outputs[i] + input[j]*weights[3*i+j];
                    }
                    outputs[i] = outputs[i]/(1+fabs(outputs[i])); //"activate" the neuron
                }
                for (i = 0; i < 6; i++){//For every hidden node and the bias that must connect to the output node
                    output1 = output1 + outputs[i]*weights[18+i];
                    weightCounter = weightCounter+1;
                }
                output1 = output1 + 1.0*weights[24];
                output1 = output1*45.0; // linear output
                output = output1*100;
                
                buffer[5] = output%100;
                output = output/100;
                buffer[4] = output; 
                output1 = 0; for(i = 0; i < 6; i++){outputs[i] = 0;}
            }
            //Neural network
            
            //
            //End of code that changes sensor float to character and puts it in the buffer to be sent
            //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            //Start of code to determine the correct length 
            //The following code initiates a TCP connection (even if one already exists))
            //then sends a send command with the length of the message (length array) to be sent)
            //It then sends the message (buffer)) and changes the state to 

            char length1[2]; char length2[3];
            WriteString("AT+CIPSTART=\"TCP\",\"192.168.4.1\",333\r\n\0"); for(i = 0; i < 1000000; i++){}
            //WriteString("AT+CIPSTART=\"TCP\",\"192.168.4.1\",333\r\n\0"); for(i = 0; i < 1000000; i++){}
            //WriteString("AT+CIPSTART=\"TCP\",\"192.168.4.1\",333\r\n\0"); for(i = 0; i < 1000000; i++){}
            WriteString("AT+CIPSEND=\0");
            for(i = 0; buffer[i] != '\0'; ++i){}            
            if(i > 10){ //This is a piece of magic code that nobody knows what it does. Don't touch it.
                length2[1] = (i%10)+'0'; 
                length2[0] = (i/10)+'0'; 
                WriteString(length2);
            }else if (appData.receivedData){ //Write data with neural network output
                length1[0] = 6 + '0';
                length1[1] = '\0';
                WriteString(length1);
            }
            else{ //write data with just sensor output
                length1[0] = 4 + '0'; 
                length1[1] = '\0';
                WriteString(length1);
            }
            WriteString("\r\n\0"); for(i = 0; i < 1000000; i++){}
            WriteString2(buffer);
            for(i = 0; i < 500000; i++);
            appData.state = APP_STATE_READ_FROM_WIFI;
            appData.readMode = 1; //Set mode to read mode
            appData.receivedData = false;
            break;
        }
        
        case APP_STATE_READ_FROM_WIFI:
        {
            //Wait to read data
            break;
        }

        

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
