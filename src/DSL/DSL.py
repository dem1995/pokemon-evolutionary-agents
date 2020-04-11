"""Domain-specific language methods for termina/semiterminal nodes of the evolved AST"""
from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.weather import Weather
from poke_env.utils import to_id_str
from DSL.dsl_toggle_categories import TOGGLE_CATEGORY, decorate_toggle_category
from DSL.dsl_types import *

#Change the value of this to decide what methods get included in the DSL
toggledCategory = TOGGLE_CATEGORY.ADVANCED

class _DSLRoot:
	def __init__(self, battle: Battle):
		self.battle: Battle = battle


class _DSLManualStatcheck(_DSLRoot):

	#Methods that return information about player Pokemon's base stats

	def player_base_attack(self) -> StatValue:
		precast = self.battle.active_pokemon.base_stats['atk']
		assert precast in StatValue.okay_values
		return StatValue(precast)

	def player_base_spec_defense(self) -> StatValue:
		precast = self.battle.active_pokemon.base_stats['spa']
		assert precast in StatValue.okay_values
		return StatValue(precast)

	def player_base_speed(self) -> StatValue:
		precast = self.battle.active_pokemon.base_stats['spe']
		assert precast in StatValue.okay_values
		return StatValue(precast)


	#Methods return information about opponent Pokemon's base stats

	def opp_base_defense(self) -> StatValue:
		precast = self.battle.opponent_active_pokemon.base_stats['def']
		assert precast in StatValue.okay_values
		return StatValue(precast)

	def opp_base_spec_defense(self) -> StatValue:
		precast = self.battle.opponent_active_pokemon.base_stats['spd']
		assert precast in StatValue.okay_values
		return StatValue(precast)

	def opp_base_speed(self) -> StatValue:
		precast = self.battle.opponent_active_pokemon.base_stats['spe']
		assert precast in StatValue.okay_values
		return StatValue(precast)


	#Methods that return information about player Pokemon's stat boosts

	def player_attack_modifier(self) -> BattleStatModifier:
		precast = self.battle.active_pokemon.boosts['atk']
		assert precast in BattleStatModifier.okay_values
		return BattleStatModifier(precast)
	
	def player_spec_attack_modifier(self) -> BattleStatModifier:
		precast = self.battle.active_pokemon.boosts['spa']
		assert precast in BattleStatModifier.okay_values
		return BattleStatModifier(precast)

	def player_speed_modifier(self) -> BattleStatModifier:
		precast = self.battle.active_pokemon.boosts['spe']
		assert precast in BattleStatModifier.okay_values
		return BattleStatModifier(precast)


	#Methods that return information about opponent Pokemon's stat boosts

	def opp_def_modifier(self) -> BattleStatModifier:
		precast = self.battle.opponent_active_pokemon.boosts['def']
		assert precast in BattleStatModifier.okay_values
		return BattleStatModifier(precast)
	
	def opp_spec_def_modifier(self) -> BattleStatModifier:
		precast = self.battle.opponent_active_pokemon.boosts['spd']
		assert precast in BattleStatModifier.okay_values
		return BattleStatModifier(precast)

	def opp_speed_modifier(self) -> BattleStatModifier:
		precast = self.battle.opponent_active_pokemon.boosts['spe']
		assert precast in BattleStatModifier.okay_values
		return BattleStatModifier(precast)


#Methods that automatically cover the gamut of player/opponent stat/buff checks
class _DSLAutoStatcheck(_DSLRoot):

	def player_base_stat(self, base_stat_category: BaseStatCategory) -> StatValue:
		precast = self.battle.active_pokemon.base_stats[base_stat_category]
		assert precast in StatValue.okay_values
		return StatValue(precast)
	
	def opponent_base_stat(self, base_stat_category: BaseStatCategory) -> StatValue:
		precast = self.battle.active_pokemon.base_stats[base_stat_category]
		assert precast in StatValue.okay_values
		return StatValue(precast)

	def player_battle_stat_modifier(self, battle_stat_category: BattleStatCategory) -> BattleStatModifier:
		precast = self.battle.active_pokemon.boosts[battle_stat_category]
		assert precast in BattleStatModifier.okay_values
		return BattleStatModifier(precast)
	
	def opponent_battle_stat_modifier(self, battle_stat_category: BattleStatCategory) -> BattleStatModifier:
		precast = self.battle.opponent_active_pokemon.boosts[battle_stat_category]
		assert precast in BattleStatModifier.okay_values
		return BattleStatModifier(precast)


