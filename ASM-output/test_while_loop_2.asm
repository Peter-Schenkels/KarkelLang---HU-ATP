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
while_true_wirce31l73:
    cmp r4, r6
    blt while_body_wirce31l73
    b while_false_wirce31l73
    while_body_wirce31l73:
@ While loop at line: 13
while_true_a1ud6twjq5:
    cmp r5, r6
    blt while_body_a1ud6twjq5
    b while_false_a1ud6twjq5
    while_body_a1ud6twjq5:
@IntOut [ iteratorY ] ! 
@ assign at line 11
    mov r7, #1
    add r5, r5, r7
    b while_true_a1ud6twjq5
while_false_a1ud6twjq5:
@ assign at line 13
    mov r5, #0
@IntOutLine [ iteratorX ] ! 
@ assign at line 15
    mov r7, #1
    add r4, r4, r7
    b while_true_wirce31l73
while_false_wirce31l73:
@ return at line 17
    mov r0, r4
    pop {r4-r11, pc }
