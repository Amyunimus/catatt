from psychopy import core, visual, gui, data, misc, event
import os, glob
import pickle
import random

#TODO: 
# - Make nice GUI for getting subject info
# - Load images into memory
# - Make the data output better
# - Unhard code what was hard coded in. 


meg = True
use_loaded_files = True
expName = 'catAtt'
subject = 's028'
version = 0
start_at_trial = 0

if meg:
	import serial
	ser = serial.Serial()
	ser.port = 'COM1'
	ser.baudrate = 115200
	ser.bytesize = serial.EIGHTBITS
	ser.parity = serial.PARITY_NONE
	ser.stopbits = serial.STOPBITS_ONE
	ser.timeout = 2.5
	
	ser.open()
	ser.read()

	print ser.name
	print ser
	
	


with open(subject+'_all_trials.pkl', 'rb') as handle:
	all_trials = pickle.load(handle)
	all_trials = all_trials[start_at_trial:]
	print len(all_trials)

### Define Blocks ###

welcome_block = {
	'type':'supporting',
	'text':"Welcome to the experiment! Experimenter will press any key to continue"
}

instructions_block = {
	'type':'supporting',
	'text':"Using to blue and yellow button, respond whether or not you saw the target picture in the stream of pictures. Sometimes the target word will occur before the pictures, sometimes it will occur after the pictures.\n\
	Sometimes there will not be any cue and you will just have to press the top or bottom button. Sometimes there will be a word before AND after the images and you will have to respond if you saw BOTH or just ONE of the targets.",
	'timing_post_trial': 0 #time before experiment starts
}

ready_block = {
	'type':'supporting',
	'text':"Ready? The experiment will begin shortly.",
	'timing_post_trial': 1.00 #time before experiment starts
}

debriefing_block = {
	'type':'supporting',
	'text':"The experiment is over!",
}

test_block = {
	'type': 'experimental',
	'timeline': all_trials
}



### Create Experiment Timeline ###
timeline = []
timeline.append(welcome_block)
timeline.append(instructions_block)
timeline.append(ready_block)
timeline.append(test_block)
timeline.append(debriefing_block)


# class Exp:
#	 def __init__(self):
# 
#		 #this is where the subject variables go.  'any' means any value is allowed as long as it's the correct type (str, int, etc.) the numbers 1 and 2 control the order in which the prompts are displayed (dicts have no natural order)
#		 self.optionList = {	'1':  {	'name' : 'subject_code',
#									 'prompt' : 'Subject Code: ',
#									 'options': 'any',
#									 'default':'sub000ses00',
#									 'type' : str},
#							 '2' : {	'name' : 'gender',
#									 'prompt' : 'Subject Gender (m/f): ',
#									 'options' : ("m","f"),
#									 'default':'',
#									 'type' : str},
#							 '3' : {	'name' : 'meg',
#									 'prompt' : 'Using MEG?:',
#									 'options' : ("yes","no"),
#									 'default':'no',
#									 'type' : str},
#							 '4' : {	'name' : 'experiment_name',
#									 'prompt' : 'Experiment Name: ',
#									 'options' : 'any',
#									 'default' : 'catAtt',
#									 'type' : str}
#								 }
# 
#		 optionsReceived=False
#		 fileOpened=False
#		 while not optionsReceived or not fileOpened:
#			 [optionsReceived,self.subjVariables] = enterSubjInfo('rsvp',self.optionList)
#			 if not optionsReceived:
#				 popupError(self.subjVariables)
#			 try:
#				 if  os.path.isfile(self.subjVariables['subjCode']+'_test.txt'):
#					 fileOpened=False
#					 popupError('Error: That subject code already exists')
#				 else:
#					 self.outputFileTest = file('test_'+self.subjVariables['subjCode']+'.txt','w')
#					 fileOpened=True
#			 except:
#				 pass
#		 # generateTrials.main(self.subjVariables['subjCode'],self.subjVariables['seed'])
#		 # 
#		 # if self.subjVariables['responseDevice']=='gamepad':
#		 #	 try:
#		 #		 self.stick=initGamepad()
#		 #		 pygame.init()
#		 #		 self.inputDevice = "gamepad"
#		 #		 self.responseInfo = " Press the GREEN key for 'Yes' and the RED' button for 'No'."
#		 #		 self.validResponses = {'1':0,'0':3}
#		 #		 assert False, 'Left right responses not implemented for gamepad. Try keyboard'
#		 #		 self.leftRightResponses = dict()
#		 #		 self.leftRightResponseInfo = ""
#		 #	 except SystemExit:
#		 #		 self.subjVariables['responseDevice']='keyboard'
#		 # 
#		 # if self.subjVariables['responseDevice']=='keyboard':
#		 #	 print "Using keyboard"
#		 #	 self.inputDevice = "keyboard"
#		 #	 self.validResponses = {'1':'up','0':'down'} #change n/o to whatever keys you want to use
#		 #	 self.leftRightResponses = {'left': 'left', 'right': 'right'}
#		 #	 self.responseInfo = "Press the up arrow if you saw the target and the down arrow if you didn't see the target."
#		 #	 self.leftRightResponseInfo = "Press the left arrow if you saw the left image or the right arrow if you saw the right image."
#		 # 



