.global _start
.section .data
newline: .ascii "\n"
.section .text
print:
    push { r7, lr }
    mov r7, #0x4
    swi 0
    pop { r7, pc }
@ Function Fibonacho at line 1
karkel_lang_Fibonacho:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ if at line 14
    mov r4, #100
    cmp r1, r4
    blt if_h9jeli60kf
    b end_if_h9jeli60kf
if_h9jeli60kf:
@ if at line 9
    mov r4, #1
    cmp r1, r4
    ble if_tcy9tldyi2
    b end_if_tcy9tldyi2
if_tcy9tldyi2:
@ return at line 7
    mov r0, r1
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
end_if_tcy9tldyi2:
@ assign at line 9
    mov r5, #1
    sub r4, r1, r5
@ assign at line 10
    mov r6, #2
    sub r5, r1, r6
@ assign at line 11
@ Function call at line 11
    push {r1, r2, r3}
    mov r1, r4
    bl karkel_lang_Fibonacho
    pop {r1, r2, r3}
    mov r7, r0
@ Function call at line 11
    push {r1, r2, r3}
    mov r1, r5
    bl karkel_lang_Fibonacho
    pop {r1, r2, r3}
    mov r8, r0
    add r6, r7, r8
@ return at line 12
    mov r0, r6
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
end_if_h9jeli60kf:
@ return at line 14
    mov r0, r1
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
@ Function PrintFibonachi at line 17
karkel_lang_PrintFibonachi:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 19
@ Function call at line 19
    push {r1, r2, r3}
    mov r1, r2
    bl karkel_lang_Fibonacho
    pop {r1, r2, r3}
    mov r4, r0
@ if at line 28
    cmp r2, r1
    blt if_njieukdijf
    b end_if_njieukdijf
if_njieukdijf:
    .section .data
    StringOut_str: .ascii "Fibonachi:n"
    .section .text
    push {r1, r2}
    ldr r1, =StringOut_str
    mov r2, #10
    bl print
    pop {r1, r2}
    push { r1, r2}
    mov r1, r4
    add r1, r1, #30
    add r2, #1
    bl print
    ldr r1, =newline
    bl print
    pop {r1, r2}
@ assign at line 24
    mov r5, #1
    add r2, r2, r5
@ assign at line 25
@ Function call at line 25
    push {r1, r2, r3}
    mov r2, r2
    mov r1, r1
    bl karkel_lang_PrintFibonachi
    pop {r1, r2, r3}
    mov r4, r0
@ return at line 26
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
end_if_njieukdijf:
@ return at line 28
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
_start:
    mov r7, #0x1
    bl karkel_lang_Main
    swi 0
@ Function Main at line 32
karkel_lang_Main:
    push {r4, r5, r6, r7, r8, r9, r10, r11, lr }
@ assign at line 34
@ Function call at line 34
    push {r1, r2, r3}
    mov r2, #0
    mov r1, #10
    bl karkel_lang_PrintFibonachi
    pop {r1, r2, r3}
    mov r4, r0
@ return at line 35
    mov r0, r4
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }
