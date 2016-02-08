def learn_spell(spellbook, name, cost, instant_damage, instant_heal, buff_duration, buff_armor, buff_damage, buff_mana):
    spell = { "name": name, "cost": cost, "instant_damage": instant_damage, "instant_heal": instant_heal,
            "buff_duration": buff_duration, "buff_armor": buff_armor, "buff_damage": buff_damage, "buff_mana": buff_mana}
    spellbook[name] = spell

def get_spellbook():
    spellbook = {}
    learn_spell(spellbook, "Magic Missile", 53, 4, 0, 0, 0, 0, 0)
    learn_spell(spellbook, "Drain", 73, 2, 2, 0, 0, 0, 0)
    learn_spell(spellbook, "Shield", 113, 0, 0, 6, 7, 0, 0)
    learn_spell(spellbook, "Poison", 173, 0, 0, 6, 0, 3, 0)
    learn_spell(spellbook, "Recharge", 229, 0, 0, 5, 0, 0, 101)
    return spellbook

def get_starting_game(player_hp, player_mana, mon_hp):
    #create the "start" game from which others will permute
    start_game = { "player_hp": player_hp, "player_mana": player_mana, "mana_spent": 0, "mon_hp": mon_hp, 
            "shield_dur": 0, "poison_dur": 0, "recharge_dur": 0 }
    return start_game

def fight(spellbook, starting_game, mon_damage, is_part_2):
    cheapest_win = 999999
    games = []
    games.append(starting_game)
    while True:
        updated_games = []
        for game in games:
            #filter permitted spells for THIS GAME, based on spell cost, existing durations, and also if the game is not already too expensive as a whole
            permitted_spells = [spell for k, spell in spellbook.items() 
                            if (game["mana_spent"] <= cheapest_win)
                                #this is a little tricky, does player have enough mana OR would he have enough mana after an active Recharge?
                                and spell["cost"] <= (game["player_mana"] + (0 if game["recharge_dur"] == 0 else spellbook["Recharge"]["buff_mana"]))
                                #it's ok for a buff spell to be expiring either this turn (dur == 1), or be expired for longer (dur == 0) 
                                and (game["shield_dur"] <= 1 or spell["name"] != "Shield")
                                and (game["poison_dur"] <= 1 or spell["name"] != "Poison")
                                and (game["recharge_dur"] <= 1 or spell["name"] != "Recharge")]
            #if there were no permitted spells, this loop is empty so game is discarded entirely (i.e. player lost in this branch) 
            #if either player or monster dies in this round, also discard the game. but if monster dies, first check/record possible cheapest win.
            for spell in permitted_spells:
                curr_game = game.copy()
                #player turn
                curr_game = apply_start_of_turn_effects(curr_game, spellbook)
                #part 2 applies ongoing damage to player...
                if is_part_2:
                    curr_game["player_hp"] -= 1
                    if curr_game["player_hp"] <= 0:
                        continue
                curr_game = apply_player_spell_instant_effects(curr_game, spell)
                if curr_game["mon_hp"] <= 0:
                    if curr_game["mana_spent"] < cheapest_win:
                        cheapest_win = curr_game["mana_spent"]
                    continue
                curr_game = apply_new_buffs(curr_game, spell)
                #monster turn
                curr_game = apply_start_of_turn_effects(curr_game, spellbook)
                if curr_game["mon_hp"] <= 0:
                    if curr_game["mana_spent"] < cheapest_win:
                        cheapest_win = curr_game["mana_spent"]
                    continue
                curr_armor = 0 if game["shield_dur"] == 0 else spellbook["Shield"]["buff_armor"]
                adj_mon_damage = max(mon_damage - curr_armor, 1)
                curr_game["player_hp"] -= adj_mon_damage
                if curr_game["player_hp"] <= 0:
                    continue
                #this round is done. both player and monster are still alive. save this state to updated_curr_games
                updated_games.append(curr_game)

        #if updated_games is empty, this means all games have terminated with a death. we're done.
        # otherwise, replace the old games list with the list of continuing games
        if len(updated_games) == 0: 
            return cheapest_win
        else:
            games = updated_games

def apply_start_of_turn_effects(game, spellbook):
    #do start of turn effects from prev active spells, process counters.
    if game["poison_dur"] > 0:
        game["mon_hp"] -= spellbook["Poison"]["buff_damage"]
        game["poison_dur"] -= 1
    if game["recharge_dur"] > 0:
        game["player_mana"] += spellbook["Recharge"]["buff_mana"]
        game["recharge_dur"] -= 1
    if game["shield_dur"] > 0:
        game["shield_dur"] -= 1

    return game

def apply_player_spell_instant_effects(game, spell):
    #cast da spell, process immediate effects. 
    game["mon_hp"] -= spell["instant_damage"]
    game["player_hp"] += spell["instant_heal"]
    game["mana_spent"] += spell["cost"]
    game["player_mana"] -= spell["cost"]

    return game

def apply_new_buffs(game, spell):
    if spell["buff_armor"] > 0: 
        game["shield_dur"] = spell["buff_duration"]
    if spell["buff_damage"] > 0: 
        game["poison_dur"] = spell["buff_duration"]
    if spell["buff_mana"] > 0: 
        game["recharge_dur"] = spell["buff_duration"]

    return game

spellbook = get_spellbook()
starting_game = get_starting_game(50, 500, 58)
cheapest_win = fight(spellbook, starting_game, 9, False)
print "cheapest win part 1: ", cheapest_win
cheapest_win = fight(spellbook, starting_game, 9, True)
print "cheapest win part 2: ", cheapest_win

