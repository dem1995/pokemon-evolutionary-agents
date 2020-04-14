"""Domain-specific language methods for termina/semiterminal nodes of the evolved AST"""
from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.status import Status
from poke_env.environment.weather import Weather
from poke_env.utils import to_id_str
from .dsl_toggle_categories import TOGGLE_CATEGORY, decorate_toggle_category
from .dsl_types import *

# Change the value of this to decide what methods get included in the DSL
# toggledCategory = TOGGLE_CATEGORY.ADVANCED
# toggledCategory = TOGGLE_CATEGORY.BASIC
# toggledCategory = TOGGLE_CATEGORY.BASIC_WITH_CHEATING
toggledCategory = TOGGLE_CATEGORY.ADVANCED


class _DSLRoot:
    def __init__(self, battle: Battle):
        self.battle: Battle = battle


class _DSLManualStatcheck(_DSLRoot):

    # Methods that return information about player Pokemon's base stats

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

    # Methods return information about opponent Pokemon's base stats

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

    # Methods that return information about player Pokemon's stat boosts

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

    # Methods that return information about opponent Pokemon's stat boosts

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


# Methods that automatically cover the gamut of player/opponent stat/buff checks
class _DSLAutoStatcheck(_DSLRoot):

    def player_base_stat(self, base_stat_category: BaseStatCategory) -> StatValue:
        precast = self.battle.active_pokemon.base_stats[base_stat_category]
        assert precast in StatValue.okay_values
        return StatValue(precast)

    def opponent_base_stat(self, base_stat_category: BaseStatCategory) -> StatValue:
        precast = self.battle.active_pokemon.base_stats[base_stat_category]
        assert precast in StatValue.okay_values
        return StatValue(precast)

    def player_battle_stat_modifier(self,
                                    battle_stat_category: BattleStatCategory) -> BattleStatModifier:
        precast = self.battle.active_pokemon.boosts[battle_stat_category]
        assert precast in BattleStatModifier.okay_values
        return BattleStatModifier(precast)

    def opponent_battle_stat_modifier(self,
                                      battle_stat_category: BattleStatCategory) -> BattleStatModifier:
        precast = self.battle.opponent_active_pokemon.boosts[battle_stat_category]
        assert precast in BattleStatModifier.okay_values
        return BattleStatModifier(precast)


# Methods that automatically cover the gamut of player/opponent status effects
class _DSLAutoStatuscheck(_DSLRoot):
    def player_has_status_effect(self, optional_status: OptionalStatus) -> bool:
        precast = self.battle.active_pokemon.status
        assert precast in OptionalStatus.okay_values
        return OptionalStatus(precast) == optional_status

    def opp_has_status_effect(self, optional_status: OptionalStatus) -> bool:
        precast = self.battle.opponent_active_pokemon.status
        assert precast in OptionalStatus.okay_values
        return OptionalStatus(precast) == optional_status


# Methods that check move properties
class _DSLMoveProperties(_DSLRoot):

    def gets_STAB(self, move: Move) -> bool:
        """Returns whether the move shares a type with the Player's active Pokemon"""
        is_type_shared = (move.type in self.battle.active_pokemon.types)
        return is_type_shared

	def type_multiplier(self, move: Move) -> TypeMultiplier:
		"""Returns the damage multiplier of the given move against the opponent's Pokemon"""
		precast = 0 #default if move is not not typed
		if move.type != 0:
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

    def check_move_inflicts_status_condition(self, move: Move,
                                             optional_status: OptionalStatus) -> bool:
        return move.status == optional_status