class PresentSupporting(object):
	
	def __init__(self,win,block):
		self.win = win
		self.trial_clock = core.Clock()
		self.text = block['text']
		
		try:
			self.timing_post_trial = block['timing_post_trial']
		except KeyError:
			self.timing_post_trial = 0
		
	def display_text(self):
		self.trial_clock.reset()
		text_display = visual.TextStim(self.win, pos=[0,0],wrapWidth=15,
			color=[-1,-1,-1],height=.7,text=self.text)
		text_display.draw()
		self.win.flip()
#		if meg:
#			responded = False
#			while not responded:
#				responded = ser.read()
#		else:
		event.waitKeys(keyList=['x'])
		
		self.trial_clock.reset()
		while self.trial_clock.getTime() < +self.timing_post_trial:	
			self.win.flip()
			

class PresentTrial(object):
	def __init__(self,win,trial,fileMatrix):
		self.win = win
		self.trial_clock = core.Clock()
		self.stim_clock = core.Clock()
		self.response_clock = core.Clock()
		
		self.trial = trial
		self.fileMatrix =  fileMatrix
		self.choices =  trial['choices']
		self.correct_response =  trial['correct_response']
		self.key_mappings = trial['key_mappings']
		self.trial_structure_data = trial['trial_structure_data']

			
	def display_trial(self):
		self.trial_clock.reset()
		
		for j, item in enumerate(self.trial_structure_data):
			
			actual_timing_list = []
			if item['start_response_timer']:
				self.response_clock.reset()
				event.clearEvents()
			else:
				pass
			
			if item['trial_part_type'] == 'response_separate': #does the response screen stand alone
				responded = PresentTrial.display_response(self,item)
			
			elif item['trial_part_type'] == 'response': # or do you just want to get the response after the stimulus
				responded = PresentTrial.get_response(self,item)
				
			else:
				actual_timing = PresentTrial.display_all(self,item)
				self.trial_structure_data[j]['actual_timing'] = actual_timing
				
		self.trial['total_trial_time'] = self.trial_clock.getTime()
		return responded

	def display_all(self,trial_part):
		self.stim_clock.reset()
		
		if meg:
			try:
				value = 9 #trial starte
				ser.write(chr(value))
			except KeyError:
				pass
	
		stim_displays_list = [] #to enable more than one stim simultaneously
		
		if trial_part['stimulus']:
			for i, stim in enumerate(trial_part['stimulus']):			    			 
				try:
					full_path = trial_part['stimulus_path'] + stim + '.' + trial_part['stimulus_ext']
					#print full_path
					#print os.path.exists(full_path)
				
				except TypeError:
					full_path = 'no_image'
							
				if trial_part['trial_part_type'] == 'single-stim':
					frame_size = 660
					frame = visual.Rect(self.win,pos = (0, 0), lineColor = 'black', units='pix', size=[frame_size,frame_size])
					
					if os.path.exists(full_path):
						try:
							if use_loaded_files:
								stim_display =  self.fileMatrix[stim]['stim']
							else:
								stim_display = visual.PatchStim(self.win, pos=trial_part['stimulus_positions'][i], tex=full_path, units='pix', size=[256,256])
						except IOError:
							#maybe just load the backup image?
							if use_loaded_files:
								stim_display =  fileMatrix[stim]['stim']
							else:
								stim_display = visual.PatchStim(self.win, pos=trial_part['stimulus_positions'][i], tex='img/shoe_5.png', units='pix', size=[256,256])
							
					elif stim: #if stim is a thing (not False)
						stim_display = visual.TextStim(self.win, pos=trial_part['stimulus_positions'][i], wrapWidth=15, color=[-1,-1,-1],height=.7,
							text=stim)
					else: 
						stim_display = visual.TextStim(self.win, pos=trial_part['stimulus_positions'][i], wrapWidth=15, color=[-1,-1,-1],height=.7,
							text="")
				elif trial_part['trial_part_type'] == 'cue':
					frame_size = 660
					frame = visual.Rect(self.win,pos = (0, 0), lineColor = 'black', units='pix', size=[frame_size,frame_size])					
					if stim: #if stim is a thing (not False)
						stim_display = visual.TextStim(self.win, pos=trial_part['stimulus_positions'][i], wrapWidth=15, color=[-1,-1,-1],height=.7,
							text=stim)
						override_fixation = False
						fixation_color = False
					else: 
						stim_display = visual.TextStim(self.win, pos=trial_part['stimulus_positions'][i], wrapWidth=15, color=[-1,-1,-1],height=.7,
							text="")
						override_fixation = True #If there could be a cue but there is not, show fixation
						fixation_color = 'black'						
							
				elif trial_part['trial_part_type'] == 'blank':
					stim_display = visual.TextStim(self.win, pos=trial_part['stimulus_positions'][i], wrapWidth=15, color=[-1,-1,-1],height=.7,
						text="")
					frame_size = 660
					frame = visual.Rect(self.win,pos = (0, 0), lineColor = 'black', units='pix', size=[frame_size,frame_size])
						
				stim_displays_list.append(stim_display)		
		elif not trial_part['stimulus']:
			stim_display = visual.TextStim(self.win, pos=[0,0],wrapWidth=15,color=[-1,-1,-1],height=.7,
				text="")
			stim_displays_list.append(stim_display)

		
		if trial_part['fixation']:
			fixation_display = visual.TextStim(self.win, pos=[0,0],wrapWidth=15,color=trial_part['fixation'],height=.7,
				text="+")
		elif not trial_part['fixation']:
			if override_fixation:
				fixation_display = visual.TextStim(self.win, pos=[0,0],wrapWidth=15,color=fixation_color,height=.7,
					text="+")
				override_fixation = False #reset for next part
				fixation_color = False
			else:
				fixation_display = visual.TextStim(self.win, pos=[0,0],wrapWidth=15,color=[-1,-1,-1],height=.7,
					text="")
			
		# Present stimulus
		if meg:
			try:
				value = trial_part['meg_code']
				ser.write(chr(value))
			except KeyError:
				pass

		
		if trial_part['timing']:
			while self.stim_clock.getTime() < trial_part['timing']:
				for stim_display in stim_displays_list:
					stim_display.draw()
				fixation_display.draw()
				frame.draw()
				self.win.flip()
			actual_timing = self.stim_clock.getTime()
		else:
			for stim_display in stim_displays_list:
				stim_display.draw()
			fixation_display.draw()
			frame.draw()
			self.win.flip()
			actual_timing = 'NaN'
		
		return actual_timing
			
	
	def display_response(self,trial_part):
		self.stim_clock.reset()
		
		if trial_part['start_response_timer']:
			self.response_clock.reset()
			event.clearEvents()
		else:
			pass
		# Present stimulus
		if meg:
			try:
				value = trial_part['meg_code']
				ser.write(chr(value))
			except KeyError:
				pass

		response_display = visual.Circle(self.win,fillColor='red', radius=0.5)
		response_display.draw()
				
		try: 
			print self.trial['trial_num'], self.trial['target_identity'],
			if self.trial['cue_type'] == 'nocue':
				updown = ['top','bottom']
				a = random.choice (updown)
				
				if a == 'top':				
					text1 = 'top'
					text2 = ''
				else:
					text1 = ''
					text2 = 'bottom'
					
			
			elif len(self.trial['target_identity']) == 2:
				text1 = 'both'
				text2 = 'one'
			else:
				text1 = 'absent'
				text2 = 'present'
		except TypeError:
			text1 = 'absent'
			text2 = 'present'
			
			
		
		text1_display = visual.TextStim(self.win, pos=[0,2],wrapWidth=15,
			color=[-1,-1,-1],height=.7,text=text1)
		
		text2_display = visual.TextStim(self.win, pos=[0,-2],wrapWidth=15,
			color=[-1,-1,-1],height=.7,text=text2)
		
		text1_display.draw()
		text2_display.draw()		
		
		self.win.flip()
					
		if meg:
			ser.flushInput()
			responded = False
			#core.wait(trial_part['timing'])
			#responded = ser.read()
			
			#while self.stim_clock.getTime() < trial_part['timing']:
				#while not responded:
			responded = ser.read()
			ser.flushInput()
			
			responded_time = self.response_clock.getTime()
			responded = [(responded,responded_time)]
			print responded
			
		else:
			responded = event.waitKeys(maxWait=trial_part['timing'], keyList=self.choices,timeStamped=self.response_clock)   
			
		#Display circle as 'answered' until time is up.
		while self.stim_clock.getTime() < trial_part['timing']:
			response_display.fillColor = 'lightblue'
			response_display.draw()
			self.win.flip()
		 
		return responded
		
				
	def get_response(self,trial_part):
		if trial_part['start_response_timer']:
			self.response_clock.reset()
			event.clearEvents()
		else:
			pass
		
		if trial_part['timing']: #TODO: figure how how to wait for keys, but time out after a certain amount
			if meg:
				responded = ser.read()
				responded_time = self.response_clock.getTime()
				if responded in self.choices:
					responded = (responded,responded_time)
				else:
					responded = []
			else:
				responded = event.getKeys(keyList=self.choices,timeStamped=self.response_clock)
		else:
			if meg:
				responded = False
				while responded not in self.choices:
					responded = ser.read()
				responded_time = self.response_clock.getTime()
				responded = [(responded,responded_time)]
				
			else:
				responded = event.waitKeys(keyList=self.choices,timeStamped=self.response_clock)
		
		return responded
		
	def evaluate_response(self,responded):
		if responded:			
			first_response = responded[0]
			first_response_key = first_response[0]
			trial_rt = first_response[1]
			
			if self.correct_response: #if there is a correct response
				try:
					if self.key_mappings[first_response_key] == self.correct_response:
						trial_correct = 1
						trial_response = self.key_mappings[first_response_key]
					else:
						trial_correct = 0
						trial_response = self.key_mappings[first_response_key]
				except KeyError:
					try:
						trial_correct = 0
						trial_response = self.key_mappings[first_response_key]
					except KeyError:
						trial_correct = 0
						trial_response = 'NaN'
						trial_rt = 'NaN'
						
				
			elif not self.correct_response: #if there is no correct response
				trial_correct = 'NaN'
				trial_response = self.key_mappings[first_response_key]
			
		elif not responded:
			first_response_key = 'NaN' #if witholding response is important, e.g. no-go trials
			try:
				if self.key_mappings[first_response_key] == self.correct_response:
					trial_correct = 1
					trial_response = self.key_mappings[first_response_key]
					trial_rt = 'NaN'
				else:
					trial_correct = 0
					trial_response = self.key_mappings[first_response_key]
					trial_rt = 'NaN'
			
			except KeyError:
				trial_correct = 0
				trial_response = 'NaN'
				trial_rt = 'NaN'
		
		self.trial['trial_correct'] = trial_correct
		self.trial['trial_response'] = trial_response
		self.trial['trial_rt'] = trial_rt
		return (trial_correct,trial_response,trial_rt)
		
		
