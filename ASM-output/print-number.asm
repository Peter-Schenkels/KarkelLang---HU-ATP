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
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 3
    mov r4, #0
@ While loop at line: 9
while_true_p1w98iw89e:
    cmp r1, r2
    bge while_body_p1w98iw89e
    b while_false_p1w98iw89e
    while_body_p1w98iw89e:
@ assign at line 6
    sub r1, r1, r2
@ assign at line 7
    mov r5, #1
    add r4, r4, r5
    b while_true_p1w98iw89e
while_false_p1w98iw89e:
@ return at line 9
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
@ Function modulo at line 12
karkel_lang_modulo:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 14
@ Function call at line 14
    push {r1, r2, r3}
    mov r2, r2
    mov r1, r1
    bl karkel_lang_divide
    pop {r1, r2, r3}
    mov r5, r0
    mul r4, r5, r2
@ assign at line 15
    sub r5, r5, r4
@ return at line 16
    mov r0, r5
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
@ Function printNumber at line 19
karkel_lang_printNumber:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 21
    mov r4, #'a'
    push { r1, r2 }
    mov r1, r4
    ldr r2, =num
    str r1, [r2]
    ldr r1, =num
    mov r2, #1
    bl print
    pop { r1, r2 }
@ assign at line 23
@ Function call at line 23
    push {r1, r2, r3}
    mov r2, #1000
    mov r1, r1
    bl karkel_lang_divide
    pop {r1, r2, r3}
    mov r5, r0
@ assign at line 24
@ Function call at line 24
    push {r1, r2, r3}
    mov r2, #1000
    mov r1, r1
    bl karkel_lang_modulo
    pop {r1, r2, r3}
    mov r1, r0
@ assign at line 25
@ Function call at line 25
    push {r1, r2, r3}
    mov r2, #100
    mov r1, r1
    bl karkel_lang_modulo
    pop {r1, r2, r3}
    mov r6, r0
@ assign at line 26
@ Function call at line 26
    push {r1, r2, r3}
    mov r2, #100
    mov r1, r1
    bl karkel_lang_modulo
    pop {r1, r2, r3}
    mov r1, r0
@ assign at line 27
@ Function call at line 27
    push {r1, r2, r3}
    mov r2, #10
    mov r1, r1
    bl karkel_lang_modulo
    pop {r1, r2, r3}
    mov r7, r0
@ assign at line 28
@ Function call at line 28
    push {r1, r2, r3}
    mov r2, #10
    mov r1, r1
    bl karkel_lang_modulo
    pop {r1, r2, r3}
    mov r1, r0
    push { r1, r2 }
    mov r1, r5
    ldr r2, =num
    str r1, [r2]
    ldr r1, =num
    mov r2, #1
    bl print
    pop { r1, r2 }
    push { r1, r2 }
    mov r1, r6
    ldr r2, =num
    str r1, [r2]
    ldr r1, =num
    mov r2, #1
    bl print
    pop { r1, r2 }
    push { r1, r2 }
    mov r1, r7
    ldr r2, =num
    str r1, [r2]
    ldr r1, =num
    mov r2, #1
    bl print
    pop { r1, r2 }
    push { r1, r2 }
    mov r1, r1
    ldr r2, =num
    str r1, [r2]
    ldr r1, =num
    mov r2, #1
    bl print
    pop { r1, r2 }
@ return at line 35
    mov r0, r1
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 38
karkel_lang_Main:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 40
@ Function call at line 40
    push {r1, r2, r3}
    mov r1, #1111
    bl karkel_lang_printNumber
    pop {r1, r2, r3}
    mov r4, r0
@ return at line 41
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
