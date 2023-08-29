# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 15:41:17 2023

@author: manum
"""

import os 
RootAnalysisFolder = os.path.split(__file__)[0]
from os import chdir
chdir(RootAnalysisFolder)

import sys
from AddPyABA_Path import PyABA_path
 
sys.path.append(PyABA_path)
import BCIGames_tools

# import sys
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import glob

rejection_rate=0.15



RootFolder =  os.path.split(RootAnalysisFolder)[0]

# Open a dialog that allow users to select directories
Folder_Part =QFileDialog.getExistingDirectory(caption='Select Folder',directory=RootFolder)


# Create Raw and Fif converted data folders
RootDirectory_RAW= Folder_Part[0:Folder_Part.find("_rawData")+9]
RootDirectory_FIF = Folder_Part[0:Folder_Part.find("_rawData")] + "_fifData/epochs/"

if not(os.path.exists(Folder_Part[0:Folder_Part.find("_rawData")] + "_fifData/")):
    os.mkdir(Folder_Part[0:Folder_Part.find("_rawData")] + "_fifData/")

if not(os.path.exists(RootDirectory_FIF)):
    os.mkdir(RootDirectory_FIF)
	
	
	
# List of files to convert in case of multiple selection
List_Files = glob.glob(Folder_Part + '/**/*.json', recursive=True)
NbFiles = len(List_Files)

# Loop on NbFiles
for i_files in range(NbFiles):
	File_curr = List_Files[i_files]
	
	# Find Subject name
	SujName = os.path.split(os.path.split(os.path.split(os.path.split(File_curr)[0])[0])[0])[1]
	
	# Find configuration (system) name
	Config = os.path.split(os.path.split(os.path.split(File_curr)[0])[0])[1]
	
	#Convert Calibration Files
	if 'CalibrationData' in File_curr:
		# Convert Target and No Target data to 'epoch' objects
		Epochs_Target,Epochs_NoTarget,NumberOfRepetitions,NbItems,NbTargets=BCIGames_tools.ReadCalib_JsonFile_Mentalink4(File_curr,True)
		
		# Add many information concerning the protocol design
		ParamStim_Target = pd.DataFrame(data = {'NbRep': [NumberOfRepetitions]*len(Epochs_Target),'NbItems' : [NbItems]*len(Epochs_Target), 'NbTurns' : [NbTargets]*len(Epochs_Target)})
		ParamStim_NoTarget = pd.DataFrame(data = {'NbRep': [NumberOfRepetitions]*len(Epochs_NoTarget),'NbItems' : [NbItems]*len(Epochs_NoTarget), 'NbTurns' : [NbTargets]*len(Epochs_NoTarget)})
		Epochs_Target.metadata = ParamStim_Target
		Epochs_NoTarget.metadata = ParamStim_NoTarget
		
		
		# Save epochs in *-epo.fif files	in converted data folder	
		TargetEpochFilename = RootDirectory_FIF + SujName + '.' + Config + '.Calib_' + str(i_files+1) + '-Target-epo.fif' 
		Epochs_Target.save(TargetEpochFilename,overwrite=True)
		
		NoTargetEpochFilename = RootDirectory_FIF + SujName + '.' + Config + '.Calib_' + str(i_files+1) + '-NoTarget-epo.fif' 
		Epochs_NoTarget.save(NoTargetEpochFilename,overwrite=True)
			
				
	#Convert Test  Files
	if 'TestData' in File_curr:
		# Convert Target and No Target data to 'epoch' objects
		Epochs_Target,Epochs_NoTarget,NumberOfRepetitions,NbItems,NbTargets=BCIGames_tools.ReadTest_JsonFile_Mentalink4(File_curr)
		
		# Add many information concerning the protocol design		
		ParamStim_Target = pd.DataFrame(data = {'NbRep': [NumberOfRepetitions]*len(Epochs_Target),'NbItems' : [NbItems]*len(Epochs_Target), 'NbTurns' : [NbTargets]*len(Epochs_Target)})
		ParamStim_NoTarget = pd.DataFrame(data = {'NbRep': [NumberOfRepetitions]*len(Epochs_NoTarget),'NbItems' : [NbItems]*len(Epochs_NoTarget), 'NbTurns' : [NbTargets]*len(Epochs_NoTarget)})
		Epochs_Target.metadata = ParamStim_Target
		Epochs_NoTarget.metadata = ParamStim_NoTarget
		
		# Save epochs in *-epo.fif files	in converted data folder	
		TargetEpochFilename = RootDirectory_FIF + SujName + '.' + Config + '.Test_' + str(i_files+1) + '-Target-epo.fif' 
		Epochs_Target.save(TargetEpochFilename,overwrite=True)
		
		NoTargetEpochFilename = RootDirectory_FIF + SujName + '.' + Config + '.Test_' + str(i_files+1) + '-NoTarget-epo.fif' 
		Epochs_NoTarget.save(NoTargetEpochFilename,overwrite=True)