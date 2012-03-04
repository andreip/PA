#Script de testare a modului in care 
#lupta botul nostru in prima etapa
#cu adversarii

# Calea catre fisierele din tools_lin.zip
# descarcate de pe cs.curs.pub.ro
lin=lin
# Presupunere: toti jucatorii se afla in directorul curent
player1="MyBot.py"
player2="./bot32"
map="$lin/maps/cell_maze/cell_maze_p02_19.map"
map1="$lin/maps/cell_maze/cell_maze_p02_20.map"
map2="$lin/maps/random_walk/random_walk_p02_21.map"
map3="$lin/maps/random_walk/random_walk_p02_24.map"


chmod a+x $player1
chmod a+x $player2

./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file $map "python $player1" $player2|java -jar $lin/visualizer.jar
./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file $map1 "python $player1" $player2|java -jar $lin/visualizer.jar
./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file $map2 "python $player1" $player2|java -jar $lin/visualizer.jar
./$lin/playgame.py --log_dir $lin/game_logs -So --verbose --engine_seed 42 --player_seed 0 --turns 100 --map_file $map3 "python $player1" $player2|java -jar $lin/visualizer.jar
