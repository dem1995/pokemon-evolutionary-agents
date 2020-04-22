from poke_env.player.player import Player
from poke_env.environment.battle import Battle
from DSL import DSL

class TestPlayer(Player):
	def choose_move(self, battle: Battle):
		# If the player can attack, it will
		dsl = DSL(battle)
	# 		##Methods check a variety of battle information about opponent

	# 	def printstatus():
	# 		print("battle")
	# 		print(battle)
	# 		print("player active")
	# 		print(battle.active_pokemon)
	# 		print("opp active")
	# 		print(battle.opponent_active_pokemon)
	# 		print("player moves")
	# 		print(list(battle.active_pokemon.moves.values()))
	# 		#print("opp moves")
	# 		#print(battle.opponent_active_pokemon.moves.values())
	# 		print("first player move:")
	# 		print(list(battle.active_pokemon.moves.values())[0])
	# 	i=0
	# 	print(f"Test method {i}") #0
	# 	i+=1
	# 	printstatus()
	# 	#print(dsl.opp_base_defense())
	# 	print(f"Test method {i}") #1
	# 	i+=1
	# 	printstatus()
	# 	#print(dsl.opp_base_spec_defense())
	# 	print(f"Test method {i}") #2
	# 	i+=1
	# 	printstatus()
	# 	#print(dsl.opp_base_speed())
	# 	print(f"Test method {i}") #3
	# 	i+=1
	# 	printstatus()
	# 	#print(dsl.player_base_attack())
	# 	print(f"Test method {i}") #4
	# 	i+=1
	# 	printstatus()
	# 	#print(dsl.player_base_spec_defense())
	# 	print(f"Test method {i}") #5
	# 	i+=1
	# 	printstatus()
	# #	print(dsl.player_base_speed())
	# 	print(f"Test method {i}") #6
	# 	i+=1
	# 	printstatus()
	# 	print("Active pokemon moves:")
	# 	print(list(battle.active_pokemon.moves.values()))
	# 	print(list(battle.active_pokemon.moves.values())[0].type)
	# 	print(battle.active_pokemon.types)
	# 	print(dsl.gets_STAB(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}") #7
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.type_multiplier(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}") #8
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.move_is_status(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}") #9
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.move_is_physical(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}") #10
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.move_is_special(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}")
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.move_base_power(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}") #12
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.move_type(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}")
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.check_move_is_gyro_ball(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}") #14
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.check_move_sds_always(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}")
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.check_move_sds_if_hits_opp(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}") #16
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.check_move_sunny(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}")
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.check_move_rainy(list(battle.active_pokemon.moves.values())[0]))
	# 	print(f"Test method {i}") #18
	# 	i+=1
	# 	printstatus()
	# 	print(dsl.check_weather())

		return self.choose_random_move(battle)
