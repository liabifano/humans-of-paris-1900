# Humans of Paris 1900

Project of Foundation of digital humanities (DH-405). The description is available [here](http://fdh.epfl.ch/index.php/Sketch_of_Humans_of_Paris_1900). 

Group: Leonore Guillain; Haeeun Kim; Liamarcia Bifano

## How to use it
   
   ### Run application locally (dockerized)
   
   You need: 
   - [conda](https://docs.conda.io/en/latest/) >= 4.7.12
   - [python](https://www.python.org/downloads/release/python-366/) >= 3.6.6
   - [Docker command line](https://docs.docker.com/engine/reference/commandline/cli/) >= 18.09.2
   
   then run: 
   ```
   conda --version
   python --version
   docker --version
   make install
   make run
   ```
   then open [here](http://127.0.0.1:5000/)
   
   ### Run application locally (without docker)
   ```
   make install
   bash run-gunicorn.sh
   ```
   then open [here](http://127.0.0.1:5000/)
   
   
   ### Deploy pre-built application in AWS
   WIP
   

If you want to use the environment with jupyter notebook run:
 ```bash
 make install
 conda install ipykernel # or pip install ipykernel
 python -m ipykernel install --user --name humans-of-paris --display-name "Humans of Paris"
 ```
 and then select Humans of Paris on the top of your notebook.


## Project Structure
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data           
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    ├── src                <- Source code for use in this project, mainly with the visualization
