package main

import "fmt"

type ability struct {
    //ability type, I add the a because type is a reserved keyword
    aType int8
    targets [][]bool
}

type piece struct {
    name string
    id int16
    abilities []ability
}

func makePiece() {
    
}

func main() {
    fmt.Printf("hello, world\n")
}
