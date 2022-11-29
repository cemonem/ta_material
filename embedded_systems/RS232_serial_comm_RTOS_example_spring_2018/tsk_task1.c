#include "common.h"

/**********************************************************************
 * ----------------------- GLOBAL VARIABLES ---------------------------
 **********************************************************************/

char data[40];
char data_size;
/**********************************************************************
 * ----------------------- LOCAL FUNCTIONS ----------------------------
 **********************************************************************/


/**********************************************************************
 * ------------------------------ TASK1 -------------------------------
 *
 * Basic echo function test. Type $hello: in cutecom and receive hello
 *
 **********************************************************************/
TASK(TASK1) 
{
    
    SetRelAlarm(ALARM_TSK1, 100, 50);
	while(1) {
        WaitEvent(ALARM_EVENT);
        ClearEvent(ALARM_EVENT);
        data_size = receiveBuffer_pop(data);
        if(data_size != 0)
        {
            transmitBuffer_push(data,data_size);
        }
	}
	TerminateTask();
}

/* End of File : tsk_task1.c */