def init_psychopy_vars():
	win = visual.Window([800,600],color=[1,1,1],fullscr=True,allowGUI=False, monitor='testMonitor', units='deg',screen=1)
	#win = visual.Window([800,600],color=[1,1,1],allowGUI=False, monitor='testMonitor', units='deg',screen=1)
	return win
	
def check_trial_list_headers():
	pass
	##TODO - make a check for absolutely necessary columns
	

def write_to_file(fileHandle,trial,separator='\t', sync=True, writeNewLine=False):
	"""Writes a trial (array of lists) to a previously opened file"""
	line = separator.join([str(i) for i in trial]) #TABify
	if writeNewLine:
		line += '\n' #add a newline
	try:
		fileHandle.write(line)
	except:
		print 'file is not open for writing'
	if sync:
			fileHandle.flush()
			os.fsync(fileHandle)


def loadFiles(directory,extension,fileType,win='',whichFiles='*',stimList=[]):
	""" Load all the pics and sounds. Uses pyo or pygame for the sound library (see prefs.general['audioLib'])"""
	path = os.getcwd() #set path to current directory
	if isinstance(extension,list):
		fileList = []
		for curExtension in extension:
			fileList.extend(glob.glob(os.path.join(path,directory,whichFiles+curExtension)))
	else:
		fileList = glob.glob(os.path.join(path,directory,whichFiles+extension))
	
	fileMatrix = {} #initialize fileMatrix  as a dict because it'll be accessed by file names (picture names, sound names)
	text = 'Loading images...'
	text_display = visual.TextStim(win, pos=[0,0],wrapWidth=15,color=[-1,-1,-1],height=.7,text=text)
	text_display.draw()
	win.flip()
	for num,curFile in enumerate(fileList):
		fullPath = curFile
		fullFileName = os.path.basename(fullPath)
		stimFile = os.path.splitext(fullFileName)[0]
		if fileType=="image":
			try:
				surface = pygame.image.load(fullPath) #gets height/width of the image
				stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
				(width,height) = (surface.get_width(),surface.get_height())
			except: #no pygame, so don't store the image dimensions
				pass
			stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
			(width,height) = (stim.size[0],stim.size[1])
			fileMatrix[stimFile] = {'stim':stim,'fullPath':fullFileName,'filename':stimFile,'num':num,'width':width, 'height':height}
		elif fileType=="sound":
			fileMatrix[stimFile] = {'stim':sound.Sound(fullPath), 'duration':sound.Sound(fullPath).getDuration()}

	#optionally check a list of desired stimuli against those that've been loaded
	if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
		popupError(str(set(stimList).difference(fileMatrix.keys())) + " does not exist in " + path+'\\'+directory) 
	
	return fileMatrix


