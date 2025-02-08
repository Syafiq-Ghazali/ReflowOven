; 76E003 ADC_Pushbuttons.asm: Reads push buttons using the ADC, AIN0 in P1.7

$NOLIST
$MODN76E003
$LIST

;  N76E003 pinout:
;                               -------
;       PWM2/IC6/T0/AIN4/P0.5 -|1    20|- P0.4/AIN5/STADC/PWM3/IC3
;               TXD/AIN3/P0.6 -|2    19|- P0.3/PWM5/IC5/AIN6
;               RXD/AIN2/P0.7 -|3    18|- P0.2/ICPCK/OCDCK/RXD_1/[SCL]
;                    RST/P2.0 -|4    17|- P0.1/PWM4/IC4/MISO
;        INT0/OSCIN/AIN1/P3.0 -|5    16|- P0.0/PWM3/IC3/MOSI/T1
;              INT1/AIN0/P1.7 -|6    15|- P1.0/PWM2/IC2/SPCLK
;                         GND -|7    14|- P1.1/PWM1/IC1/AIN7/CLO
;[SDA]/TXD_1/ICPDA/OCDDA/P1.6 -|8    13|- P1.2/PWM0/IC0
;                         VDD -|9    12|- P1.3/SCL/[STADC]
;            PWM5/IC7/SS/P1.5 -|10   11|- P1.4/SDA/FB/PWM1
;                               -------
;

CLK               EQU 16600000 ; Microcontroller system frequency in Hz
BAUD              EQU 115200 ; Baud rate of UART in bps
TIMER1_RELOAD     EQU (0x100-(CLK/(16*BAUD)))
TIMER0_RELOAD_1MS EQU (0x10000-(CLK/1000))
TIMER2_RATE		  EQU 100
TIMER2_RELOAD     EQU (65536-(CLK/(16*TIMER2_RATE)))

      

ORG 0x0000
	ljmp main
org 0x002B
	ljmp Timer2_ISR

;              1234567890123456    <- This helps determine the location of the counter

start:     db 'SBFF Press Start', 0 
Blank:     db '                ', 0
Values:    db 'State:', 0
Values1:   db 'Runt:', 0
Values2:   db 'Run:', 0
Blank1:    db ' ', 0

AbortMsg:  db '  ***ABORTED***  ',0
AbortMsgnd:db '   **FAILED**    ',0
celsius:   db 'C', 0

cseg
; These 'equ' must match the hardware wiring
LCD_RS equ P1.3
LCD_E  equ P1.4
LCD_D4 equ P0.0
LCD_D5 equ P0.1
LCD_D6 equ P0.2
LCD_D7 equ P0.3
PWM_OUT EQU P1.0 

$NOLIST
$include(LCD_4bit.inc) ; A library of LCD related functions and utility macros
$include(math32.inc)
$LIST

BSEG
; These eight bit variables store the value of the pushbuttons after calling 'ADC_to_PB' below
PB0: dbit 1
PB1: dbit 1
PB2: dbit 1
PB3: dbit 1
PB4: dbit 1
PB5: dbit 1
PB6: dbit 1
PB7: dbit 1
s_flag: dbit 1
mf: dbit 1


DSEG at 30H ; Before the state machine!
state: ds 1
temp_soak: ds 2
time_soak: ds 2
Temp_refl: ds 2
Time_refl: ds 2
Temp_cool: ds 2
pwm: ds 1
sec: ds 5
FSM1_state: ds 1
temp: ds 5
time: ds 5
pwm_counter: ds 1
runtime: ds 2
temp_safety: ds 1

x: ds 4
y: ds 4
bcd: ds 5



