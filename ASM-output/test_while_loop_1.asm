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
    mov r5, #10
@ While loop at line: 9
while_true_sok1868kkf:
    cmp r4, r5
    blt while_body_sok1868kkf
    b while_false_sok1868kkf
    while_body_sok1868kkf:
@ assign at line 7
    mov r6, #1
    add r4, r4, r6
    b while_true_sok1868kkf
while_false_sok1868kkf:
@ return at line 9
    mov r0, r4
    pop {r4-r11, pc }

