package main

/*
so, the top row is pascal trianglish, and all the other rows can be gotten from the top row
i see that the top row is what is called triangular numbers, which can be calculated as: n(n+1) / 2

to get the code number for cell x, y we want the value from row 1 in column [y + (x - 1)] and then subtract (y - 1)

i suspect this could be more elegant, but it will do

once we can get the code number for cell x, y grinding out the code value should be easy. using remainders, values won't get that big.
*/

import (
	"fmt"
)

func triangleNumber(n int) int {
	return (n * (n + 1)) / 2
}

func codeNumber(x int, y int) int {
	triNum := triangleNumber(y + (x - 1))
	return triNum - (y - 1)
}

func codeValue(start int, mult int, modby int, x int, y int) int {
	codeNum := codeNumber(x, y)
	current := start
	//note we start at 1, not 0. x=1 y=1 should return start unchanged
	for i := 1; i < codeNum; i++ {
		current = current * mult
		current = current % modby
	}

	return current
}

func main() {
	fmt.Println("Code value: ", codeValue(20151125, 252533, 33554393, 3019, 3010))
}
