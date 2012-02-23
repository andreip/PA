# run my bot with my bot
./playgame.py --log_dir game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file maps/maze/maze_02p_01.map "python starter_bots/python/RandomBot.py" "./adversar" |java -jar visualizer.jar 
