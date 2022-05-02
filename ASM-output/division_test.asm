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

@ Function divide at line 1
karkel_lang_divide:
    push {r4-r11, lr }
@ assign at line 3
    mov r4, #0
@ While loop at line: 9
while_true_mn4ljab1ra:
    cmp r1, r2
    bge while_body_mn4ljab1ra
    b while_false_mn4ljab1ra
    while_body_mn4ljab1ra:
@ assign at line 6
    sub r1, r1, r2
@ assign at line 7
    mov r5, #1
    add r4, r4, r5
    b while_true_mn4ljab1ra
while_false_mn4ljab1ra:
@ return at line 9
    mov r0, r4
    pop {r4-r11, pc }

_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 12
karkel_lang_Main:
    push {r4-r11, lr }
@ assign at line 14
@ Function call at line 14
    push {r1, r2, r3}
    mov r2, #6
    mov r1, #60
    bl karkel_lang_divide
    pop {r1, r2, r3}
    mov r4, r0
@ return at line 15
    mov r0, r4
    pop {r4-r11, pc }