#Methods that check move properties
class _DSLMoveProperties(_DSLRoot):

	def gets_STAB(self, move: Move) -> bool:
		"""Returns whether the move shares a type with the Player's active Pokemon"""
		is_type_shared = (move.type in self.battle.active_pokemon.types)
		return is_type_shared

	def type_multiplier(self, move: Move) -> TypeMultiplier:
		"""Returns the damage multiplier of the given move against the opponent's Pokemon"""
		precast = move.type.damage_multiplier(*self.battle.opponent_active_pokemon.types)
		assert precast in TypeMultiplier.okay_values
		return TypeMultiplier(precast)

	def move_is_status(self, move: Move) -> bool:
		return move.category == MoveCategory.STATUS

	def move_is_physical(self, move: Move) -> bool:
		return move.category == MoveCategory.PHYSICAL

	def move_is_special(self, move: Move) -> bool:
		return move.category == MoveCategory.SPECIAL

	def move_base_power(self, move: Move) -> MovePower:
		precast = move.base_power
		assert precast in MovePower.okay_values
		return MovePower(precast)
	
	def move_accuracy(self, move: Move) -> PercentageValue:
		precast = move.accuracy
		assert precast in PercentageValue.okay_values
		return PercentageValue(precast)

	def move_type(self, move: Move) -> PokemonType:
		return move.type


#Miscellaneous methods currently included
class _DSLMisc(_DSLRoot):

	#Player/Opponent-specific checks

	def player_health_percent(self) -> PercentageValue:
		precast = round(self.battle.active_pokemon.current_hp_fraction*100)
		assert precast in PercentageValue.okay_values
		return PercentageValue(precast)

	def opp_health_percent(self) -> PercentageValue:
		precast = round(self.battle.opponent_active_pokemon.current_hp_fraction*100)
		assert precast in PercentageValue.okay_values
		return PercentageValue(precast)


	#Move-specific checks

	def check_move_is_gyro_ball(self, move: Move) -> bool:
		return move.id == to_id_str("Gyro Ball")

	def check_move_sds_always(self, move: Move) -> bool:
		"""Checks whether the move universally causes the using Pok'emon to self-destruct"""
		return move.self_destruct == 'always'

	def check_move_sds_if_hits_opp(self, move: Move) -> bool:
		"""Checks whether the move triggers the user's self-destruction if the attack hits the opponent"""
		return move.self_destruct == 'ifHit'

	def check_move_sunny(self, move: Move) -> bool:
		"""Checks whether the move causes harsh sunlight"""
		return (
			move.weather == Weather.SUNNYDAY or
			move.weather==Weather.DESOLATELAND)

	def check_move_rainy(self, move: Move) -> bool:
		"""Checks whether the move causes rain"""
		return (
			move.weather == Weather.RAINDANCE or
			move.weather == Weather.PRIMORDIALSEA)

	def check_move_boosts_stat(self, move: Move, battle_stat_category: BattleStatCategory) -> bool:
		return move.boosts[battle_stat_category]>=1


	# Weather checks

	def check_weather(self) -> OptionalWeather:
		precast = self.battle.weather
		assert precast in OptionalWeather.okay_values
		return OptionalWeather(precast)


base_classes = set()
if TOGGLE_CATEGORY.AUTO_STATCHECK in toggledCategory:
	base_classes.add(_DSLAutoStatcheck)
if TOGGLE_CATEGORY.MANUAL_STATCHECK in toggledCategory:
	base_classes.add(_DSLManualStatcheck)

base_classes.add(_DSLMoveProperties)
base_classes.add(_DSLMisc)


class DSL(*base_classes):
	pass