CSEG
Init_All:
	; Configure all the pins for biderectional I/O
	mov	P3M1, #0x00
	mov	P3M2, #0x00
	mov	P1M1, #0x00
	mov	P1M2, #0x00
	mov	P0M1, #0x00
	mov	P0M2, #0x00
	
	orl	CKCON, #0x10 ; CLK is the input for timer 1
	orl	PCON, #0x80 ; Bit SMOD=1, double baud rate
	mov	SCON, #0x52
	anl	T3CON, #0b11011111
	anl	TMOD, #0x0F ; Clear the configuration bits for timer 1
	orl	TMOD, #0x20 ; Timer 1 Mode 2
	mov	TH1, #TIMER1_RELOAD ; TH1=TIMER1_RELOAD;
	setb TR1
	
	; Using timer 0 for delay functions.  Initialize here:
	clr	TR0 ; Stop timer 0
	orl	CKCON,#0x08 ; CLK is the input for timer 0
	anl	TMOD,#0xF0 ; Clear the configuration bits for timer 0
	orl	TMOD,#0x01 ; Timer 0 in Mode 1: 16-bit timer
	
	; Initialize and start the ADC:
	
	; AIN0 is connected to P1.7.  Configure P1.7 as input.
	orl	P1M1, #0b10000010
	anl	P1M2, #0b01111101
	
	; AINDIDS select if some pins are analog inputs or digital I/O:
	orl AINDIDS, #0b10000010
	orl ADCCON1, #0x01 ; Enable ADC
	
	; Initialize timer 2 for periodic interrupts
	mov T2CON, #0 ; Stop timer/counter. Autoreload mode.
	mov TH2, #high(TIMER2_RELOAD)
	mov TL2, #low(TIMER2_RELOAD)
; Set the reload value
	mov T2MOD, #0b1010_0000 ; Enable timer 2 autoreload, and clock divider is 16
	mov RCMP2H, #high(TIMER2_RELOAD)
	mov RCMP2L, #low(TIMER2_RELOAD)
; Init the free running 10 ms counter to zero
	mov pwm_counter, #0
	; Enable the timer and interrupts
	orl EIE, #0x80 ; Enable timer 2 interrupt ET2=1
	setb TR2 ; Enable timer 2
	setb EA ; Enable global interrupts
	
	ret
	
putchar:
    jnb TI, putchar
    clr TI
    mov SBUF, a
    ret

	
wait_1ms:
	clr	TR0 ; Stop timer 0
	clr	TF0 ; Clear overflow flag
	mov	TH0, #high(TIMER0_RELOAD_1MS)
	mov	TL0,#low(TIMER0_RELOAD_1MS)
	setb TR0
	jnb	TF0, $ ; Wait for overflow
	ret

; Wait the number of miliseconds in R2
waitms:
	lcall wait_1ms
	djnz R2, waitms
	ret

ADC_to_PB:
	anl ADCCON0, #0xF0
	orl ADCCON0, #0x00 ; Select AIN0
	
	clr ADCF
	setb ADCS   ; ADC start trigger signal
    jnb ADCF, $ ; Wait for conversion complete

	setb PB7
	setb PB6
	setb PB5
	setb PB4
	setb PB3
	setb PB2
	setb PB1
	setb PB0
	
	; Check PB7
ADC_to_PB_L7:
	clr c
	mov a, ADCRH
	subb a, #0xf0
	jc ADC_to_PB_L6
	clr PB7
	ret

	; Check PB6
ADC_to_PB_L6:
	clr c
	mov a, ADCRH
	subb a, #0xd0
	jc ADC_to_PB_L5
	clr PB6
	ret

	; Check PB5
ADC_to_PB_L5:
	clr c
	mov a, ADCRH
	subb a, #0xb0
	jc ADC_to_PB_L4
	clr PB5
	ret

	; Check PB4
ADC_to_PB_L4:
	clr c
	mov a, ADCRH
	subb a, #0x90
	jc ADC_to_PB_L3
	clr PB4
	ret

	; Check PB3
ADC_to_PB_L3:
	clr c
	mov a, ADCRH
	subb a, #0x70
	jc ADC_to_PB_L2
	clr PB3
	ret

	; Check PB2