# 
# def getRunTimeVars(varsToGet,order,expName):
#   """Get run time variables, see http://www.psychopy.org/api/gui.html for explanation"""
#   order.append('expName')
#   varsToGet['expName']= expName
#   try:
#   previousRunTime = misc.fromFile(expName+'_lastParams.pickle')
#   for curVar in previousRunTime.keys():
#       if isinstance(varsToGet[curVar],list) or curVar=="room" or curVar=="date_time":
#         pass #don't load it in
#       else:
#         varsToGet[curVar] = previousRunTime[curVar]
#   except:
#   pass
#   if varsToGet.has_key('room') and varsToGet.has_key('date_time'):
#   infoDlg = gui.DlgFromDict(dictionary=varsToGet, title=expName, fixed=['room','date_time'],order=order)
#   else:
#   infoDlg = gui.DlgFromDict(dictionary=varsToGet, title=expName, fixed=[expName],order=order) 
# 
#   misc.toFile(expName+'_lastParams.pickle', varsToGet)
#   if infoDlg.OK:
#   return varsToGet
#   else: print 'User Cancelled'

def experiment_init(timeline):
    #     while True:
    # runTimeVarOrder = ['subject','gender','MEG']
    # runTimeVars = getRunTimeVars({'subject':'sub000ses00', 'gender':['Choose', 'male','female'], 'MEG': ['Choose', 'Yes', 'No']},runTimeVarOrder,expName)
    # if 'Choose' in runTimeVars.values():
    #     popupError('Need to choose a value from a dropdown box')
    # else:
    #     outputFile = openOutputFile(runTimeVars['subject'],'rsvpMEG')
    #     if outputFile:
    #     break

    
    
	win = init_psychopy_vars()
	
	fileMatrix = loadFiles('img','.png','image',win=win)
	#print 'printing fileMatrix', fileMatrix.keys()
	
	#TODO LOAD IN IMAGES BEFOREHAND
	
		#	 loading = visual.TextStim(win, pos=[0,0], wrapWidth=15,color=[-1,-1,-1],text="Loading...")
		#	 loading.draw()
		#	 win.flip()
		# 
		#	 #Reads images to better timing
		#	 
		#	 for block in timeline:
		#		 if block['type'] == 'supporting':
		#			 current_trial = PresentSupporting(win,block)
		#			 current_trial.display_text()
		#		 else:
		#			 for trial in block['timeline']:
		#	 
		#	 
		#	 loaded_stims =[]
		#	 for thisTrial in trialsImgLoad:
		# stim = visual.PatchStim(win, colorSpace='rgb',tex = 'stims/'+str(thisTrial['scene'])+'_'+str(thisTrial['environment'])+'.png')
		# loaded_stims.append(stim)
	with open(subject+'_output_'+str(version)+'.txt','w') as infile:
	
		for block in timeline:
			if block['type'] == 'supporting':
				current_trial = PresentSupporting(win,block)
				current_trial.display_text()
			else:
				k=1
				for trial in block['timeline']:
					manual_control = event.getKeys()
					if 'q' in manual_control:
						core.quit()
					elif 'p' in manual_control:
						text = 'PAUSED. Experimenter will resume task shortly.'
						text_display = visual.TextStim(win, pos=[0,0],wrapWidth=15,
							color=[-1,-1,-1],height=.7,text=text)
						text_display.draw()
						win.flip()
						event.waitKeys(keyList=['x'])
						win.flip()
						core.wait(.5)
						
						
					##Break ever 62x trials
					if trial['trial_num'] % 62 == 0:
						text = 'Block '+str(k)+' is finished. Please wait for the experimenter to start the next block. Remember to keep your head as still as possible unless directed to shift it.'
						text_display = visual.TextStim(win, pos=[0,0],wrapWidth=15,
							color=[-1,-1,-1],height=.7,text=text)
						text_display.draw()
						win.flip()
						event.waitKeys(keyList=['x'])
						win.flip()
						core.wait(.5)
						k =k+1
						
					current_trial = PresentTrial(win,trial,fileMatrix)
					responded = current_trial.display_trial()
					trial_correct = current_trial.evaluate_response(responded)
				  
				  
					#TODO MAKE THIS A LITTLE MORE AUTOMATIC, maybe input into trial_block defintiion			  
					order = ['trial_num', 'cue_type', 'target_identity', 'target_category','choices', 'correct_response','trial_response','trial_correct','trial_rt','total_trial_time']
					#order = ['trial_num', 'choices', 'trial_response','trial_rt']

					trial_to_print = []

					for item in order:
						trial_to_print.append(trial[item])

					for item in trial['trial_structure_data']:
						if item['trial_part_type'] not in ['blank','response_separate','response']:
						
							#TODO build in better how to return the key AND meaning of key when 
							# the key mapping includes a 0, 1 etc index
							#if [isinstance( x, int ) for x in trial['key_mappings'].values()]:
							#	print item['stimulus'][trial['trial_response']]
						
							trial_to_print.extend([item['stimulus'],[trial['trial_response']], item['stimulus'], item['timing'],item['actual_timing'],item['stimulus_positions']])
							#trial_to_print.extend([item['stimulus'], item['timing'],item['actual_timing'],item['stimulus_positions']])
				
					print trial['trial_num'],"finished." 
					line = '\t'.join([str(i) for i in trial_to_print])
					writeToFile(infile,trial_to_print)
 

def writeToFile(fileHandle,trial,sync=True):
	"""Writes a trial (array of lists) to a fileHandle"""
	line = '\t'.join([str(i) for i in trial]) #TABify
	line += '\n' #add a newline
	fileHandle.write(line)
	if sync:
		fileHandle.flush()
		os.fsync(fileHandle)

def syncFile(fileHandle):
	"""syncs file to prevent buffer loss"""
	fileHandle.flush()
	os.fsync(fileHandle)
		
experiment_init(timeline)