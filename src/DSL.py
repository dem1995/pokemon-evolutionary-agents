from poke_env.environment.battle import Battle

class DSL:

    _grammar = {}
    _grammar['$B$'] = ['$B1$', '$B1$ and $B1$']
    _grammar['$B1$'] = ['DSL.isDoubles(a)', 'DSL.containsNumber(a, $NUMBER$)', 'DSL.actionWinsColumn(state,a)', 'DSL.hasWonColumn(state,a)', 
                            'DSL.numberPositionsProgressedThisRoundColumn(state, $NUMBER$) > $SMALL_NUMBER$ and DSL.isStopAction(a)', 'DSL.isStopAction(a)',
                            'DSL.numberPositionsConquered(state, $NUMBER$) > $SMALL_NUMBER$ and DSL.containsNumber(a, $NUMBER$)']
    _grammar['$NUMBER$'] = ['2', '3', '4', '5', '6']
    _grammar['$SMALL_NUMBER$'] = ['0', '1', '2']


	@staticmethod
	def 

	#Type Methods
	@staticmethod
	def OpponentType1(battle: Battle):
		return battle.opponent_active_pokemon.types