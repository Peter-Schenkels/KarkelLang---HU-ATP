.global _start
.section .data
newline: .ascii "\n"
.section .text
print:
    push { r7, lr }
    mov r7, #0x4
    swi 0
    pop { r7, pc }
@ Function Func at line 1
karkel_lang_Func:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 3
    mov r5, #1
    mov r6, #2
    add r4, r5, r6
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
@ Function call at line 9
    push {r1, r2, r3}
    bl karkel_lang_Func
    pop {r1, r2, r3}
    mov r4, r0
@ return at line 10
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
