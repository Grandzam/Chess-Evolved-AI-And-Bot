package main

import "fmt"


/* Right now, we use a system where an ability is a description of a movement/attack pattern,
 * a piece has a slice of abilities along with some other data,
 * and a board state is just a 8x8 array of pieces
 *
 * This model may change if we can find something that provides a major performance upgrade
 */


type Ability struct {
    //type is a reserved keyword, so we name it ability type
    aType uint8

    //TODO: add documentation describing what this stores
    aRange []int8
}

type Piece struct {

    //piece type

    //to make the data more compact for the cashe, whether the piece is the bot's or the enemy's
    //is stored in here as negitive or positive rather than as a boolean
    //positive = ours, negitive = theirs
    pType int16

    value uint8

    abilities []Ability
}

type Board struct{
    pieces [64]Piece

    morale uint8
    turnNum uint8
}

//makes a piece with a piece type and who it is owned by. For now, it is hardcoded
//this will change soon
func makePiece(pType int16) Piece {
    piece := Piece{ pType, 0, []Ability{} }

    //pawn is 57
    if pType == 57 {
        piece.value = 0

        abil1 := Ability{2, []int8{0,0,1,1} }

        abil2 := Ability{3, []int8{-1,1,0,0} }

        abil3 := Ability{25, []int8{0,0,2,2} }

        piece.abilities = []Ability{abil1,abil2,abil3}
    }

    //rook is 181
    if pType == 181 {
        piece.value = 12

        abil1 := Ability{1, []int8{-8,8,0,0,0,0,-8,8} }

        piece.abilities = []Ability{abil1}
    }

    //bishop is 17
    if pType == 17 {
        piece.value = 9

        //try saying -8,8,-8,8,-8,8,8,-8 out loud
        abil1 := Ability{1, []int8{-8,8,-8,8,-8,8,8,-8} }

        piece.abilities = []Ability{abil1}
    }

    //knight
    if pType == 49 {
        piece.value = 7

        abil1 := Ability{4, []int8{-2,-1,1,2,-2,-1,-1,-2,1,2,2,1,1,2,-2,-1} }

        piece.abilities = []Ability{abil1}
    }

    //queen
    if pType == 241 {
        piece.value = 22

        abil1 := Ability{1, []int8{-8,8,0,0,0,0,-8,8,-8,8,-8,8,-8,8,8,-8} }

        piece.abilities = []Ability{abil1}
    }

    //king
    if pType == 313 {
        piece.value = 25

        abil1 := Ability{1, []int8{-1,1,0,0,0,0,-1,1,-1,1,-1,1,-1,1,1,-1} }

        piece.abilities = []Ability{abil1}
    }

    return piece
}

//makes a new board by initualizing all the pieces on it
//pieces is a 64 array of piece types
func makeBoard(pieces [64]int16, morale uint8, turnNum uint8) Board {

    board := Board{}

    for i, pType := range pieces {
        piece := makePiece(pType)
        board.pieces[i] = piece
    }

    board.morale = morale
    board.turnNum = turnNum

    return board
}

//generates a slice of boards that represent all possible next board states after the current board
//botTurn if it is the bot's turn
func generateLegalMoves(board Board,botTurn bool) []Board {

    for pLocation, piece := range board.pieces {
        if piece.pType == 0 { continue; }

        fmt.Println(pLocation);
        fmt.Println(piece);

        /*for _, abil := range piece.abilities {
            blockable := false
            meleeAttack := false
            move := false
            firstTurnOnly := false

            switch(abil.aType){
            case 1: //move + attack
                blockable = true
                meleeAttack = true
                move = true
            case 2: //move only
                blockable = true
                move = true
            case 3: //attack only
                blockable = true
                meleeAttack = true
            case 4: //attack or move unblockable
                meleeAttack = true
                move = true
            case 5: //teleport
                move = true
            case 25: //this number is subject to change. Move first turn only
                blockable = true
                move = true
                firstTurnOnly = true
            }*/

            //TODO: put in seperate function to deal with too many nested loops and a long fucntion?

            /*for n in range abil.aRange {

            }*/

        /*}*/
    }
    return []Board{}
}

func main() {
    var boardPieces [64]int16

    board := makeBoard(boardPieces,80,0)

    fmt.Println(board.morale)

    fmt.Printf("hello, world\n")
}
