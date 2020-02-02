/*

* Hand gesture project.
* Creators: Mikko Koivula and Mikael Karvonen 

 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* XDCtools Header files */
#include <xdc/std.h>
#include <xdc/runtime/System.h>
#include <ti/sysbios/BIOS.h>
#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Task.h>
#include <ti/drivers/I2C.h>
#include <ti/drivers/i2c/I2CCC26XX.h>
#include <ti/drivers/PIN.h>
#include <ti/drivers/pin/PINCC26XX.h>

/* Board Header files */
#include "Board.h"
#include "sensors/mpu9250.h"
/*KELLO*/
#include <ti/sysbios/knl/Clock.h>

#define STACKSIZE 4096
Char taskStack[STACKSIZE];

float printti(float x_lista[]);

// *******************************
//
// MPU GLOBAL VARIABLES
//
// *******************************

int nappi;
int sensorit;
int highfive = 0;
static PIN_Handle buttonHandle;
static PIN_State buttonState;
PIN_Config buttonConfig[] = {
   Board_BUTTON0  | PIN_INPUT_EN | PIN_PULLUP | PIN_IRQ_NEGEDGE, // Hox! TAI-operaatio
   PIN_TERMINATE
};

Void clkFxn(UArg arg0) {
    if (nappi == 1){
        sensorit = 1;
    
    }
}

void buttonFxn(PIN_Handle handle, PIN_Id pinId) {
   if(pinId == Board_BUTTON0) {
        if (sensorit == 0){
            //System_printf("nappi painettu\n");
            //System_flush();
            sensorit = 1;
        }
       
        //nappi = 0;
        
   }
}


static PIN_Handle hMpuPin;
static PIN_State MpuPinState;
static PIN_Config MpuPinConfig[] = {
    Board_MPU_POWER  | PIN_GPIO_OUTPUT_EN | PIN_GPIO_HIGH | PIN_PUSHPULL | PIN_DRVSTR_MAX,
    PIN_TERMINATE
};



// *******************************
//
// MPU9250 I2C CONFIG
//
// *******************************
static const I2CCC26XX_I2CPinCfg i2cMPUCfg = {
    .pinSDA = Board_I2C0_SDA1,
    .pinSCL = Board_I2C0_SCL1
};

