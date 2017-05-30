catatt
==============================

MEG project on temporal dynamics of category-based attention

Project Organization
------------

    ├── LICENSE
    ├── Makefile           				<- Makefile with commands like `make data` or `make train`
    ├── README.md          				<- The top-level README for developers using this project.
    ├── data                                                                    
    │   ├── external       				<- Data from third party sources.                   
    │   ├── interim        				<- Intermediate data that has been transformed or modified.     
    │   ├── processed      				<- The final, canonical data sets for analyses.     
    │   └── raw            				<- The original, immutable data dump.               
    │                                                                           
    ├── notebooks          				<- Jupyter notebooks. Naming convention is a number (for ordering),
    │                      	  			 the creator's initials, and a short `-` delimited description, e.g.
    │                      	  			 `1.0-jqp-initial-data-exploration`.              
    │                                                                           
    ├── support            				<- Data dictionaries, manuals, and all other explanatory materials, 
    │                                    including debriefing etc. from experiment. 
    │                                                                           
    ├── reports            				<- Generated analysis as HTML, PDF, LaTeX, etc.     
    │   └── figures        				<- Generated graphics and figures to be used in reporting
    │                                                                           
    ├── requirements.txt   				<- The requirements file for reproducing the analysis environment, e.g.
    │                      	   			generated with `pip freeze > requirements.txt`   
    │                                                                           
    └── code               				<- Source code for use in this project.            
        ├── __init__.py    				<- Makes `code` a Python module                        
    	│                                                                           
        ├── analyses       				<- Scripts to analyze the data                      
        │                                                                       
        ├── base        			   	<- Base python functions used to analyze the data   
        │   ├── __init__.py				<- Makes `base` a Python module   
	    │   ├── formatting_basics.py    <- Functions to format data for plotting or for statistics
	    │   ├── plotting_basics.py      <- Functions to plot data
	    │   └── statistics_basics.py    <- Functions for basic statistical analyses
        │
        ├── data       					<- Scripts to format and transform raw data
        │
        ├── presentation         		<- Scripts generate experimental trials and present the experiment
        │   ├── present_experiment.py	<- Experiment presentation script
	    │   ├── generate_trials.py		<- Trial generation script
	    │   ├── img      				<- Stimuli used
	    │   └── trials    				<- Trials generated
        │
        └── visualization  				<- Scripts to create exploratory and results oriented visualizations
            └── visualize.py
    


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
