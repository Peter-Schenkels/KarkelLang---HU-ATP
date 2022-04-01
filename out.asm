.global _start
.section .text
@ Function Recursive at line 1
karkel_lang_Recursive:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ if at line 9
    push { r0, r1 }
    mov r0, #10
    mov r1, r1
    cmp r0, r1
    blt if_1glcq1a9bq
    b end_if_1glcq1a9bq
if_1glcq1a9bq:
@ assign at line 5
    push { r0, r1 }
    mov r0, #1
    mov r1, r1
    add r1, r1, r0
    pop { r0, r1 }
@ assign at line 6
@ Function call at line 6
    push {r1, r2, r3}
    mov r1, r1
    bl karkel_lang_Recursive
    mov r1, r0
    pop {r1, r2, r3}
@ return at line 7
    mov r0, r1
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
end_if_1glcq1a9bq:
@ return at line 9
    mov r0, r1

    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
@ Function Main at line 12
_start:
    mov r7, #0x1
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 14
@ Function call at line 14
    push {r1, r2, r3}
    mov r1, #1
    bl karkel_lang_Recursive
    mov r4, r0
    pop {r1, r2, r3}
@ return at line 15
    mov r0, r4
    swi 0
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }

