from psychopy import core, visual, gui, data, misc, event
import os
import pickle
import random

meg = False

if meg:
    import serial
    ser = serial.Serial()
    ser.port = 'COM1'
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    
    ser.open()

    print ser.name
    print ser



with open('practice_all_trials.pkl', 'rb') as handle:
    all_trials = pickle.load(handle)


### Define Blocks ###

welcome_block = {
    'type':'supporting',
    'text':"Welcome to the experiment! Press any key to continue"
}

instructions_block = {
    'type':'supporting',
    'text':"These are instructions.",
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
timeline.append(test_block)
timeline.append(debriefing_block)

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
        text_display = visual.TextStim(self.win, pos=[0,0],wrapWidth=45,
            color=[-1,-1,-1],height=.7,text=self.text)
        text_display.draw()
        self.win.flip()
        if meg:
            responded = False
            while not responded:
                responded = ser.read() #reads 1 bit
        else:
            event.waitKeys()
        
        self.trial_clock.reset()
        while self.trial_clock.getTime() < +self.timing_post_trial:    
            self.win.flip()
            

class PresentTrial(object):
    def __init__(self,win,trial):
        self.win = win
        self.trial_clock = core.Clock()
        self.stim_clock = core.Clock()
        self.response_clock = core.Clock()
        
        self.trial = trial
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
                        stim_display = visual.PatchStim(self.win, pos=trial_part['stimulus_positions'][i], tex=full_path, units='pix', size=[256,256])
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

        response_display = visual.Circle(self.win,fillColor='red', radius=0.5)
        response_display.draw()
                
        try: 
            print self.trial['target_identity']
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
                text1 = 'present'
                text2 = 'absent'
        except TypeError:
            text1 = 'present'
            text2 = 'absent'
            
            
        
        text1_display = visual.TextStim(self.win, pos=[0,2],wrapWidth=15,
            color=[-1,-1,-1],height=.7,text=text1)
        
        text2_display = visual.TextStim(self.win, pos=[0,-2],wrapWidth=15,
            color=[-1,-1,-1],height=.7,text=text2)
        
        text1_display.draw()
        text2_display.draw()        
        
        self.win.flip()
                    
        if meg:
            responded = False
            while (responded not in self.choices) and (self.stim_clock.getTime() < trial_part['timing']):
                responded = ser.read()
            
            responded_time = self.response_clock.getTime()
            responded = (responded,responded_time)
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
                    trial_correct = 0
                    trial_response = self.key_mappings[first_response_key]
                
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
    win = visual.Window([800,600],color=[1,1,1],fullscr=False,allowGUI=True, 
        monitor='testMonitor', units='deg')
    
    #win = visual.Window(color=[1,1,1],fullscr=True,allowGUI=False, 
    #    monitor='testMonitor', units='pix')
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

def experiment_init(timeline):
    win = init_psychopy_vars()
    
    #TODO LOAD IN IMAGES BEFOREHAND
    
        #     loading = visual.TextStim(win, pos=[0,0], wrapWidth=15,color=[-1,-1,-1],text="Loading...")
        #     loading.draw()
        #     win.flip()
        # 
        #     #Reads images to better timing
        #     
        #     for block in timeline:
        #         if block['type'] == 'supporting':
        #             current_trial = PresentSupporting(win,block)
        #             current_trial.display_text()
        #         else:
        #             for trial in block['timeline']:
        #     
        #     
        #     loaded_stims =[]
        #     for thisTrial in trialsImgLoad:
        # stim = visual.PatchStim(win, colorSpace='rgb',tex = 'stims/'+str(thisTrial['scene'])+'_'+str(thisTrial['environment'])+'.png')
        # loaded_stims.append(stim)

    
    
    
    
    with open('test.txt','w') as infile:
    
        for block in timeline:
            if block['type'] == 'supporting':
                current_trial = PresentSupporting(win,block)
                current_trial.display_text()
            else:
                for trial in block['timeline']:
                    ##Break ever 64 trials
                    if trial['trial_num'] % 61 == 0:
                        text = 'This block is finished. Please wait for the experimenter to start the next block. Remember to keep your head as still as possible unless directed to shift it.'
                        text_display = visual.TextStim(win, pos=[0,0],wrapWidth=15,
                            color=[-1,-1,-1],height=.7,text=text)
                        text_display.draw()
                        win.flip()
                        event.waitKeys(keyList=['x'])
                        
                    current_trial = PresentTrial(win,trial)
                    responded = current_trial.display_trial()
                    trial_correct = current_trial.evaluate_response(responded)
                  
                  
                    #TODO MAKE THIS A LITTLE MORE AUTOMATIC, maybe input into trial_block defintiion              
                    order = ['trial_num', 'cue_type', 'target_identity', 'choices', 'correct_response','trial_response','trial_correct','trial_rt','total_trial_time']
                    #order = ['trial_num', 'choices', 'trial_response','trial_rt']

                    trial_to_print = []

                    for item in order:
                        trial_to_print.append(trial[item])

                    for item in trial['trial_structure_data']:
                        if item['trial_part_type'] not in ['blank','response_separate','response']:
                        
                            #TODO build in better how to return the key AND meaning of key when 
                            # the key mapping includes a 0, 1 etc index
                            #if [isinstance( x, int ) for x in trial['key_mappings'].values()]:
                            #    print item['stimulus'][trial['trial_response']]
                        
                            #trial_to_print.extend([item['stimulus'][trial['trial_response']], item['stimulus'], item['timing'],item['actual_timing'],item['stimulus_positions']])
                            trial_to_print.extend([item['stimulus'], item['timing'],item['actual_timing'],item['stimulus_positions']])
                
                
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