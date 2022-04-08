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

@ Function Return at line 1
karkel_lang_Return:
    push {r4-r11, lr }
@ return at line 3
    mov r0, r1
    pop {r4-r11, pc }

_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 6
karkel_lang_Main:
    push {r4-r11, lr }
@ assign at line 8
@ Function call at line 8
    push {r1, r2, r3}
    mov r1, #4
    bl karkel_lang_Return
    pop {r1, r2, r3}
    mov r5, r0
@ Function call at line 8
    push {r1, r2, r3}
    mov r1, #6
    bl karkel_lang_Return
    pop {r1, r2, r3}
    mov r6, r0
    add r4, r5, r6
@ return at line 9
    mov r0, r4
    pop {r4-r11, pc }

