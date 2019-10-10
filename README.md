# Humans of Paris 1900

Project of Foundation of digital humanities (DH-405). The description is available [here](http://fdh.epfl.ch/index.php/Sketch_of_Humans_of_Paris_1900). 

Group: Leonore Guillain; Haeeun Kim; Liamarcia Bifano


## Setup

To create the conda environment and run the unit tests:

```bash
make install
make test
```

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
