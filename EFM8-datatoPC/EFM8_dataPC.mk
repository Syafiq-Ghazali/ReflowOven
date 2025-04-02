SHELL=cmd
CC=c51
COMPORT = $(shell type COMPORT.inc)
OBJS=EFM8_dataPC.obj

EFM8_dataPC.hex: $(OBJS)
	$(CC) $(OBJS)
	@echo Done!
	
EFM8_dataPC.obj: EFM8_dataPC.c
	$(CC) -c EFM8_dataPC.c

clean:
	@del $(OBJS) *.asm *.lkr *.lst *.map *.hex *.map 2> nul

LoadFlash:
	@Taskkill /IM putty.exe /F 2>NUL | wait 500
	EFM8_prog.exe -ft230 -r EFM8_dataPC.hex
	cmd /c start putty -serial $(COMPORT) -sercfg 115200,8,n,1,N

putty:
	@Taskkill /IM putty.exe /F 2>NUL | wait 500
	cmd /c start putty -serial $(COMPORT) -sercfg 115200,8,n,1,N

Dummy: EFM8_dataPC.hex EFM8_dataPC.Map
	@echo Nothing to see here!
	
explorer:
	cmd /c start explorer .
		