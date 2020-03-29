from poke_env.player.player import Player
from poke_env.environment.battle import Battle

class TypePlayer(Player):
	def choose_move(self, battle: Battle):
		# If the player can attack, it will

		if battle.available_moves:
			# Finds the most type-effective move among available ones
			for move in battle.available_moves:
				opptypes = battle.opponent_active_pokemon.types
				if move.type.damage_multiplier(*battle.opponent_active_pokemon.types)>1:
					return self.create_order(move)

		# If no type-advantageous attack is chosen, a random move will be chosen.
		return self.choose_random_move(battle)