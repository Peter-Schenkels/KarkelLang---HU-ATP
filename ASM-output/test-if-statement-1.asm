.global _start
.section .data
newline: .ascii "\n"
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
    mov r4, #0
@ if at line 9
    mov r5, #1
    mov r6, #2
    cmp r5, r6
    blt if_gn6v9d4g6o
    b end_if_gn6v9d4g6o
if_gn6v9d4g6o:
@ assign at line 6
    mov r4, #10
@ return at line 7
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
end_if_gn6v9d4g6o:
@ assign at line 9
    mov r4, #5
@ return at line 10
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