// SENSOR TASK
Void sensorFxn(UArg arg0, UArg arg1) {

    // *******************************
    //
    // USE TWO DIFFERENT I2C INTERFACES
    //
    // *******************************
    I2C_Handle i2c; // INTERFACE FOR OTHER SENSORS
    I2C_Params i2cParams;
    I2C_Handle i2cMPU; // INTERFACE FOR MPU9250 SENSOR
    I2C_Params i2cMPUParams;

    float ax, ay, az, gx, gy, gz;
    double pres,temp;
    char str[80];
    int i = 0;
    float ax_data[100];
    float ay_data[100];
    float az_data[100];
    float gx_data[100];
    float gy_data[100];
    float gz_data[100];
    int s = 0;
    int nousu;


    char h[50];
    int j;
    int v = 0;  
    I2C_Params_init(&i2cParams);
    i2cParams.bitRate = I2C_400kHz;

    I2C_Params_init(&i2cMPUParams);
    i2cMPUParams.bitRate = I2C_400kHz;
    i2cMPUParams.custom = (uintptr_t)&i2cMPUCfg;

    // *******************************
    //
    // MPU OPEN I2C
    //
    // *******************************
    i2cMPU = I2C_open(Board_I2C, &i2cMPUParams);
    if (i2cMPU == NULL) {
        System_abort("Error Initializing I2CMPU\n");
    }

    // *******************************
    //
    // MPU POWER ON
    //
    // *******************************
    PIN_setOutputValue(hMpuPin,Board_MPU_POWER, Board_MPU_POWER_ON);

    // WAIT 100MS FOR THE SENSOR TO POWER UP
    Task_sleep(100000 / Clock_tickPeriod);
    System_printf("MPU9250: Power ON\n");
    System_flush();

    // *******************************
    //
    // MPU9250 SETUP AND CALIBRATION
    //
    // *******************************
    System_printf("MPU9250: Setup and calibration...\n");
    System_flush();

    mpu9250_setup(&i2cMPU);

    System_printf("MPU9250: Setup and calibration OK\n");
    System_flush();

    // *******************************
    //
    // MPU CLOSE I2C
    //
    // *******************************
    I2C_close(i2cMPU);
    // LOOP FOREVER
    while (1) {
    if (sensorit == 1){
        while (1) {
    
    
            // *******************************
            //
            // MPU OPEN I2C
            //
            // *******************************
            i2cMPU = I2C_open(Board_I2C, &i2cMPUParams);
            if (i2cMPU == NULL) {
                System_abort("Error Initializing I2CMPU\n");
            }
    
            // *******************************
            //
            // MPU ASK DATA
            //
            //    Accelerometer values: ax,ay,az
            //    Gyroscope values: gx,gy,gz
            //
            // *******************************
            mpu9250_get_data(&i2cMPU, &ax, &ay, &az, &gx, &gy, &gz);
    
            
            // DO SOMETHING WITH THE DATA
            
            if (i > 40 && i < 141){
                ax_data[i-40] = ax;
                ay_data[i-40] = ay;
                az_data[i-40] = az;
                gx_data[i-40] = gx;
                gy_data[i-40] = gy;
                gz_data[i-40] = gz;
                }
                
            i++;
            if (i == 140){
                
                
                sensorit = 0;
            
                for (j = 0; j < (sizeof(ax_data) / sizeof(ax_data[0])); j++){
                    
                    if (s == 13){
                        nousu = 1;
                      }
                    if (az_data[j] < az_data[j-1]){
                        s = 0;
                     }
                    if (az_data[j] > 0.5){
                        s++;
                        }
                    if (az_data[j] < 0.5){
                        s = 0;
                    }
                
                    if (((ax_data[j] < 0 | ax_data[j] > 2) && (az_data[j] > 4 | az_data[j] < -4) && (gy_data[j] < -200 | gy_data[j] > 150)) && nousu == 1) {
                           highfive = 1; 
                        }
                        
                    
                    v++;
                    sprintf(h, "%d,%f,%f,%f,%f,%f,%f\n", v, ax_data[j], ay_data[j], az_data[j], gx_data[j], gy_data[j], gz_data[j]);
                    System_printf(h);
                    System_flush();

                    
                    
                    }; 
                if (highfive == 1){
                   
                    System_printf("OLIPAS KOVA LYÖNTI!\n");
                    System_flush(); 
                    highfive = 0; 
                }
                
                ax_data[i] = 0;
                ay_data[i] = 0;
                az_data[i] = 0;
                gx_data[i] = 0;
                gy_data[i] = 0;
                gz_data[i] = 0;
                v = 0;
                nousu = 0;
            };
            
            I2C_close(i2cMPU);
    
            // WAIT 30MS
            Task_sleep(10000 / Clock_tickPeriod);
            if (i == 140) {
                i = 0;
                
                break;
            }
            //nappi = 0;
        }
    }
    }
    // MPU9250 POWER OFF 
    // Because of loop forever, code never goes here

    PIN_setOutputValue(hMpuPin,Board_MPU_POWER, Board_MPU_POWER_OFF);
}



int main(void) {
    Task_Handle task;
    Task_Params taskParams;
    
    // RTOS:n kellomuuttujat
    Clock_Handle clkHandle;
    Clock_Params clkParams;
    
    Board_initGeneral();
    Board_initI2C();
    
    Clock_Params_init(&clkParams);
    clkParams.period = 1000000 / Clock_tickPeriod;
    clkParams.startFlag = TRUE;

   // Luodaan kello
   clkHandle = Clock_create((Clock_FuncPtr)clkFxn, 1000000 / Clock_tickPeriod, &clkParams, NULL);
   if (clkHandle == NULL) {
      System_abort("Clock create failed");
   }
    
    buttonHandle = PIN_open(&buttonState, buttonConfig);
    if(!buttonHandle) {
      System_abort("Error initializing button pins\n");
      
    }
    if (PIN_registerIntCb(buttonHandle, &buttonFxn) != 0) {
        System_abort("Error registering button callback function");
        }
    // *******************************
    //
    // OPEN MPU POWER PIN
    //
    // *******************************
    hMpuPin = PIN_open(&MpuPinState, MpuPinConfig);
    if (hMpuPin == NULL) {
        System_abort("Pin open failed!");
    }

    Task_Params_init(&taskParams);
    taskParams.stackSize = STACKSIZE;
    taskParams.stack = &taskStack;
    task = Task_create((Task_FuncPtr)sensorFxn, &taskParams, NULL);
    if (task == NULL) {
        System_abort("Task create failed!");
    }

    /* Start BIOS */
    BIOS_start();

    return (0);
}