package main

//this took like 5 hours to run for part 2. i don't advise using this unmodified.

import (
	"fmt"
	"strconv"
)

func transform(left string, right string) (string, string) {
	if len(right) == 0 {
		return left, ""
	} else if len(right) == 1 {
		return left + "1" + right, ""
	}

	end := 0
	firstByte := rune(right[0])
	for i, b := range right {
		if b != firstByte {
			break
		}
		end = i
	}

	//i is zero based, # of matches is i+1. this is also the boundary that starts the new "right".
	matches := end + 1
	return left + strconv.Itoa(matches) + string(firstByte), string(right[matches:])
}

func speak(initial string) string {
	left := ""
	right := initial
	for right != "" {
		left, right = transform(left, right)
	}

	return left
}

func main() {
	seed := "3113322113"
	for i := 0; i < 50; i++ {
		seed = speak(seed)

		if i == 39 {
			fmt.Println("length of speaking 40: ", len(seed))
		}
	}

	fmt.Println("length of speaking 50: ", len(seed))
}
