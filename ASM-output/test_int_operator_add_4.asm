.global _start
.section .data
newline: .ascii "\n"
num: .word 0
.section .text

print:
    push { r7, lr }
    mov r7, #0x4
    swi 0
    pop { r7, pc }

_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 1
karkel_lang_Main:
    push {r4-r11, lr }
@ assign at line 3
    mov r4, #7
@ assign at line 4
    mov r5, #3
@ assign at line 5
    add r6, r4, r5
@ return at line 6
    mov r0, r6
    pop {r4-r11, pc }

