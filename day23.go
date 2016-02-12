package main

import (
	"fmt"
	"strconv"
	"strings"
)

type instruction struct {
	name     string
	register string
	offset   int
}

func mustAtoi(str string) int {
	ret, err := strconv.Atoi(str)
	if err != nil {
		panic("Failure parsing string to int.")
	}

	return ret
}

func processInstructions(starta int, instrs []instruction) int {
	registers := map[string]int{"a": starta, "b": 0}
	index := 0
	for {
		ins := instrs[index]
		//rv will be 0 for instruction types that don't ref registers, this is fine.
		rv := registers[ins.register]
		if ins.name == "hlf" {
			registers[ins.register] = rv / 2
			index++
		} else if ins.name == "tpl" {
			registers[ins.register] = rv * 3
			index++
		} else if ins.name == "inc" {
			registers[ins.register] = rv + 1
			index++
		} else if (ins.name == "jmp") || (ins.name == "jie" && rv%2 == 0) || (ins.name == "jio" && rv == 1) {
			index = index + ins.offset
		} else {
			//should be only left with the case where jie or jio don't jump. i think only sensible thing to do here is advance.
			index++
		}

		if index >= len(instrs) {
			break
		}
	}

	return registers["b"]
}

func getInstructions(lines []string) []instruction {
	instrs := make([]instruction, 0)
	for _, line := range lines {
		parts := strings.Split(line, " ")
		instr := instruction{name: parts[0]}
		if parts[0] == "hlf" || parts[0] == "tpl" || parts[0] == "inc" {
			instr.register = parts[1]
		} else if parts[0] == "jmp" {
			instr.offset = mustAtoi(parts[1])
			//we'll assume good input, only jie or jie now, because AoC always has good input
		} else {
			instr.register = string(parts[1][0])
			instr.offset = mustAtoi(parts[2])
		}
		instrs = append(instrs, instr)
	}

	return instrs
}

func main() {
	lines := getLines()
	instructions := getInstructions(lines)

	results1 := processInstructions(0, instructions)
	fmt.Println("Final results part 1:", results1)

	results2 := processInstructions(1, instructions)
	fmt.Println("Final results part 2:", results2)
}

func getLines() []string {
	input := `jio a, +18
inc a
tpl a
inc a
tpl a
tpl a
tpl a
inc a
tpl a
inc a
tpl a
inc a
inc a
tpl a
tpl a
tpl a
inc a
jmp +22
tpl a
inc a
tpl a
inc a
inc a
tpl a
inc a
tpl a
inc a
inc a
tpl a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
jio a, +8
inc b
jie a, +4
tpl a
inc a
jmp +2
hlf a
jmp -7`

	return strings.Split(input, "\n")
}
