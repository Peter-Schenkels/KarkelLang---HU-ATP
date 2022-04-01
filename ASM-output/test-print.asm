.global _start
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
    .section .data
    StringOutLine_str: .ascii "Hello, World!\n"
    .section .text
    push {r1, r2}
    ldr r1, =StringOutLine_str
    mov r2, #14
    bl print
    pop {r1, r2}
    swi 0
    mov r7, #0x0
