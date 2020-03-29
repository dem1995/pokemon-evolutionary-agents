from poke_env.player.player import Player
from poke_env.environment.battle import Battle

class TypePlayer(Player):
	def choose_move(self, battle: Battle):
		# If the player can attack, it will

		print(battle.active_pokemon.base_stats)
		if battle.available_moves:
			# Finds the most type-effective move among available ones
			for move in battle.available_moves:
				opptypes = battle.opponent_active_pokemon.types
				if move.type.damage_multiplier(*battle.opponent_active_pokemon.types)>1:
					return self.create_order(move)
		# if battle.available_moves:
		# 	# Finds the best move among available ones
		# 	best_move = max(battle.available_moves, key=lambda move: move.base_power)
		# 	return self.create_order(best_move)

		# If no attack is available, a random switch will be made
		return self.choose_random_move(battle)