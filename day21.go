package main

import (
	"fmt"
	"strconv"
	"strings"
)

type item struct {
	category string
	name     string
	cost     int
	damage   int
	armor    int
}

func max(x int, y int) int {
	if x > y {
		return x
	}
	return y
}

func mustAtoi(str string) int {
	ret, err := strconv.Atoi(str)
	if err != nil {
		panic("Failure parsing string to int.")
	}

	return ret
}

func getItemsByCategory(category string, items []item) []item {
	filtered := make([]item, 0)
	for _, item := range items {
		if item.category == category {
			filtered = append(filtered, item)
		}
	}

	return filtered
}

func getAllItems(lines []string) []item {
	items := make([]item, 0)
	for _, line := range lines {
		parts := strings.Split(line, "~")
		newItem := item{category: parts[0], name: parts[1], cost: mustAtoi(parts[2]), damage: mustAtoi(parts[3]), armor: mustAtoi(parts[4])}
		items = append(items, newItem)
	}

	return items
}

//written with the help of http://ewencp.org/blog/golang-iterators/
func getOutfit(items []item) <-chan []item {
	ch := make(chan []item)
	go func() {
		//the first ring is the "None" ring
		ringNone := getItemsByCategory("Ring", items)[0]
		for _, weapon := range getItemsByCategory("Weapon", items) {
			for _, armor := range getItemsByCategory("Armor", items) {
				for _, ring1 := range getItemsByCategory("Ring", items) {
					for _, ring2 := range getItemsByCategory("Ring", items) {
						//can't equip the same ring twice, except "None", check for this and set repeated ring to None.
						// we'll get some dupe outfits this way, that's OK.
						if ring1 == ring2 {
							ring2 = ringNone
						}
						outfit := []item{weapon, armor, ring1, ring2}
						ch <- outfit
					}
				}
			}
		}
		close(ch)
	}()

	return ch
}

func fight(shopItems []item, monHp int, monDamage int, monArmor int) (int, int) {
	cheapestWin := 999999
	costliestLoss := 0

	for outfit := range getOutfit(shopItems) {
		currPlayerHp := 100
		currMonHp := monHp
		playerBaseDamage, playerArmor, playerCost := 0, 0, 0
		for _, gear := range outfit {
			playerBaseDamage += gear.damage
			playerArmor += gear.armor
			playerCost += gear.cost
		}

		//these won't change during the battle.
		currPlayerDamage := max(playerBaseDamage-monArmor, 1)
		currMonDamage := max(monDamage-playerArmor, 1)

		for {
			currMonHp -= currPlayerDamage

			if currMonHp <= 0 {
				//player wins, did he win with cheap gear?
				if playerCost < cheapestWin {
					cheapestWin = playerCost
				}
				break
			}

			currPlayerHp -= currMonDamage

			if currPlayerHp <= 0 {
				//player dies. how much did he spend before dying? maybe it's the most expensive loss.
				if playerCost > costliestLoss {
					costliestLoss = playerCost
				}
				break
			}
		}
	}

	return cheapestWin, costliestLoss
}

func main() {
	lines := getLines()
	items := getAllItems(lines)

	cheapestWin, costliestLoss := fight(items, 109, 8, 2)
	fmt.Println("Cheapest win:", cheapestWin, ", most expensive loss:", costliestLoss)
}

func getLines() []string {
	//this is a little bit altered from the original to make parsing easier
	input := `Weapon~Dagger~8~4~0
Weapon~Shortsword~10~5~0
Weapon~Warhammer~25~6~0
Weapon~Longsword~40~7~0
Weapon~Greataxe~74~8~0
Armor~None~0~0~0
Armor~Leather~13~0~1
Armor~Chainmail~31~0~2
Armor~Splintmail~53~0~3
Armor~Bandedmail~75~0~4
Armor~Platemail~102~0~5
Ring~None~0~0~0
Ring~Damage +1~25~1~0
Ring~Damage +2~50~2~0
Ring~Damage +3~100~3~0
Ring~Defense +1~20~0~1
Ring~Defense +2~40~0~2
Ring~Defense +3~80~0~3`

	return strings.Split(input, "\n")
}
