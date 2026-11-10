// Box.asm  (K = 2)
// Box starts at row 2, is 20 rows tall and 3 words (48 pixels) wide.
// Black while any key is pressed, white when released.
// Start address = SCREEN + 32*2 = 16384 + 64 = 16448

(LOOP)
    // color = (KBD != 0) ? -1 : 0
    @KBD
    D=M
    @BLACK
    D;JNE
    @color
    M=0
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1

(DRAW)
    @20            
    D=A
    @rows
    M=D
    @16448          
    D=A
    @addr
    M=D

(ROW)
    @3              
    D=A
    @cols
    M=D
    @addr
    D=M
    @p
    M=D             

(COL)
    @color
    D=M
    @p
    A=M
    M=D            
    @p
    M=M+1           
    @cols
    MD=M-1
    @COL
    D;JGT           

    @32             
    D=A
    @addr
    M=D+M
    @rows
    MD=M-1
    @ROW
    D;JGT           

    @LOOP           
    0;JMP