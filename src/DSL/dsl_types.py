"""Additional types to facility the grammar/AST derivation"""
from typing import NewType, Optional
from poke_env.environment.weather import Weather
from poke_env.environment.status import Status

#None-able Weather wrapper class
OptionalWeather = NewType("OptionalWeather", Optional[Weather])
OptionalWeather.okay_values = frozenset(Weather).union({None})

#None-able Status wrapper class
OptionalStatus = NewType("OptionalStatus", Optional[Status])
OptionalStatus.okay_values = frozenset(Status).union({None})

#Float wrapper class restricting/providing possible type matchup multipliers
TypeMultiplier = NewType("TypeMultiplier", float)
TypeMultiplier.okay_values = frozenset(2 ** num for num in range(-2, 3)).union({0})

#Int wrapper class restricting/providing possible base stat values
StatValue = NewType("StatValue", int)
StatValue.okay_values = frozenset(range(1, 256))

#Int wrapper class restricting/providing base move powers
MovePower = NewType("MovePower", int)
MovePower.okay_values = frozenset(range(0, 256))

#Int wrapper class restricting/providing percentage values from 0 to 100
PercentageValue = NewType("PercentageValue", int)
PercentageValue.okay_values = frozenset(range(0, 101))
PercentageValue.suggested_values = frozenset(range(0, 101, 10))

#Str wrapper class restricting/providing base stat types
BaseStatCategory = NewType("BaseStatCategory", str)
BaseStatCategory.okay_values = frozenset({'hp', 'atk', 'def', 'spa', 'spd', 'spe'})

#Str wrapper class restricing/providing battle stat types
BattleStatCategory = NewType("BattleStatCategory", str)
BattleStatCategory.okay_values = frozenset({'hp', 'atk', 'def', 'spa', 'spd', 'spe', 'accuracy', 'evasion'})

#Int wrapper class restricting/providing battle stat boosts
BattleStatModifier = NewType("BattleStatModifier", int)
BattleStatModifier.okay_values = frozenset(range(-6, 7))