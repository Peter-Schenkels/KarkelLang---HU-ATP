.global _start
.section .text
@ Function Main at line 1
_start:
    mov r7, #0x1
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 3
    mul r4, r4, #7
@ return at line 4
    mov r0, r4
    swi 0
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }

