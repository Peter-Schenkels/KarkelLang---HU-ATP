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
    push {r4-r11, lr }
@ assign at line 3
    mov r4, #0
@ assign at line 4
    mov r5, #0
@ assign at line 5
    mov r6, #10
@ While loop at line: 17
while_true_qfsil8yjiq:
    cmp r4, r6
    blt while_body_qfsil8yjiq
    b while_false_qfsil8yjiq
    while_body_qfsil8yjiq:
@ While loop at line: 13
while_true_0wov61bhtq:
    cmp r5, r6
    blt while_body_0wov61bhtq
    b while_false_0wov61bhtq
    while_body_0wov61bhtq:
@ assign at line 11
    mov r7, #1
    add r5, r5, r7
    b while_true_0wov61bhtq
while_false_0wov61bhtq:
@ assign at line 13
    mov r5, #0
@ assign at line 15
    mov r7, #1
    add r4, r4, r7
    b while_true_qfsil8yjiq
while_false_qfsil8yjiq:
@ return at line 17
    mov r0, r4
    pop {r4-r11, pc }

