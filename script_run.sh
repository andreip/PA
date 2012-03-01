# run our bot with adversar

# path to your lin directory
lin=lin
# all players must be in this directory
player1="RandomBot.py"		# our bot
player2="./opponent"			# our opponent
map="$lin/maps/cell_maze/cell_maze_p02_01.map"	# running map

chmod +x $player1
chmod +x $player2

./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file $map "python $player1" $player2|java -jar $lin/visualizer.jar
