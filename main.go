package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"math/rand"
	"time"
	"strconv"
)

func randomInt(min, max int) int {
    return min + rand.Intn(max-min)
}

func randomString(len int) string {
    bytes := make([]byte, len)
    for i := 0; i < len; i++ {
        bytes[i] = byte(randomInt(65, 90))
    }
    return string(bytes)
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Select mode: \n\t0 - generate string\n\t1 - input text\n\t2 - surname of autor\n")
	str, _ := reader.ReadString('\n')
	mode, _ := strconv.ParseInt(strings.TrimSuffix(str, "\n"), 0, 4)
	var sourceString string
	if mode == 0 {
		rand.Seed(time.Now().UnixNano())
		sourceString = randomString(10)
	} else if mode == 1 {
		fmt.Print("Enter text: ")
		text, _ := reader.ReadString('\n')
		sourceString = strings.TrimSuffix(text, "\n")
	} else if mode == 2 {
		sourceString = "Samotoy"
	} else {
		fmt.Print("Invalid mode. Exit")
		return
	}
	fmt.Printf("Source string: %s\n", sourceString)

	tree := NewHuffmanTree(sourceString)

	var encoded string

	fmt.Printf("Tree:\n")
	tree.Print()
	fmt.Println()
	fmt.Println()


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
