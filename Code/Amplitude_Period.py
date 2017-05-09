from __future__ import print_function#4/27/17 COC: for Python 2.7 backwards compatability
import argparse#parse command line arguments 4/13/17 COC
import os
import glob

DownloadPath = '/scratch/coc25/LMIdata/LMIfinal/'#'/Volumes/Moon/Keck/Downloads/'
BasePath = DownloadPath

BaseOutputFolder = '/common/contrib/classroom/ast520/output/'


def CrawlTree(directory):
	'''
	4/19/2017 Colin Orion Chandler
	Crawl a directory structure and create a dictionary of dictionaries.
	Each child dictionary will have the file shortname (filename only) and folder (directory) path as dictionary items.
	4/20/17 COC: added targetmode pair outermost folders to target names, so simply find first TARGNAME in a tree, then move on to the next directory.
	'''
	FolderList = []
	AllFits = {}
	a = os.walk(directory)
	CrawlCount = 0
	TotCrawlCount = 0
#	print('a: ' + str(a))
	for folder in a:
		CrawlCount += 1
		TotCrawlCount += 1
		if CrawlCount == 100:
			print(str(time.asctime()) + ': Crawled ' + str(TotCrawlCount) + ' folders thus far...')
			CrawlCount = 0
		if '/.' in folder[0]:#skip hidden directories (note 5/2/17 COC)
			pass
		else:
			FolderList.append(folder[0])
	return(FolderList)

def ThisFilePath():#this is the path of this Python file 4/13/17 COC
	return(str(os.path.dirname(os.path.realpath(__file__))) + '/')
#print(ThisFilePath())

def BeginTable(outputfile):
	try:
		os.remove(outputfile + '.bak')
	except:
		pass
	try:
		os.rename(outputfile,outputfile + '.bak')
	except:
		pass
	with open (outputfile,'a') as f:
		print('<html>',file=f)
		print('<!-- From HZG originally 5/6/17 COC -->',file=f)
		print('<head>',file=f)
		print('',file=f)
		print('<title>A520 Results</title>',file=f)
		print('',file=f)
		print('<script src="sorttable.js"></script>',file=f)
		print('',file=f)
		print('<script src="jquery-1.4.2.min.js"></script>',file=f)
		print('<script src="jquery.thead-1.1.min.js"></script>',file=f)
		print('',file=f)
		print('<style type="text/css">',file=f)
		print('th{font-family: arial, arial narrow, helvetica}',file=f)
		print('td{font-family: arial, arial narrow, helvetica}',file=f)
		print('</style>',file=f)
		print('',file=f)
		print('</head>',file=f)
		print('',file=f)
		print('<body bgcolor="#000000" text="#FFFFFF" link="#FFFFFF" vlink="8888FF">',file=f)
		print('',file=f)
		print('<!-- <center> -->',file=f)
		print('<!-- <img src="title.gif" width=800> -->',file=f)
		print('<!-- </center> -->',file=f)
		print('',file=f)
		print('<center>',file=f)
		print('',file=f)
		print('<div>',file=f)
		print('',file=f)
		print('<table width=900 border=0 cellpadding=5 class="sortable jquery-thead">',file=f)
		print('',file=f)
		print('<thead>',file=f)
#		print('<tr bgcolor="#000000">',file=f)
		print('<tr bgcolor="#033333">',file=f)
		print('<!-- Table column headers 5/6/17 COC -->',file=f)
		print('<th><b>TargetID</b></th>',file=f)
		print('<th><b>FinalStatus</b></th>',file=f)
		print('<th><b>Folder</b></th>',file=f)
		print('<th><b>.diagnostics Link</b></th>',file=f)
		print('<th><b>pp_run Status</b></th>',file=f)
		print('<th><b>pp_run ldac count</b></th>',file=f)
		print('<th><b>pp_ident</b></th>',file=f)
		print('<th><b>pp_ident phot count</b></th>',file=f)
		print('<th><b>pp_distill Status</b></th>',file=f)
		print('<th><b>pp_distill LC count</b></th>',file=f)
		print('<th><b>pp_parse Status</b></th>',file=f)
		print('<th><b>pp_parse .varformat count</b></th>',file=f)
		print('<th><b>AmpPer Status</b></th>',file=f)
		print('<th><b>AmpPer Count</b></th>',file=f)
		print('<th><b>Vartools Status</b></th>',file=f)
		print('<th><b>TMP Count</b></th>',file=f)
		print('<th><b>Scratch Count</b></th>',file=f)
		print('<th><b>VarFinal Count</b></th>',file=f)
		print('<th><b>LC Link</b></th>',file=f)
		print('<!-- <th><b>T<sub>eq</sub><sup>a</sup> (K)</b></th> -->',file=f)
		print('</tr>',file=f)
		print('</thead>',file=f)
		print('',file=f)
		print('<!-- Begin table rows here -->',file=f)
		print('',file=f)

