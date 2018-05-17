### ONLY RUN THIS AFTER YOU HAVE CLONED THE "TetrisParsing" REPO
setwd("/SET/WORKING/DIRECTORY")
remote_run = parsed = F

### the only variables you should have to change are 
## data_folder --- this is where the raw data is located
## new_data --- this is where the output files will be, you need a folder called "rds" and one called "rois" in this folder
## subject.id --- whats the id for this subject
## filename --- what's the raw file you're going to work on.
##### lastly, in the section on gazetools  you will have to update the settings for the project you are working on.

## location of raw input files
data_folder <- "/Users/Matthew/Projects/NewROIs/Raw/"

## location of to-be created output files
## make sure this folder contains a folder called "rds" and one called "rois" --- also make sure not to put a slash at the end
new_data <- "/Users/Matthew/Projects/NewROIs/Data"


source("parse-popStudy.R")
require(ggplot2)


############### step 1 ############### 
######## create RDA
subject.id = "3117"





#################
# Three options, in order of automaticity. 
# NO NEED TO RUN ALL OF THEM. RUN EACH UNTIL YOU GET TO ONE THAT WORKS FOR YOU. 

###OPTION 1:
# Uses the base data file structure used to store tetris logs, if you diverge from that this won't work.
# Assumes you have a folder for each subject (as is the case for the data storage structure used on the server)
# Use case: Copy the WHOLE folder of the desired subject inside the location designated by data_folder
rdaTetrisLog2(sid=subject.id, meta2=F)
#Remember, only run one of these options


###OPTION 2:
# This assumes you dont have each subject in its own folder inside the data_folder location.
# This means you must have only one file for each subject (so make sure it's the COMPLETE file)
# Use case: copy just the "Complete" file into the folder designated by the "data_folder" variable
filename = list.files(data_folder)[which(unlist(gregexpr(subject.id, list.files(data_folder),fixed = TRUE))>-1)]
rdaTetrisLog2(sid=subject.id, f=paste(data_folder,filename,sep=""), meta2=F)
#Remember, only run one of these options


###OPTION 3:
# Every other use case. all you need to do is change the string to the name of the file inside the data_folder
# alternatively, you can forgo the "pasting" and just manually set a "filename" variable to the absolute location of the file
filename = paste(data_folder, "complete_3117_2015-2-18_9-37-56.tsv", sep="")
rdaTetrisLog2(sid=subject.id, f=filename, meta2=F)
#Remember, only run one of these options







############### step 2 ############### 
####### load RDA/RDS


########
# Again, 2 options, but the option you used is determined by which was successful for you previously.

## If you used Option 1 above:
rda <- loadTetrisRDA(subject.id, meta2=F)

## else, you used option 2 or 3:
rda <- readRDS(file.path(new_data, "rds", sprintf("%s.a1.rds", subject.id)))



############### step 3 ############### 
####### create ROI file
## this function creates rois, and takes a while to run. 
write.DynamicROI(getROIs(rda, 1), file.path(new_data, "rois", sprintf("%s.a1.rois.txt", subject.id)))


############### step 4 ############### 
####### create additionalROI file
rep.list <- fread("reg_best_full_game_zoid_reps.tsv",sep = "\t", header = F)
class(rda$episode_number) = "integer"
rep.list <- rep.list[,json := as.character(V1)]$json


write.DynamicROI(addROIs(rda=rda,rep.list=rep.list, rep.name = "best_zoid", layer = 4, mc.cores = 1, game=6), file.path(new_data, "rois", sprintf("%s.a1.NEWroi.txt", subject.id)))


############### step 4 ############### 
####### load ROI
rois_old <- read.DynamicROI(file.path(new_data, "rois", sprintf("%s.a1.rois.txt", subject.id)))
rois_new <- read.DynamicROI(file.path(new_data, "rois", sprintf("%s.a1.NEWroi.txt", subject.id)))
compiledrois <- rbindlist(list(rois_old, rois_new))

write.DynamicROI(compiledrois,file.path(new_data, "rois", sprintf("%s.a1.COMPILED.txt", subject.id)))

############### step 5 ############### 
####### use gazetool
rda = rda[event_type=="EYE_SAMP"]


##make sure to adjust the parameters for your experiment. See ?pva for documentation.
g = rda[game_number > 0, gazetools(x=smi_samp_x_l, y=smi_samp_y_l, samplerate=500, rx=1680, ry=1050, sw=473.76, sh=296.1, ez=smi_eye_z_l,ex = smi_eye_x_l, ey= smi_eye_y_l, blinks=(smi_samp_x_l==0 & smi_samp_y_l==0), timestamp=smi_ts)]
g$data = cbind(g$data, rda[game_number >0, list(game_number,episode_number,curr_zoid,next_zoid,level,score)])
g$data[is.na(score),score:=0]
g$data[is.na(level),level:=0]

## check ?classify for documentation
g$classify()



sp1 <- g$scanpath(rois = rois_old)
sp2 <- g$scanpath(rois = compiledrois)

