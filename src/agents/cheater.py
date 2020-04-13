from poke_env.player.player import Player
from poke_env.environment.battle import Battle
from DSL import DSL_ALL

class CheaterPlayer(Player):
	def choose_move(self, battle: Battle):
		available_moves = battle.available_moves
		if not available_moves:
			return self.choose_random_move(battle)
			
		dsl = DSL_ALL(battle)
		for move in battle.available_moves:
			if dsl.is_hyper_effective(move):
				return self.create_order(move)

		for move in battle.available_moves:
			if dsl.is_super_effective(move):
				return self.create_order(move)
		
		for move in battle.available_moves:
			if dsl.gets_STAB(move) and dsl.is_not_ineffective(move):
				return self.create_order(move)
		
		for move in battle.available_moves:
			if dsl.is_physical_attacker_and_move_physical(move):
				return self.create_order(move)
		
		for move in battle.available_moves:
			if dsl.is_special_attacker_and_move_special(move):
				return self.create_order(move)

		return self.choose_random_move(battle)