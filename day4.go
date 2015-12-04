package main

import (
	"crypto/md5"
	"fmt"
	"math"
	"strings"
)

//mine searches the md5 hashes of (input + integer++) until a hash with the matching prefix is found.
func mine(input string, prefix string) int {
	for i := 1; i < math.MaxInt32; i++ {
		shaft := input + fmt.Sprintf("%d", i)
		ore := fmt.Sprintf("%x", md5.Sum([]byte(shaft)))

		if strings.HasPrefix(ore, prefix) {
			fmt.Printf("%s\n", ore)
			return i
		}
	}

	return -1
}

func main() {
	input := "ckczppom"

	coin5 := mine(input, "00000")
	fmt.Println("5 zero coin at ", coin5)

	coin6 := mine(input, "000000")
	fmt.Println("6 zero coin at ", coin6)
}
