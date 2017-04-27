# 4/13/17 COC: take Photometry Pipeline output and convert into 
# Vartools desired format, including changing JD to JD-J0 where
# I chose J0 to be the integer (pre-decimal) part of the 1st JD
# I successfully analyzed LCs via vartools with this command:
# vartools -i photometry_3199.dat.txt.varformat -inputlcformat t:1,mag:2,err:3-rm -LS 0.1 30. 0.1 4 0 -o tmp.lc -oneline
# command line usage: python ParsePPlc.py lightcurve.dat

import argparse#parse command line arguments 4/13/17 COC
import os
import glob

def ThisFilePath():#this is the path of this Python file 4/13/17 COC
	return(str(os.path.dirname(os.path.realpath(__file__))) + '/')
#print(ThisFilePath())

debug = False
TestFile = ThisFilePath() + 'photometry_3199.dat.txt'

if debug == False:
	parser = argparse.ArgumentParser(description='PhotometryPipeline light curve .dat format to Vartools format file.')
	parser.add_argument('objects', metavar='LightCurveFile', type=str, nargs='+', help='input Photometry Pipeline light curve file; example: python ParsePPlc.py lightcurve.dat')
	args = parser.parse_args()
else:
	args = [Testfile]

def ParsePPlc(ppFile):
	'''Function to take Mommert et. Al Photometery Pipeline light curve output and reformat it for Vartools.
	AST-520 (Prof. Chad Trujillo) Spring 2016; COC === Colin Orion Chandler
	'''
	HashCount = 0#track hashed lines 4/13/17 COC
	JD0 = 0	#per vartools documentation, they prefer JD-JD0 format time values due to roundoff errors
			#I think it's easier to read the output if we only obbset by the pre-decimal part of JD0. 4/13/17 COC
	CleanPP = ppFile.split('/')[-1]#keeps only last item in the split list, so not the full path any longer 4/13/17 COC
	with open (ppFile,'r') as f:
		with open (ppFile + '.varformat','w') as outfile:
			for i,line in enumerate(f):
				if not line:#end of file
					break
				elif line == '':#skip blank lines
					pass
				elif line[0] == '#':#could make this dynamic (movable columns) but prob. not needed 4/13/17 COC
					print(line.strip())#remove newlines with strip 4/13/17 COC
				else:						
					a=line.split()
#					print(a)#for testing, uncomment 4/13/17 COC
					JD = float(a[1]) - JD0#Julian Date, offset by "JD0" 4/13/17 COC
					mag = a[2]#Asteroid Magnitude
					err = a[3]#Asteroid Sigmas
					if i - HashCount == 1:#first non-hashed line 4/13/17 COC
						JD0 = float(str(JD).split('.')[0])
						JD = JD - JD0#correct this first line's time 4/13/17 COC
						print('# JD0=' + str(JD0),file=outfile)#write our JD0 to file 4/13/17 COC
						print('# JD-J0 mag err',file=outfile)#write column headers to file 4/13/17 COC
					TheRow = str(JD) + ' ' + str(mag) + ' ' + str(err)
					print(TheRow)#testing 4/13/17 COC
					print(TheRow,file=outfile)#write to file 4/13/17 COC
	return

#ParsePPlc(TestFile)

for arg in args.objects:#corrected command-line argument parsing 4/26/17 COC
	ParsePPlc(arg)
