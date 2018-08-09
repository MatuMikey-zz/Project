/*******************************************************************************
  Timer Static Driver File

  File Name:
    drv_tmr_static.c

  Company:
    Microchip Technology Inc.   

  Summary:
    Timer driver implementation for the static single instance driver.

  Description:
    The Timer device driver provides a simple interface to manage the Timer
    modules on Microchip microcontrollers.
    
  Remarks:
    None
 *******************************************************************************/

/*******************************************************************************
Copyright (c) 2014 released Microchip Technology Inc.  All rights reserved.

Microchip licenses to you the right to use, modify, copy and distribute
Software only when embedded on a Microchip microcontroller or digital signal
controller that is integrated into your product or third party product
(pursuant to the sublTMRense terms in the accompanying lTMRense agreement).

You should refer to the lTMRense agreement accompanying this Software for
additional information regarding your rights and obligations.

SOFTWARE AND DOCUMENTATION ARE PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF
MERCHANTABILITY, TITLE, NON-INFRINGEMENT AND FITNESS FOR A PARTTMRULAR PURPOSE.
IN NO EVENT SHALL MTMRROCHIP OR ITS LTMRENSORS BE LIABLE OR OBLIGATED UNDER
CONTRACT, NEGLIGENCE, STRTMRT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR
OTHER LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE OR
CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT OF
SUBSTITUTE GOODS, TECHNOLOGY, SERVTMRES, OR ANY CLAIMS BY THIRD PARTIES
(INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.
 *******************************************************************************/

// *****************************************************************************
// *****************************************************************************
// Header Includes
// *****************************************************************************
// *****************************************************************************
#include "driver/tmr/drv_tmr_static.h"
#include "driver/tmr/src/drv_tmr_variant_mapping.h"

typedef struct
{
    DRV_TMR_CALLBACK alarmFunc;  // For alarm registering
    uint32_t alarmCount;    // For AlarmHasElapsed function
    bool    alarmEnabled;   // For Enable/Disable function
    bool    alarmPeriodic;      // Keep Alarm enabled or disable it
    uintptr_t   alarmContext;   // For Alarm Callback
    uint32_t    alarmPeriod;    // For Period Set/Get
} DRV_TMR_ALARM_OBJ;

static bool _DRV_TMR_ClockSourceSet(TMR_MODULE_ID timerId, DRV_TMR_CLK_SOURCES clockSource)
{
    bool clockSet = true;
    /* Clock Source Selection */
    if(clockSource == DRV_TMR_CLKSOURCE_INTERNAL)
    {
        if ( PLIB_TMR_ExistsClockSource ( timerId ) )
        {               
            PLIB_TMR_ClockSourceSelect ( timerId, TMR_CLOCK_SOURCE_PERIPHERAL_CLOCK );           
        }
        else
        {
            /* If clock source feature doesn't exist for any specific timer module instance,
            then by default internal peripheral clock is considered as timer source, so do nothing */ 
        }
    }
    /* External Synchronous Clock Source Selection */
    else if(!(clockSource & 0x10))
    {
        if ( PLIB_TMR_ExistsClockSource ( timerId ) )
        {               
            if ( PLIB_TMR_ExistsClockSourceSync ( timerId )  )
            {
                PLIB_TMR_ClockSourceSelect ( timerId, (TMR_CLOCK_SOURCE)(clockSource & 0x0F) );                
                PLIB_TMR_ClockSourceExternalSyncEnable ( timerId );                    
            }
            /* If Synchronization feature doesn't exist for any specific timer module 
            instance with external clock source then it is synchronous by default */
            else if (clockSource == DRV_TMR_CLKSOURCE_EXTERNAL_SYNCHRONOUS)
            {
                PLIB_TMR_ClockSourceSelect ( timerId, TMR_CLOCK_SOURCE_EXTERNAL_INPUT_PIN );
            }
            else
            {
                clockSet = false;
            }  
        }
        else
        {
            clockSet = false;
        }        
    }
    /* External Asynchronous Clock Source Selection */
    else if(clockSource & 0x10)
    {
        if ( PLIB_TMR_ExistsClockSourceSync ( timerId ) )
        {
            PLIB_TMR_ClockSourceSelect ( timerId, (TMR_CLOCK_SOURCE)(clockSource & 0x0F) );
            PLIB_TMR_ClockSourceExternalSyncDisable ( timerId );
        }
        else
        {
            clockSet = false;
        }        
    }
    
    return clockSet;
}

// Prescaler selection
static bool _DRV_TMR_ClockPrescaleSet(TMR_MODULE_ID timerId, TMR_PRESCALE  prescale)
{
    if( PLIB_TMR_ExistsPrescale( timerId ) )
    {
        PLIB_TMR_PrescaleSelect( timerId , prescale );
        return true;
    }
    return false;
}


 
 
/*******************************************************************************
 End of File
*/
