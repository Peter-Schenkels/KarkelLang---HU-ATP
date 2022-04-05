.global _start
.section .data
newline: .ascii "\n"
.section .text
print:
    push { r7, lr }
    mov r7, #0x4
    swi 0
    pop { r7, pc }
@ Function Recursive at line 1
karkel_lang_Recursive:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ if at line 9
    mov r4, #10
    cmp r1, r4
    blt if_l6x9elnmqr
    b end_if_l6x9elnmqr
if_l6x9elnmqr:
@ assign at line 5
    mov r4, #1
    add r1, r1, r4
@ assign at line 6
@ Function call at line 6
    push {r1, r2, r3}
    mov r1, r1
    bl karkel_lang_Recursive
    pop {r1, r2, r3}
    mov r1, r0
@ return at line 7
    mov r0, r1
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
end_if_l6x9elnmqr:
@ return at line 9
    mov r0, r1
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 12
karkel_lang_Main:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 14
@ Function call at line 14
    push {r1, r2, r3}
    mov r1, #1
    bl karkel_lang_Recursive
    pop {r1, r2, r3}
    mov r4, r0
@ return at line 15
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
