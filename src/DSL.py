"""Domain-specific language methods for termina/semiterminal nodes of the evolved AST"""
from typing import Optional, NewType
from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.weather import Weather
from poke_env.utils import to_id_str

#None-able Weather wrapper class
OptionalWeather = NewType("OptionalWeather", Optional[Weather])
OptionalWeather.okay_values = frozenset(Weather).union({None})

#Float wrapper class restricting/providing possible type matchup multipliers
TypeMultiplier = NewType("TypeMultiplier", float)
TypeMultiplier.okay_values = frozenset(2 ** num for num in range(-2, 3)).union({0})

#Int wrapper class restricting/providing possible base stat values
StatValue = NewType("StatValue", int)
StatValue.okay_values = frozenset(range(1, 256))

#Int wrapper class restricting/providing base move powers
MovePower = NewType("MovePower", int)
MovePower.okay_values = frozenset(range(0, 256))

class DSL:
	def __init__(self, battle: Battle):
		self.battle: Battle = battle

	#Methods check a variety of battle information about opponent
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

	##Methods that return information about player pokemon
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

	##Methods that check move properties
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

	def move_type(self, move: Move) -> PokemonType:
		return move.type

	##Move-specific checks
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
			move.weather == Weather.DESOLATELAND)

	def check_move_rainy(self, move: Move) -> bool:
		"""Checks whether the move causes rain"""
		return (
			move.weather == Weather.RAINDANCE or
			move.weather == Weather.PRIMORDIALSEA)

	## Weather checks
	def check_weather(self) -> OptionalWeather:
		precast = self.battle.weather
		assert precast in OptionalWeather.okay_values
		return OptionalWeather(precast)
