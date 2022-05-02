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

@ Function divide at line 2
karkel_lang_divide:
    push {r4-r11, lr }
@Function Declaration , return int 
@Int assigment 
@ assign at line 6
    mov r4, #0
@While Loop [ left > right ] 
@ While loop at line: 15
while_true_ee4ps9j4gh:
    cmp r1, r2
    bge while_body_ee4ps9j4gh
    b while_false_ee4ps9j4gh
    while_body_ee4ps9j4gh:
@Minus operator reassignment 
@ assign at line 11
    sub r1, r1, r2
@Plus operator reassignment 
@ assign at line 13
    mov r5, #1
    add r4, r4, r5
    b while_true_ee4ps9j4gh
while_false_ee4ps9j4gh:
@Return Value 
@ return at line 16
    mov r0, r4
    pop {r4-r11, pc }

@ Function modulo at line 19
karkel_lang_modulo:
    push {r4-r11, lr }
@Function Declaration , return int 
@Multiply operator with function call 
@ assign at line 23
@ Function call at line 23
    push {r1, r2, r3}
    mov r2, r2
    mov r1, r1
    bl karkel_lang_divide
    pop {r1, r2, r3}
    mov r5, r0
    mul r4, r2, r5
@Minus operator reassignment 
@ assign at line 25
    sub r4, r1, r4
@Return Value 
@ return at line 27
    mov r0, r4
    pop {r4-r11, pc }

_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 30
karkel_lang_Main:
    push {r4-r11, lr }
@Main Function Declaration 
@Function call assignment int 
@ assign at line 34
@ Function call at line 34
    push {r1, r2, r3}
    mov r2, #21
    mov r1, #100
    bl karkel_lang_modulo
    pop {r1, r2, r3}
    mov r4, r0
@Return value 
@ return at line 36
    mov r0, r4
    pop {r4-r11, pc }


