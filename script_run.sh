#Script de testare a modului in care 
#lupta botul nostru in prima etapa
#cu adversarii

# Calea catre fisierele din tools_lin.zip
# descarcate de pe cs.curs.pub.ro
lin=lin
# Presupunere: toti jucatorii se afla in directorul curent
player1="./bot32"
player2="MyBot.py"
map="$lin/maps/cell_maze/cell_maze_p02_10.map"
map1="$lin/maps/cell_maze/cell_maze_p02_15.map"
map2="$lin/maps/random_walk/random_walk_p02_10.map"
map3="$lin/maps/random_walk/random_walk_p02_24.map"


chmod a+x $player1
chmod a+x $player2

#./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file $map $player1 "python $player2"|java -jar $lin/visualizer.jar
#./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file $map1 $player1 "python $player2"|java -jar $lin/visualizer.jar
./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 1000 --map_file $map2 $player1 "python $player2"|java -jar $lin/visualizer.jar
#./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file $map3 $player1 "python $player2"|java -jar $lin/visualizer.jar
