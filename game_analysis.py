import sys
from translate_test import zoid_place
from operator import itemgetter

datafile = raw_input("Enter game data file: ")
predictionsfile = datafile[:-4] + "_predictions.bin"
outfile = datafile[:-4] + "_analysis.bin"

bestfile = datafile[:-4] + "_best_moves_byep.bin"
bestout = open(bestfile, "w")

repfile = datafile[:-4] + "_zoid_reps.bin"
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
	if move_rank != None and i < len(options_byep):
		(rank, epdata) = move_rank

		bestoption = options_byep[str(i)][len(options_byep[str(i)])-1]
		bestout.write(bestoption[0]+"\t"+bestoption[1]+"\t"+bestoption[2]+"\t"+bestoption[3]+"\t"+bestoption[4]+"\t")
		bestout.write("\t" + str(zoid_place( int(zoid_col), int(zoid_rot), int(zoid_actual_row), epdata[0], space))+"\n")
		repout.write("\t" + str(zoid_place( int(zoid_col), int(zoid_rot), int(zoid_actual_row), epdata[0], space))+"\n")
	if move_rank != None:
		rank_by_ep[ep_num] = str(rank)
		num_options = len(options_byep[ep_num])

		rank= str(rank_by_ep[ep_num])
		outline += (ep_num + "\t" + epdata[0] + "\t" + epdata[1] + "\t" + epdata[2] + "\t" + epdata[3] + "\t" + epdata[4] + "\t")
		outline += str(rank + "\t")
		outline += str(num_options)
		outfile.write(outline + "\n")
	else:
		outline += (ep_num + "\t" + epdata[0] + "\t" + epdata[1] + "\t" + epdata[2] + "\t" + epdata[3] + "\t" + epdata[4] + "\t")
		outline += ("NA" + '\t')
		outline += "NA"
		outfile.write(outline + "\n")