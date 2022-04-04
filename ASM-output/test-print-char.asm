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
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 3
    mov r4, #'a'
    push { r1, r2 }
    mov r1, r4
    ldr r2, =num
    str r1, [r2]
    ldr r1, =num
    mov r2, #1
    bl print
    pop { r1, r2 }
@ return at line 5
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
