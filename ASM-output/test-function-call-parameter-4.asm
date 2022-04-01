.global _start
.section .data
newline: .ascii "\n"
.section .text
print:
    push { r7, lr }
    mov r7, #0x4
    swi 0
    pop { r7, pc }
@ Function Sum at line 1
karkel_lang_Sum:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 3
    add r4, r1, r2
@ return at line 4
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 7
karkel_lang_Main:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 9
    mov r4, #4
@ assign at line 10
    mov r5, #6
@ assign at line 11
@ Function call at line 11
    push {r1, r2, r3}
    mov r2, r5
    mov r1, r4
    bl karkel_lang_Sum
    pop {r1, r2, r3}
    mov r6, r0
@ return at line 12
    mov r0, r6
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
