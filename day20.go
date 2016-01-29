package main

import (
	"errors"
	"fmt"
)

func getPresentsForHouse(houseNum int) int {
	presents := 0
	for i := 1; i <= houseNum; i++ {
		if houseNum%i == 0 {
			presents += (i * 10)
		}
	}

	return presents
}

// findHouse finds the first house in part 1 where elves deliver a present count >= target.
func findHouse(start int, target int) (int, error) {
	//let's start with brute force. not sure this is going to work with the size of the input
	// the target / 10 house will always get the target number of presents from elf / 10, can't be higher than that.
	// if i was more mathy i bet i could reduce this series cleverly.
	for i := start; i <= target/10; i++ {
		presents := getPresentsForHouse(i)
		//fmt.Println(i, presents)
		if presents >= target {
			return i, nil
		}

		//i wanted to watch progress, that's all this is.
		if i%100000 == 0 {
			fmt.Println(i)
		}
	}

	return 0, errors.New("Failed to find target present count.")
}

// findLazyElfHouse finds the smallest house number in part 2 where the lazy elves deliver >= target presents.
func findLazyElfHouse(start int, target int) int {
	houseTotals := make(map[int]int)

	smallestHouse := target
	//since the elves deliver 11 presents to each house, there is a house near target / 11 which immediately gets the target number
	// first house can't be bigger than that, we can truncate search there.
	for i := start; i < (target/11 + 11); i++ {
		//each elf only delivers to the first 50 multiples of his number.
		for j := 1; j <= 50; j++ {
			houseNumber := i * j
			houseTotals[houseNumber] += i * 11

			if houseTotals[houseNumber] >= target && houseNumber < smallestHouse {
				smallestHouse = houseNumber
				break
			}
		}
	}

	return smallestHouse
}

func main() {
	target := 34000000
	//some of the early houses can certainly be skipped. take a guess (and a chance) if you want to save some time
	// i got burned on this in part 2, be careful
	start := 1000

	//uncomment the below for part 1, but be warned, it's slow
	/*
		houseNum, err := findHouse(start, target)
		if err != nil {
			panic(err)
		}

		fmt.Printf("First house with %d presents was %d.", target, houseNum)
	*/

	houseNum := findLazyElfHouse(start, target)

	fmt.Printf("First lazy-elf house with %d presents was %d.", target, houseNum)
}
