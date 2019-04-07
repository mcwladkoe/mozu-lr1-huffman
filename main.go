package main

import (
	"fmt"
)

func main() {
	sourceString := "Samotoy"
	tree := NewHuffmanTree(sourceString)

	var encoded string

	tree.Print()
	fmt.Println()
	fmt.Println()

	fmt.Printf("Source string: %s\n", sourceString)

	err := tree.Encode(&encoded)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Encoded string: %s\n", encoded)

	decoded, err := tree.Decode(encoded)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Decoded string: %s\n", decoded)
}
