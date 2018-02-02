from simulator_API import *
from simulator import TetrisSimulator
from tetris_cpp import *
from boards import print_board, all_zoids
import sys
from translate_test import zoid_place
from operator import itemgetter

inputfile= raw_input("Enter data file to analyze: ")
#reg_best_full_game.tsv
data = open(inputfile, "rU")
prediction_file= inputfile[:-4]+"_predictions"
outfile = open(prediction_file, "w")

CERLscore = {"landing_height": -152.3582,
                   "eroded_cells": 25.0868439339,
                   "row_trans": -162.330389078,
                   "col_trans": -383.049691756,
                   "pits": -498.471504549,
                   "cuml_wells": 3.59862230086}
                   
header = data.readline()
header = header.rstrip().split('\t')


board_ix = header.index('board_rep') 
zoid_rot_ix = header.index('zoid_rot') 
zoid_col_ix = header.index('zoid_col') 
zoid_row_ix = header.index('zoid_row') 
curr_zoid_ix = header.index('curr_zoid') 
ep_num_ix = header.index('episode_number')

out_header = ""
out_header += ("episode_number" + "\t")
out_header += ("zoid" + "\t")
out_header += ("move_row" + "\t")
out_header += ("move_col" + "\t")
out_header += ("move_rot" + "\t")
out_header += "move_score"

outfile.write(out_header + "\n")

lines = data.readlines()
for x in range(len(lines)):
    line = lines[x]
    if x == 0:
        player_board = [[0]*10 for i in range(20)]
    else:
        prev_line = lines[x - 1]
        prev_line = prev_line.rstrip().split('\t')
        player_board = eval(eval(prev_line[board_ix]))
    line = line.rstrip().split('\t')
    
    if line[curr_zoid_ix] != 'NA':
        player_zoid = line[curr_zoid_ix]

    working_controller = CERLscore
    working_features = CERLscore.keys()
    
    sim = TetrisSimulator(controller=working_controller)
    sim.space = tetris_cow2.convert_old_board(player_board)
    sim.curr_z = all_zoids[player_zoid]


    feats = get_features(player_board, player_zoid, working_controller, dictionaries=False)
    
    for f in feats:
        lh_val = f['features']['landing_height'] * working_controller['landing_height']
        ec_val = f['features']['eroded_cells'] * working_controller['eroded_cells']
        rt_val = f['features']['row_trans'] * working_controller['row_trans']
        ct_val = f['features']['col_trans'] * working_controller['col_trans']
        pit_val = f['features']['pits'] * working_controller['pits']
        wells_val = f['features']['cuml_wells'] * working_controller['cuml_wells']
        move_score = lh_val + ec_val + rt_val + ct_val + pit_val + wells_val
        
        out_line = ""
        out_line += (str(line[ep_num_ix]) + "\t")
        out_line += (str(f['zoid']) + "\t")
        out_line += (str(f['row']) + "\t")
        out_line += (str(f['col']) + "\t")
        out_line += (str(f['orient']) + "\t")
        out_line += str(move_score)
        
        outfile.write(out_line + "\n")
    
###############################################

datafile = inputfile
predictionsfile = prediction_file
outfile = datafile[:-4] + "_analysis"

bestfile = datafile[:-4] + "_best_moves_byep"
bestout = open(bestfile, "w")

repfile = datafile[:-4] + "_zoid_reps"
repout = open(repfile, "w")

game_data = open(datafile, "rU")
byepisode_data = open(predictionsfile, "rU")
outfile = open(outfile, "w")

options_byep= {}
header= byepisode_data.readline()
for line in byepisode_data:
    line= line.split()
    if line[0] in options_byep:
        options_byep[line[0]].append(line[1:])
    else:
        options_byep[line[0]]= [line[1:]]
for ep in options_byep:
    options_byep[ep] = sorted(options_byep[ep], key= itemgetter(4))

header = game_data.readline()
header = header.rstrip().split('\t')

board_ix = header.index('board_rep') 
zoid_rot_ix = header.index('zoid_rot') 
zoid_col_ix = header.index('zoid_col') 
zoid_row_ix = header.index('zoid_row')
zoid_lh_ix = header.index('landing_height')
curr_zoid_ix = header.index('curr_zoid') 
ep_num_ix = header.index('episode_number')

rank_by_ep = {}

# bestout.write("Best Move:\n")
# for i in range(0,len(options_byep)):
    # bestout.write(str(options_byep[str(i)][len(options_byep[str(i)])-1]) + "\n")

def findmove_rank(options,ep,rot,col,row):
    options = options[ep]
    num_options = len(options)
    for option in options:
        # option_row= str(int(option[1])+1)
        if option[3] == rot and option[2] == col and option[1] == row:
            return (num_options, option)
        elif num_options!= 0:
            num_options -= 1
        else:
            return (999,[9,9,9,9])

outfile.write("Moves chosen by episode \n")

out_header = ""
out_header += ("episode_number" + "\t")
out_header += ("zoid" + "\t")
out_header += ("move_row" + "\t")
out_header += ("move_col" + "\t")
out_header += ("move_rot" + "\t")
out_header += ("move_score" + "\t")
out_header += ("move_rank" + "\t")
out_header += ("num_options")

best_header = ""
best_header += ("zoid" + "\t")
best_header += ("move_row" + "\t")
best_header += ("move_col" + "\t")
best_header += ("move_rot" + "\t")
best_header += ("move_score" + "\t")
best_header += ("zoid_rep")

outfile.write(out_header + "\n")
bestout.write(best_header + "\n")
i = -1
for line in game_data:
    space = []
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])
    space.append([0,0,0,0,0,0,0,0,0,0])

    i+=1
    outline = ""
    line= line.rstrip().split('\t')
    ep_num = line[ep_num_ix]
    zoid_rot = line[zoid_rot_ix]
    zoid_col = line[zoid_col_ix]
    zoid_row = line[zoid_lh_ix]
    zoid_actual_row = line[zoid_row_ix]

    move_rank = findmove_rank(options_byep, ep_num, zoid_rot, zoid_col, zoid_row)
    if move_rank == None and i < len(options_byep):
        bestoption = options_byep[str(i)][len(options_byep[str(i)])-1]
        bestout.write(bestoption[0]+"\t"+bestoption[1]+"\t"+bestoption[2]+"\t"+bestoption[3]+"\t"+bestoption[4]+"\t")
        bestout.write(str(zoid_place( int(zoid_col), int(zoid_rot), int(zoid_actual_row), line[curr_zoid_ix], space))+"\n")
        repout.write(str(zoid_place( int(zoid_col), int(zoid_rot), int(zoid_actual_row), line[curr_zoid_ix], space))+"\n")        
    if move_rank != None and i < len(options_byep):
        (rank, epdata) = move_rank

        bestoption = options_byep[str(i)][len(options_byep[str(i)])-1]
        bestout.write(bestoption[0]+"\t"+bestoption[1]+"\t"+bestoption[2]+"\t"+bestoption[3]+"\t"+bestoption[4]+"\t")
        bestout.write(str(zoid_place( int(zoid_col), int(zoid_rot), int(zoid_actual_row), epdata[0], space))+"\n")
        repout.write(str(zoid_place( int(zoid_col), int(zoid_rot), int(zoid_actual_row), epdata[0], space))+"\n")
    if move_rank != None:
        rank_by_ep[ep_num] = str(rank)
        num_options = len(options_byep[ep_num])

        rank= str(rank_by_ep[ep_num])
        outline += (ep_num + "\t" + epdata[0] + "\t" + epdata[1] + "\t" + epdata[2] + "\t" + epdata[3] + "\t" + epdata[4] + "\t")
        outline += str(rank + "\t")
        outline += str(num_options)
        outfile.write(outline + "\n")
    else:
        outline += (line[ep_num_ix] + "\t" + line[curr_zoid_ix] + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\t")
        outline += ("NA" + '\t')
        outline += "NA"
        outfile.write(outline + "\n")
    
    
    

