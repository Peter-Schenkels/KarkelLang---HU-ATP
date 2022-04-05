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
while_true_y08b8n3w8b:
    cmp r1, r2
    bge while_body_y08b8n3w8b
    b while_false_y08b8n3w8b
    while_body_y08b8n3w8b:
@ assign at line 6
    sub r1, r1, r2
@ assign at line 7
    mov r5, #1
    add r4, r4, r5
    b while_true_y08b8n3w8b
while_false_y08b8n3w8b:
@ return at line 9
    mov r0, r4
    pop {r4-r11, pc }

@ Function modulo at line 12
karkel_lang_modulo:
    push {r4-r11, lr }
@ assign at line 14
@ Function call at line 14
    push {r1, r2, r3}
    mov r2, r2
    mov r1, r1
    bl karkel_lang_divide
    pop {r1, r2, r3}
    mov r5, r0
    mul r4, r2, r5
@ assign at line 15
    sub r4, r1, r4
@ return at line 16
    mov r0, r4
    pop {r4-r11, pc }

@ Function ord at line 19
karkel_lang_ord:
    push {r4-r11, lr }
@ assign at line 21
    mov r4, #48
    add r1, r1, r4
@ return at line 22
    mov r0, r1
    pop {r4-r11, pc }

@ Function printNumber at line 25
karkel_lang_printNumber:
    push {r4-r11, lr }
@ assign at line 27
    ldr r4, =10000
@ assign at line 28
    mov r5, #5
@ While loop at line: 40
while_true_xixwch0b6v:
    mov r6, #0
    cmp r5, r6
    bge while_body_xixwch0b6v
    b while_false_xixwch0b6v
    while_body_xixwch0b6v:
    .section .data
    StringOutLine_str: .ascii ":sukkel
n"
    .section .text
    push {r1, r2}
    ldr r1, =StringOutLine_str
    mov r2, #8
    bl print
    pop {r1, r2}
@ assign at line 37
    mov r6, #1
    sub r5, r5, r6
    b while_true_xixwch0b6v
while_false_xixwch0b6v:
@ assign at line 40
    mov r6, #1
@ return at line 41
    mov r0, r6
    pop {r4-r11, pc }

_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 44
karkel_lang_Main:
    push {r4-r11, lr }
@ assign at line 46
@ Function call at line 46
    push {r1, r2, r3}
    mov r1, #1
    bl karkel_lang_printNumber
    pop {r1, r2, r3}
    mov r4, r0
@ return at line 47
    mov r0, r4
    pop {r4-r11, pc }