ADC_to_PB_L2:
	clr c
	mov a, ADCRH
	subb a, #0x50
	jc ADC_to_PB_L1
	clr PB2
	ret

	; Check PB1
ADC_to_PB_L1:
	clr c
	mov a, ADCRH
	subb a, #0x30
	jc ADC_to_PB_L0
	clr PB1
	ret

	; Check PB0
ADC_to_PB_L0:
	clr c
	mov a, ADCRH
	subb a, #0x10
	jc ADC_to_PB_Done
	clr PB0
	ret
	
ADC_to_PB_Done:
	; No pusbutton pressed	
	ret
	
;---------------------------------;
; ISR for timer 2 ;
;---------------------------------;
Timer2_ISR:
	clr TF2 ; Timer 2 doesn't clear TF2 automatically. Do it in the ISR. It is bit addressable.
	push psw
	push acc
	inc pwm_counter
	clr c
	mov a, pwm
	subb a, pwm_counter ; If pwm_counter <= pwm then c=1
	cpl c
	mov PWM_OUT, c
	mov a, pwm_counter
	cjne a, #100, Timer2_ISR_done
	mov pwm_counter, #0
	
	mov a, sec
	add a, #1
	da a
	mov sec, a
	cjne a, #0x99, runtimeinc
	mov sec, #0
	
runtimeinc:
	mov a, runtime
	add a, #1
	da a
	mov runtime, a
	cjne a, #0x99, Timer2_ISR_done1
	mov runtime, #0	
	mov a, runtime+1
	add a, #1
	da a
	mov runtime+1, a
	cjne a, #0x99, Timer2_ISR_done1	
	mov runtime+1, #0

Timer2_ISR_done:
	pop acc
	pop psw
	reti

Timer2_ISR_done1:
	pop acc
	pop psw
	reti

tempcalc:
	anl ADCCON0, #0xF0
	orl ADCCON0, #0x07 ; Select channel 7
	clr ADCF
	setb ADCS ;  ADC start trigger signal
    jnb ADCF, $ ; Wait for conversion complete
    
    ; Read the ADC result and store in [R1, R0]
    mov a, ADCRH   
    swap a
    push acc
    anl a, #0x0f
    mov R1, a
    pop acc
    anl a, #0xf0
    orl a, ADCRL
    mov R0, A
    
 	mov x+0, R0
	mov x+1, R1
	mov x+2, #0
	mov x+3, #0
	Load_y(50300) ; VCC voltage measured
	lcall mul32
	Load_y(4095) ; 2^12-1
	lcall div32
	
	Load_y(100)
	lcall mul32
	Load_y(2730000) ;floating point conversion (idk search this up)
	lcall sub32
	lcall hex2bcd
	
	mov R2, #99
	lcall waitms

	
    ret
    
Send_BCD mac
	push ar0
	mov r0, %0
	lcall ?Send_BCD
	pop ar0
endmac

?Send_BCD:
	push acc
	; Write most significant digit
	mov a, r0
	swap a
	anl a, #0fh
	orl a, #30h
	
	lcall putchar
; write least significant digit
	mov a, r0
	anl a, #0fh
	orl a, #30h
	lcall putchar
	pop acc
	ret

	
