## Multi-modal Dynamic User Equilibrium (MMDUE) with Multi-class Vehicles, Ridesharing, Public Transit and Parking

Implemented by Wei Ma and Xidong Pi (AlanPi1992), advised by Sean Qian, Civil and environmental engineering, Carnegie Mellon University. 


### Requirements

- cvxopt 1.1.9
- numpy 1.14.2
- MNMAPI: MNMAPI is a traffic simulation library developed by MAC in CMU, please refer to https://github.com/Lemma1/MAC-POSTS and http://mac-posts.com/
- MNM_mcnb: the folder interface to MNMAPI, please refer to https://github.com/Lemma1/MAC-POSTS/tree/master/side_project/network_builder

### Instructions

Please clone the whole repo, and run renner.ipynb using jupyter notebook.

### Experiments

To check the details of the experiments in exp_config.py, please refer to the paper.

### File specifications

- src/exp_config.py: experiment settings in the paper
- src/gp.py: gradient projection method
- src/models.py: implementation of multi-modal DUE
- src/runner.ipynb: script that runs the MMDUE
- img/.: imagines used in the paper
- data/input_files_small_multiclass: experiment network in the paper


### Questions

For any question, please contact Wei Ma (Lemma171@gmail.com) and Xidong Pi (xpi@andrew.cmu.edu).