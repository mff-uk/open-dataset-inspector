# Open Dataset Visualisation (ODIN)
This tool is designed to support exploration, evaluation and design 
of dataset similarity. 

This tool consists of several sub-projects:
 * data-preparation
 * evaluation
 * odin-backend
 * odin-frontend
 
## data-preparation
This project contains scripts that are responsible for data preparation.

## evaluation
Used to process results of user evaluation done by *odin-frontend*.

### How to run
 * Make sure you have Python (3.5+) installed
 * Make sure you have evaluation files ready in ```./data/evaluation```
 * Install dependencies using 
    ```pip install numpy plotly```
 * Install [Orca](https://github.com/plotly/orca) for plotly
 * Update arguments in the scripts ```evaluate.py``` and ```plot_graphs.py```
 * Run the updated script.

## odin-backend
Provide functionality to compute graph-based dataset similarity. Can be run
as a command line tool or as a web service. The web service is required 
by *odin-frontend* in order to visualize similarity details in *Visualisation*.
It requires data prepared by *data-preparation* project.

### How to run
 * Make sure all data are prepared by *data-preparation*.
 * Make sure you have Python (3.5+) installed
 * Install dependencies using 
 ```pip install flask pyyaml```   
 * Navigate into project directory
 * Start the service by 
 ```python webserver.py```

## odin-frontend
 * Make sure you have evaluation files ready in ```./data/evaluation```
 * Make sure you have *NodeJs* installed
 * Navigate to project directory
 * Run ```npm ci``` to install packages
 * Run ```npm run build``` to build the project
 * Run ```npm run start``` to start the web server