def RowEntry(SomeString):
	return('<td>' + str(SomeString) + '</td>')

def WriteRow(OutputFile,
			ID,
			FinalStatus,
			Folder,
			DiagLink,
			pp_runStatus,
			pp_runCount,
			pp_identStatus,
			pp_identCount,
			pp_distillStatus,
			pp_distill_LC_count,
			pp_parseStatus,
			pp_parse_varformatCount,
			AmpPerStatus,
			AmpPerCount,
			VarToolsStatus,
			VartoolsTmpCount,
			VarStatCount,
			VarFinalCount,
			lcLink):
	with open(OutputFile,'a') as f:
		print('',file=f)
		print(RowEntry(ID),file=f)
		print(RowEntry(FinalStatus),file=f)
		print(RowEntry(Folder),file=f)
		print(RowEntry(DiagLink),file=f)
		print(RowEntry(pp_runStatus),file=f)
		print(RowEntry(pp_runCount),file=f)
		print(RowEntry(pp_identStatus),file=f)
		print(RowEntry(pp_identCount),file=f)
		print(RowEntry(pp_distillStatus),file=f)
		print(RowEntry(pp_distill_LC_count),file=f)
		print(RowEntry(pp_parseStatus),file=f)
		print(RowEntry(pp_parse_varformatCount),file=f)
		print(RowEntry(AmpPerStatus),file=f)
		print(RowEntry(AmpPerCount),file=f)
		print(RowEntry(VarToolsStatus),file=f)
		print(RowEntry(VartoolsTmpCount),file=f)
		print(RowEntry(VarStatCount),file=f)
		print(RowEntry(VarFinalCount),file=f)
		print(RowEntry(lcLink),file=f)
		print('</tr>',file=f)
		print('',file=f)


def FinishTable(outputfile):
	with open(outputfile,'a') as f:
		print('<!-- End table rows here -->',file=f)
		print('',file=f)
		print('</table>',file=f)
		print('',file=f)
		print('</div>',file=f)
		print('',file=f)
		print('</center>',file=f)
		print('',file=f)
		print('</body>',file=f)
		print('',file=f)
		print('</html>',file=f)

def GetJobWorkDir(JobFile):
	'''Extract the job (working) directory from the output file.'''#5/6/17 COC: copied from ppTaskCrawler.py
	with open(JobFile,'r') as f:
		for line in f:#.iter_lines():
			if line:
				line = line.strip()#remove newlines
				if line.strip() == '':
					pass
				else:
					if BasePath in line:
						return(line)
	return(False)

def GetAllTargets(OutputFolder):
	FolderList = CrawlTree(OutputFolder)
	AllTargetDict = {}
	for Folder in FolderList:
		FolderParts = Folder.split('/')
#		print('FolderParts: ' + str(FolderParts))
		if Folder[-1] != '/':
			Folder += '/'
		OutFiles = glob.glob(Folder + '*.out')#os.listdir(Folder)
#		print('Outfiles: ' + str(OutFiles))
		for File in OutFiles:
			if File.split('.out')[0][-1] == '_':
#				print('Correcting Filename of ' + File)
				File = File.split('.out')[0][0:-1] + '.out'
#				print('... to: ' + File)
				
#			print('File: ' + str(File))
			TargetID = File.split('/')[-1].split('.out')[0]
			if TargetID not in AllTargetDict.keys():
				AllTargetDict[TargetID] = {}
			if 'pp_run' in FolderParts:
				if 'Finished' in FolderParts:
					AllTargetDict[TargetID]['pp_runStatus'] = True
				else:
					AllTargetDict[TargetID]['pp_runStatus'] = False
				path = GetJobWorkDir(File)
				if path == False:
					print('Failed to get path for job: ' + str(TargetID))
					path = 'unknown'
				AllTargetDict[TargetID]['path'] = path
			elif 'pp_ident' in Folder:
				if 'Finished' in FolderParts:
					AllTargetDict[TargetID]['pp_identStatus'] = True
				else:
					AllTargetDict[TargetID]['pp_identStatus'] = False
			elif 'pp_distill' in Folder:
				if 'Finished' in FolderParts:
					AllTargetDict[TargetID]['pp_distillStatus'] = True
				else:
					AllTargetDict[TargetID]['pp_distillStatus'] = False
			AllTargetDict[TargetID]['lcLink'] = TargetID + '_lcAll.txt'#need to make this file later
	for Target in AllTargetDict:
		if 'pp_identStatus' not in AllTargetDict[Target].keys():
			AllTargetDict[Target]['pp_identStatus'] = 'unknown'
		if 'pp_runStatus' not in AllTargetDict[Target].keys():
			AllTargetDict[Target]['pp_runStatus'] = 'unknown'
		if 'pp_distillStatus' not in AllTargetDict[Target].keys():
			AllTargetDict[Target]['pp_distillStatus'] = 'unknown'
	return(AllTargetDict)

def ProcessPhotFiles(PhotFile,ThisPath,TargetID):
	with open(ThisPath + TargetID + '_lcAll.txt', 'a') as outfile:
		outfile.write('This Item: ' + PhotFile)
		outfile.write('This Path:' + ThisPath)
		outfile.write('')
		outfile.write('')
		try:
			with open(PhotFile + '.AmpPer') as infile:
				outfile.write('')
				outfile.write('.AmpPer Data: ')
				for line in infile:
					outfile.write(line)
				outfile.write('')
		except:
			print('Failed to read ' + str(PhotFile + '.AmpPer'))
		try:
			with open(PhotFile + '.vartools_t_mag_err') as infile:
				outfile.write('')
				outfile.write('.vartools_t_mag_err Data: ')
				for line in infile:
					outfile.write(line)
				outfile.write('')
		except:
			print('Failed to read ' + str(PhotFile + '.vartools_t_mag_err'))
		try:
			with open(PhotFile + '.vartools_stats') as infile:
				outfile.write('')
				outfile.write('.vartools_stats Data: ')#label for the section in the file
				for line in infile:
					outfile.write(line)
				outfile.write('')
		except:
			print('Failed to read ' + str(PhotFile + '.vartools_stats'))
		try:
			with open(PhotFile + '.vartools_FinalResults') as infile:
				outfile.write('')
				outfile.write('.vartools_FinalResults Data: ')
				for line in infile:
					outfile.write(line)
				outfile.write('')
		except:
			print('Failed to read ' + str(PhotFile + '.vartools_FinalResults'))


def GetTargetInfo(TargetID,SingleTargetDict):
#	print(TargetID + ' SingleTargetDict=' + str(SingleTargetDict))
	ThisPath = SingleTargetDict['path']
	if ThisPath[-1] != '/':
		ThisPath += '/'

	#ldac files from pp_run
	SingleTargetDict['ldacCount'] = len(glob.glob(ThisPath + '*.ldac'))

	#Find results html file:
	ResultFile = glob.glob(ThisPath + '.diagnostics/*results.html')
	ResultFileType = type(ResultFile).__name__
#	print(ResultFile)
	if ResultFileType == 'None':
		ResultFile == 'missing'
#	print('ResultFile for path ' + ThisPath + '.diagnostics/ with ' + TargetID + ': ')
	SingleTargetDict['DiagLink'] = ResultFile

	#pp_run files *ldac
	
	# ident files are position dat files
	pp_identCount = len(glob.glob(ThisPath + 'positions*.dat'))
	SingleTargetDict['pp_identCount'] = pp_identCount
	
	# distill files are photfiles, see later
	
	# pp_parseStatus# maybe later
	pp_parseStatus = ''
	SingleTargetDict['pp_parseStatus'] = pp_parseStatus
		
	#ppParse File Count
	ppParseFiles = len(glob.glob(ThisPath + '*.varformat'))
	SingleTargetDict['ppParseFiles'] = ppParseFiles
	
	#AmplitudePeriod Status; to do later 5/6/17 COC
	AmpPerStatus = ''
	SingleTargetDict['AmpPerStatus'] = AmpPerStatus
	
	#AmplitudePeriod File Count
	AmpPerCount = len(glob.glob(ThisPath + '*.AmpPer'))
	SingleTargetDict['AmpPerCount'] = AmpPerCount
	
	#Vartools Status (State)
	VarToolsStatus = ''#later 5/6/17 COC
	SingleTargetDict['VarToolsStatus'] = VarToolsStatus
	
	#Vartools Status File Count
	VarStatCount = ''#for later 5/6/17 COC
	SingleTargetDict['VarStatCount'] = VarStatCount
	
	#Vartools t_mag_err File Count
	VartoolsTmpCount = len(glob.glob(ThisPath + '*.vartools_t_mag_err'))
	SingleTargetDict['VartoolsTmpCount'] = VartoolsTmpCount
	
	#Vartools Stats Files Count
	VarToolsStatsCount = len(glob.glob(ThisPath + '*.vartools_stats'))
	SingleTargetDict['VarToolsStatsCount'] = VarToolsStatsCount

	#Vartools Final Results File Count
	VarFinalResultsCount = len(glob.glob(ThisPath + '*.vartools_FinalResults'))
	SingleTargetDict['VarFinalResultsCount'] = VarFinalResultsCount
	
	#Process Phot Files (combine them, etc)
	PhotFiles = glob.glob(ThisPath + 'photometry_*.dat')
	PhotFileCount = len(PhotFiles)
	SingleTargetDict['PhotFileCount'] = PhotFileCount
	try:
		os.remove(ThisPath + 'TargetID_lcAll.txt.bak')
	except:
		pass
	try:
		os.rename(ThisPath + 'TargetID_lcAll.txt', ThisPath + 'TargetID_lcAll.txt.bak')
	except:
		pass
	for PhotFile in PhotFiles:
		ProcessPhotFiles(PhotFile=PhotFile,ThisPath=ThisPath,TargetID=TargetID)
	return(SingleTargetDict)

def ParseAllFiles(OutputFolder,outputfile='A520results.html'):
	'''OutputFolder should be the output folder from the book keeping, e.g. /common/contrib/classes/ast520/output/'''
	outputfile = BaseOutputFolder + outputfile#put it there
	print('Crawling ' + OutputFolder + ' ...')
	AllTargets = GetAllTargets(OutputFolder)
	print('Creating table html file and adding rows...')
	BeginTable(outputfile)
	for Target in AllTargets.keys():
		print('Parsing ' + str(Target) + ' ...')
		AllTargets[Target] = GetTargetInfo(Target, AllTargets[Target])
		WriteRow(OutputFile=outputfile,
				ID=Target,
				FinalStatus='',#maybe later
				Folder=AllTargets[Target]['path'],
				DiagLink=AllTargets[Target]['DiagLink'],
				pp_runStatus=AllTargets[Target]['pp_runStatus'],
				pp_runCount=AllTargets[Target]['ldacCount'],#careful, different key name!
				pp_identStatus=AllTargets[Target]['pp_identStatus'],
				pp_identCount=AllTargets[Target]['pp_identCount'],
				pp_distillStatus=AllTargets[Target]['pp_distillStatus'],
				pp_distill_LC_count=AllTargets[Target]['PhotFileCount'],#careful, different key name!
				pp_parseStatus=AllTargets[Target]['pp_parseStatus'],
				pp_parse_varformatCount=AllTargets[Target]['ppParseFiles'],#careful, different key name!
				AmpPerStatus=AllTargets[Target]['AmpPerStatus'],
				AmpPerCount=AllTargets[Target]['AmpPerCount'],
				VarToolsStatus=AllTargets[Target]['VarToolsStatus'],
				VartoolsTmpCount=AllTargets[Target]['VartoolsTmpCount'],
				VarStatCount=AllTargets[Target]['VarStatCount'],
				VarFinalCount=AllTargets[Target]['VarFinalResultsCount'],
				lcLink=AllTargets[Target]['lcLink'])
	print('Finishing html file...')
	FinishTable(outputfile)
	print('Done!')

ParseAllFiles(OutputFolder=BaseOutputFolder)