abort:
	mov FSM1_state, #0
	Set_Cursor(1,1)
	Send_Constant_String(#AbortMsg)
	Set_Cursor(2,1)
	Send_Constant_String(#AbortMsgnd)
	mov R2, #250
	lcall waitms
	Set_Cursor(1,1)
	Send_Constant_String(#Blank)
	Set_Cursor(2,1)
	Send_Constant_String(#Blank)
	mov R2, #250
	lcall waitms
	ret
	
Startmenu:
	Set_Cursor(1,1)
	Send_Constant_String(#Start)		
	Set_Cursor(2,1)
	Display_BCD(temp_soak+1)
	Set_Cursor(2,3)
	Display_BCD(temp_soak)
	Set_Cursor(2,6)
	Display_BCD(time_soak)
	Set_Cursor(2,10)
	Display_BCD(Temp_refl+1)
	Set_Cursor(2,12)
	Display_BCD(Temp_refl)
	Set_Cursor(2,15)
	Display_BCD(Time_refl)
	Set_Cursor(2,5)
	Send_Constant_String(#Blank1)
	Set_Cursor(2,8)
	Send_Constant_String(#Blank1)
	Set_Cursor(2,9)
	Send_Constant_String(#Blank1)
	Set_Cursor(2,14)
	Send_Constant_String(#Blank1)
	ret
	
Statmenu:
	Set_Cursor(1,1)
	Send_Constant_String(#Values)
	Set_Cursor(2,1)
	Send_Constant_String(#Values1)
	Set_Cursor(2,11)
	Send_Constant_String(#Values2)
	Set_Cursor(1,9)
	Send_Constant_String(#Blank1)
	Set_Cursor(1,10)
	Send_Constant_String(#Blank1)
	Set_Cursor(2,10)
	Send_Constant_String(#Blank1)
	Set_Cursor(1,16)
	Send_Constant_String(#Blank1)
	Set_Cursor(1,7)
	Display_BCD(FSM1_state)
	Set_Cursor(1,10)
	Display_BCD(bcd+4)	
	Display_BCD(bcd+2)
	Set_Cursor(1,14)
	Send_Constant_String(#celsius)
	Set_Cursor(1,15)
	Send_Constant_String(#Blank1)
	Set_Cursor(2,6)
	Display_BCD(runtime+1)
	Set_Cursor(2,8)
	Display_BCD(runtime)
	Set_Cursor(2,15)
	Display_BCD(sec)
	Set_Cursor(1,14)
ret	 
		
	
main:
	mov sp, #0x7f
	lcall Init_All
    lcall LCD_4BIT
    mov sec, #0
    mov temp_safety, #0x50
    mov runtime, #0
    mov runtime+1, #0
    mov temp_soak, #0x50 ;I hate the 8051 -> 220 and 150 greator than 8 bits so must use 16 bits
    mov temp_soak+1, #0x01
	mov time_soak, #0x60
	mov Temp_refl, #0x20
	mov Temp_refl+1, #0x02
	mov Time_refl, #0x45
	mov Temp_cool, #0x60
	mov FSM1_state, #0x00
	mov temp, #0x00
	mov temp+1, #0x00
	
Forever:
BeginMenu:
	lcall StartMenu
		
ljmp NewDisplayeEnd
FSM1:
	lcall Statmenu
	

NewDisplayeEnd:
	lcall tempcalc

	Send_BCD (bcd+4)
	Send_BCD (bcd+2)
	mov a, #'\n'
	lcall putchar

TimeSoakbutton:
	lcall ADC_to_PB
	mov c, PB2
	jc Timereflbutton
	mov a, time_soak
;	Wait_Milli_Seconds(#99)
	add a, #1
	da a
	mov time_soak, a
	cjne a, #0x99, TimeSoakbuttondone
	mov a, #0x00
TimeSoakbuttondone:
	mov time_soak, a

Timereflbutton:
	lcall ADC_to_PB
	mov c, PB0
	jc Tempsoakbutton
	mov a, Time_refl
;	Wait_Milli_Seconds(#99)
	add a, #1
	da a
	mov Time_refl, a
	cjne a, #0x99, Timereflbuttondone
	mov a, #0x00
Timereflbuttondone:
	mov Time_refl, a
	
Tempsoakbutton:
	lcall ADC_to_PB
	mov c, PB3
	jc Tempreflbutton
    mov a, temp_soak
 ;   Wait_Milli_Seconds(#99)
    add a, #1
    da a
    mov temp_soak, a
    cjne a, #0x00, Tempreflbutton
    mov a, temp_soak+1
    add a, #1
    da a
    mov temp_soak+1, a
    cjne a, #0x10, Tempreflbutton
    mov temp_soak+1, #0x00
    
Tempreflbutton:
	lcall ADC_to_PB
	mov c, PB1
	jc restart
    mov a, Temp_refl
;    Wait_Milli_Seconds(#99)
    add a, #1
    da a
    mov Temp_refl, a
    cjne a, #0x00, restart
    mov a, Temp_refl+1
    add a, #1
    da a
    mov Temp_refl+1, a
    cjne a, #0x10, restart
    mov Temp_refl+1, #0x00
    
restart:
	lcall ADC_to_PB
	mov c, PB6
	jc FSM1_state0
	mov FSM1_state, #0

mov a, FSM1_state	
FSM1_state0:		;Go to state 1 if PB6 is pushed ;INTIAL;
					;Set power to 0%
	mov a, FSM1_state
	cjne a, #0, FSM1_state1
	mov pwm, #0
	mov runtime, #0
	mov runtime+1, #0
	lcall ADC_to_PB
	mov c, PB7
	jc FSM1_state1
	mov FSM1_state, #1
	
FSM1_state1:		;Stay in state 1 if temp<=150 ;RAMP TO SOAK;
					;go to state 2 if temp > 150
					;Set Power = 100&% and Sec = 0
	cjne a, #1, FSM1_state2
	mov pwm, #100
	mov sec, #0
    mov a, temp_soak
    clr c
    subb a, bcd+2
    mov a, temp_soak+1
    subb a, bcd+4
	jnc FSM1_state1_check_for_temp
	mov FSM1_state, #2
	ljmp FSM1_state3_done
FSM1_state1_check_for_temp:
	mov a, runtime
	cjne a, #0x60, FSM1_state1_done
	mov a, temp_safety
	clr c
	subb a, temp
	jnc abortmessage
	ljmp FSM1_state1_done
abortmessage:
	lcall abort
	lcall abort
	lcall abort

FSM1_state1_done:
	ljmp FSM1

FSM1_state2:		;Stay in State 2 if Sec<=60 ;PREHEAT/SOAK;
					;Go to state 3 if Sec > 60
					;Set Power = 20%
	cjne a, #2, FSM1_state3
	mov pwm, #20
	mov a, time_soak
	clr c
	subb a, sec
	jnc FSM1_state2_done
	mov FSM1_state, #3
FSM1_state2_done:
	ljmp FSM1

FSM1_state3:		;Stay in state 3 if temp<=220 ;RAMP TO PEAK;
					;Go to state 4 if temp>220
					;Power =100% Sec = 0
	cjne a, #3, FSM1_state4
	mov pwm, #100
	mov time, #0
    mov a, Temp_refl
    clr c
    subb a, bcd+2
    mov a, Temp_refl+1
    subb a, bcd+4
	jnc FSM1_state3_done 
	mov FSM1_state, #4
FSM1_state3_done:
	ljmp FSM1

FSM1_state4:		;Stay in state 4 if Sec <=45 :REFLOW:
					; Go to state 5 if sec > 45
					;Power = 20%
	cjne a, #4, FSM1_state5
	mov pwm, #20
	clr c
	mov a, Time_refl
	subb a, sec
	jnc FSM1_state4_done
	mov FSM1_state, #5
FSM1_state4_done:
	ljmp FSM1

FSM1_state5:		;Stay in state 5 if temp >= 60 ;cooling;
					; Go to state 09 if temp < 60
					;Power set 0%
	cjne a, #5, FSM1_state5_done
	mov pwm, #0
	clr c
	mov a, Temp_cool
	subb a, bcd+2
	mov a, Temp_refl+1
	subb a, bcd+4
	jc FSM1_state5_done
	mov FSM1_state, #0
FSM1_state5_done:
	ljmp BeginMenu

	ljmp Forever
	
END
