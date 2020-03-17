# -*- coding: utf-8 -*-
import asyncio

from poke_env.player.random_player import RandomPlayer
from poke_env.player.utils import cross_evaluate
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import LocalhostServerConfiguration
from tabulate import tabulate

from agents.maxdam import MaxDamagePlayer
from agents.typeplayer import TypePlayer


async def main():
	# First, we define three player configurations.
	player_1_configuration = PlayerConfiguration("Player 1", None)
	player_2_configuration = PlayerConfiguration("Player 2", None)
	player_3_configuration = PlayerConfiguration("Max Damage Player", None)
	player_4_configuration = PlayerConfiguration("Type Damage Player", None)


	# # Then, we create the corresponding players.
	players = []
	players.extend([
		RandomPlayer(
			player_configuration=player_config,
			battle_format="gen1randombattle",
			server_configuration=LocalhostServerConfiguration,
			max_concurrent_battles=20,
		)
		for player_config in [
			player_1_configuration,
	#		player_2_configuration,
		]
	])

	players.extend(
		MaxDamagePlayer(
			player_configuration=player_config,
			battle_format="gen1randombattle",
			server_configuration=LocalhostServerConfiguration,
			max_concurrent_battles=20,
		)
		for player_config in [
			player_3_configuration,
		]
	)

	players.extend([
		TypePlayer(
			player_configuration=player_config,
			battle_format="gen7randombattle",
			server_configuration=LocalhostServerConfiguration,
			max_concurrent_battles=20,
		)
		for player_config in [
			player_4_configuration,
		]
	])

	# Now, we can cross evaluate them: every player will player 20 games against every
	# other player.
	cross_evaluation = await cross_evaluate(players, n_challenges=80)

	# Defines a header for displaying results
	table = [["-"] + [p.username for p in players]]

	# Adds one line per player with corresponding results
	for p_1, results in cross_evaluation.items():
		table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])

	# Displays results in a nicely formatted table.
	print(tabulate(table))


if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())