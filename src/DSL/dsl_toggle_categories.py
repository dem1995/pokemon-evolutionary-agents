"""Contains flags for determining which methods to include in the DSL"""
from enum import Flag, auto

class TOGGLE_CATEGORY(Flag):
	"""Flags for determining which DSL methods to include"""
	MANUAL_STATCHECK = auto()
	AUTO_STATCHECK = auto()
	AUTO_STATUSCHECK = auto()
	MISC_MOVECHECKS = auto()
	CHEAT = auto()
	CORE = auto()
	BASIC = MANUAL_STATCHECK | CORE | MISC_MOVECHECKS
	ADVANCED = AUTO_STATCHECK | CORE | MISC_MOVECHECKS | AUTO_STATUSCHECK
	BASIC_WITH_CHEATING = BASIC | CHEAT

def decorate_toggle_category(togglecategory: TOGGLE_CATEGORY):
	"""Decorator that attaches a toggle category to a method"""
	def set_toggletype(method):
		method.toggletype = togglecategory
		return method
	return set_toggletype
