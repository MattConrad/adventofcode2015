package main

import (
	"fmt"
	"strconv"
	"strings"
)

type deer struct {
	speed     int
	durFly    int
	durRest   int
	flying    bool
	countdown int
	distance  int
	points    int
}

var reindeers = make(map[string]deer)

//mustAtoi takes a string and returns the int, panicing if not parsable. thanks br0xen!
func mustAtoi(str string) int {
	ret, err := strconv.Atoi(str)
	if err != nil {
		panic("Failure parsing string to int.")
	}

	return ret
}

//defineDeer assembles a stable of reindeer from lines of text.
func defineDeer(lines []string) {
	for _, line := range lines {
		parts := strings.Split(line, " ")
		name := parts[0]
		speed := mustAtoi(parts[3])
		durFly := mustAtoi(parts[6])
		durRest := mustAtoi(parts[13])
		flying := true
		countdown := durFly
		reindeer := deer{speed: speed, durFly: durFly, durRest: durRest, flying: flying, countdown: countdown, distance: 0, points: 0}
		reindeers[name] = reindeer
	}
}

//main got a little out of hand.
func main() {
	lines := getInput()
	defineDeer(lines)

	for i := 0; i < 2503; i++ {
		furthest := 0
		for name, deer := range reindeers {
			if deer.flying {
				deer.distance += deer.speed
			}

			deer.countdown--

			if deer.countdown == 0 {
				if deer.flying {
					deer.countdown = deer.durRest
				} else {
					deer.countdown = deer.durFly
				}

				deer.flying = !deer.flying
			}

			reindeers[name] = deer

			if deer.distance > furthest {
				furthest = deer.distance
			}
		}

		for name, deer := range reindeers {
			if deer.distance == furthest {
				//they're not made up and they matter a lot!
				deer.points++
				reindeers[name] = deer
			}
		}
	}

	for name, deer := range reindeers {
		fmt.Println(name, "traveled", deer.distance, "points", deer.points)
	}
}

func getInput() []string {
	input := `Rudolph can fly 22 km/s for 8 seconds, but then must rest for 165 seconds.
Cupid can fly 8 km/s for 17 seconds, but then must rest for 114 seconds.
Prancer can fly 18 km/s for 6 seconds, but then must rest for 103 seconds.
Donner can fly 25 km/s for 6 seconds, but then must rest for 145 seconds.
Dasher can fly 11 km/s for 12 seconds, but then must rest for 125 seconds.
Comet can fly 21 km/s for 6 seconds, but then must rest for 121 seconds.
Blitzen can fly 18 km/s for 3 seconds, but then must rest for 50 seconds.
Vixen can fly 20 km/s for 4 seconds, but then must rest for 75 seconds.
Dancer can fly 7 km/s for 20 seconds, but then must rest for 119 seconds.`

	return strings.Split(input, "\n")
}