# Human-designed methods for use in a simple human-designed AI
class _DSLCheat(_DSLRoot):
    def is_raining_and_move_is_water(self, move: Move) -> bool:
        is_raining = self.battle.weather in {Weather.RAINDANCE, Weather.PRIMORDIALSEA}
        move_is_water = move.type == PokemonType.WATER
        return is_raining and move_is_water

    def is_sunny_and_move_is_fire(self, move: Move) -> bool:
        is_sunny = self.battle.weather in {Weather.SUNNYDAY, Weather.DESOLATELAND}
        move_is_fire = move.type == PokemonType.FIRE
        return is_sunny and move_is_fire

    def is_raining_and_move_is_not_fire(self, move: Move) -> bool:
        is_raining = self.battle.weather in {Weather.RAINDANCE, Weather.PRIMORDIALSEA}
        move_is_not_fire = move.type != PokemonType.FIRE
        return is_raining and move_is_not_fire

    def is_sunny_and_move_is_not_water(self, move: Move) -> bool:
        is_sunny = self.battle.weather in {Weather.SUNNYDAY, Weather.DESOLATELAND}
        move_is_not_water = move.type != PokemonType.WATER
        return is_sunny and move_is_not_water

	def is_hyper_effective(self, move: Move) -> bool:
		precast = 0 #default if move is not not typed
		if move.type != 0:
			precast = move.type.damage_multiplier(*self.battle.opponent_active_pokemon.types)
		casted =  TypeMultiplier(precast)
		return casted == 4

	def is_super_effective(self, move: Move) -> bool:
		precast = 0 #default if move is not not typed
		if move.type != 0:
			precast = move.type.damage_multiplier(*self.battle.opponent_active_pokemon.types)
		casted =  TypeMultiplier(precast)
		return casted == 2

	def is_not_ineffective(self, move: Move) -> bool:
		precast = 0 #default if move is not not typed
		if move.type != 0:
			precast = move.type.damage_multiplier(*self.battle.opponent_active_pokemon.types)
		casted =  TypeMultiplier(precast)
		return casted >=1

    def is_physical_attacker_and_move_physical(self, move: Move) -> bool:
        is_physical_attacker = (self.battle.active_pokemon.base_stats['atk'] >
                                self.battle.active_pokemon.base_stats['spa'])
        return is_physical_attacker and (move.category == MoveCategory.PHYSICAL)

    def is_special_attacker_and_move_special(self, move: Move) -> bool:
        is_special_attacker = (self.battle.active_pokemon.base_stats['spa'] >=
                               self.battle.active_pokemon.base_stats['atk'])
        return is_special_attacker and (move.category == MoveCategory.SPECIAL)

    def is_opponent_primarily_attack_and_is_not_burnt_and_move_is_burning_and_opp_not_afflicted(
        self, move: Move) -> bool:
        opponent_primarily_attack = self.battle.opponent_active_pokemon.base_stats['atk'] > \
                                    self.battle.opponent_active_pokemon.base_stats["spa"]
        opponent_not_afflicted = self.battle.opponent_active_pokemon.status == None
        move_is_burning = move.status == Status.BRN
        return opponent_primarily_attack and opponent_not_afflicted and move_is_burning


# Miscellaneous methods currently included
class _DSLMisc(_DSLRoot):

    # Player/Opponent-specific checks

    def player_health_percent(self) -> PercentageValue:
        precast = round(self.battle.active_pokemon.current_hp_fraction * 100)
        assert precast in PercentageValue.okay_values
        return PercentageValue(precast)

    def opp_health_percent(self) -> PercentageValue:
        precast = round(self.battle.opponent_active_pokemon.current_hp_fraction * 100)
        assert precast in PercentageValue.okay_values
        return PercentageValue(precast)

    # Weather checks

    def get_weather(self) -> OptionalWeather:
        precast = self.battle.weather
        assert precast in OptionalWeather.okay_values
        return OptionalWeather(precast)

    # Move-specific checks

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

    def check_move_boosts_stat(self, move: Move, battle_stat_category: BattleStatCategory) -> bool:
        return move.boosts[battle_stat_category] >= 1


base_classes = set()
if TOGGLE_CATEGORY.AUTO_STATCHECK in toggledCategory:
    base_classes.add(_DSLAutoStatcheck)
if TOGGLE_CATEGORY.AUTO_STATUSCHECK in toggledCategory:
    base_classes.add(_DSLAutoStatuscheck)
if TOGGLE_CATEGORY.MANUAL_STATCHECK in toggledCategory:
    base_classes.add(_DSLManualStatcheck)
if TOGGLE_CATEGORY.CHEAT in toggledCategory:
    base_classes.add(_DSLCheat)
if TOGGLE_CATEGORY.CORE in toggledCategory:
    base_classes.add(_DSLMoveProperties)
    base_classes.add(_DSLMisc)

all_classes = {_DSLAutoStatcheck, _DSLAutoStatuscheck, _DSLManualStatcheck, _DSLCheat,
               _DSLMoveProperties, _DSLMisc}


class DSL(*base_classes):
    pass


class DSL_ALL(*all_classes):
    pass
