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

@ Function return at line 2
karkel_lang_return:
    push {r4-r11, lr }
@ return at line 4
    mov r0, r1
    pop {r4-r11, pc }

@ Function Sum at line 8
karkel_lang_Sum:
    push {r4-r11, lr }
@ assign at line 10
    mov r4, #'m'
@ assign at line 11
@ Function call at line 11
    push {r1, r2, r3}
    mov r1, r1
    bl karkel_lang_return
    pop {r1, r2, r3}
    mov r6, r0
@ Function call at line 11
    push {r1, r2, r3}
    mov r1, r2
    bl karkel_lang_return
    pop {r1, r2, r3}
    mov r7, r0
    add r5, r6, r7
@ return at line 12
    mov r0, r5
    pop {r4-r11, pc }

_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 15
karkel_lang_Main:
    push {r4-r11, lr }
@ assign at line 17
    mov r4, #4
@ assign at line 18
    mov r5, #6
@ assign at line 19
@ Function call at line 19
    push {r1, r2, r3}
    mov r2, r5
    mov r1, r4
    bl karkel_lang_Sum
    pop {r1, r2, r3}
    mov r6, r0
@ return at line 20
    mov r0, r6
    pop {r4-r11, pc }

