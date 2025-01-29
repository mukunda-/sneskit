;*****************************************************************************************
; snesmod example code
;*****************************************************************************************

; Press A to make a sound.
;
; Sound effects use up channel 8. Music should avoid
; using channel 8 for important sections because it
; may get overwritten.
;
; This music uses the hi-hat in channel 8 so it is
; particularly noticable that it's being cut off for
; sound effects.

.include "snes.inc"
.include "snes_joypad.inc"
.include "snesmod.inc"
.include "smconv_soundbank.inc"

.global _nmi, main

;=========================================================================================
	.zeropage
;=========================================================================================

;...insert some zeropage variables

bgcolor:	.res 2

;=========================================================================================
	.code
;=========================================================================================

; Here is an example Sound Table
; The Sound Table defines the sounds that will be used as streamed sound effects.

; The sound data must be in BRR format.
; BRR files can be created with the snesbrr tool by DMV47.

;==============================================================================
SoundTable:
;==============================================================================
SND_TEST = 0
	.byte	4				; DEFAULT PITCH (1..6) (hz = PITCH*2000)
	.byte	8				; DEFAULT PANNING (0..15)
	.byte	15				; DEFAULT VOLUME (0..15)
	.word	(TEST66_DATA_END-TEST66_DATA)/9	; NUMBER OF BRR CHUNKS IN SAMPLE (BYTES/9)
	.word	.LOWORD(TEST66_DATA)		; ADDRESS OF BRR SAMPLE
	.byte	^TEST66_DATA			; ADDRESS BANK
;------------------------------------------------------------------------------

;------------------------------
; Include BRR binary data, pointed to by the sound table entry above.
;------------------------------
TEST66_DATA:
.incbin "../sound/tada.brr" ;tada sound, converted with snesbrr.exe
TEST66_DATA_END:
	
	.a8
	.i16

;---------------------------------------------------------------
; Program entry point
;===============================================================
main:
;===============================================================
	lda	#0Fh			; enable screen
	sta	REG_INIDISP		;
	
	
;---------------------------------------------------------------
	jsr	spcBoot			; BOOT SNESMOD
;---------------------------------------------------------------
	lda	#^__SOUNDBANK__		; give soundbank
	jsr	spcSetBank		; (the soundbank must 
					; have dedicated bank(s))
;---------------------------------------------------------------
	ldx	#MOD_POLLEN8		; load module into SPC
	jsr	spcLoad			;
;---------------------------------------------------------------
	lda	#39			; allocate around 10K of sound ram (39 256-byte blocks)
	jsr	spcAllocateSoundRegion	;
	; now the module size must be restricted to 10K less than the
	; maximum allowed
;---------------------------------------------------------------
	lda	#^SoundTable|80h	; set sound table address
	ldy	#.LOWORD(SoundTable)	;
	jsr	spcSetSoundTable	;
;---------------------------------------------------------------
	ldx	#0			; play module starting at position 0
	jsr	spcPlay			;
;---------------------------------------------------------------

	ldx	#150			; lower the music volume a bit (150/255)
	jsr	spcSetModuleVolume	;

	lda	#81h			; enable IRQ, joypad
	sta	REG_NMITIMEN
	
main_loop:

	lda	joy1_down		; on keypress A:
	bit	#JOYPAD_A		;
	beq	@nkeypress_a		;
					;
	spcPlaySoundM SND_TEST		; play sound using all default parameters
					;
@nkeypress_a:				;

	jsr	spcProcess		; update SPC

	wai
	
	rep	#20h			; increment bgcolor
	inc	bgcolor			;
	lda	bgcolor			;
	sep	#20h			;
	stz	REG_CGADD		;
	sta	REG_CGDATA		;
	xba				;
	sta	REG_CGDATA		;
	
	bra	main_loop
	
	
;---------------------------------------------------------------
; NMI irq handler
;===============================================================
_nmi:
;===============================================================
	rep	#30h			; push a,x,y
	pha				;
	phx				;
	phy				;-----------------------
	sep	#20h			; 8bit akku
					;
;---------------------------------------
;TODO: insert vblank code
;---------------------------------------
	jsr	joyRead
					;
	lda	REG_TIMEUP		; read from REG_TIMEUP (?)
					;
	rep	#30h			; pop a,x,y
	ply				;
	plx				;
	pla				;
	rti				; return
	
;===============================================================
; Other segments unused.
	.segment "HDATA"
	.segment "HRAM"
	.segment "HRAM2"
	.segment "XCODE"
;===============================================================
