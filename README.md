<!-- #region -->
[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)


# [Unified framework for choice-based facility location problem](https://doi.org/10.1287/ijoc.2022.0366)

This archive is distributed in association with the [INFORMS Journal on Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

This repository contains supporting material for the paper 
 
    "Unified framework for choice-based facility location problem" by Yun Hui Lin, Qingyun Tian and Yanlu Zhao.

The software and data in this repository are a snapshot of the software and data that were used in the research reported on in the paper.


## Cite

To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

https://doi.org/10.1287/ijoc.2022.0366

https://doi.org/10.1287/ijoc.2022.0366.cd

Below is the BibTex for citing this snapshot of the respoitory.

```
@article{Lin2024,
  author =        {Y.H. Lin, Q. Tian, and Y. Zhao},
  publisher =     {INFORMS Journal on Computing},
  title =         {Unified framework for choice-based facility location problem},
  year =          {2024},
  doi =           {10.1287/ijoc.2022.0366},
  url =           {https://github.com/INFORMSJoC/2022.0366},
}
```


## Description
The choice-based facility location (CBFL) problem arises in various industrial and business contexts. The problem is based on a decentralized perspective: Companies set up chains of facilities, and customers determine from which chain or facility to seek service according to their own preferences. Essentially, customer preferences or choices play a key role in characterizing various CBFL problems, which differ mainly in the models or rules employed to characterize the choice. Consequently, a large number of formulations appear and are often solved by dedicatedly designed approaches in the literature. Such a situation significantly complicates practitioners' decision-making process when they are facing practical problems but are unsure which ad hoc model is suitable for their cases. In this article, we address this dilemma by providing a unified modeling framework based on the concept of preference dominance.  Specifically, we conceptualize the choice behavior as a sequential two-step procedure: Given a set of open facilities, each customer first forms a nondominated consideration set and then splits the buying power within the set. Such an interpretation renders practitioners high modeling flexibility, as they can tailor how preference dominance is constructed according to their specific contexts. In particular, we show that our model can represent several streams of CBFL problems. To support the applicability of our model, we design an efficient exact decomposition algorithm. Extensive computational studies reveal that although the algorithm is designed for a general purpose, it outperforms most approaches that are tailored for ad hoc problems by a large margin, which justifies both the effectiveness and the efficiency of the unified framework.

This repository provides data for the problem and code for the algorthm. The main folders are 'data', 'src', and 'results'.

- 'data': four datasets generator (and instances) used in the paper.

- 'src': the source code for the decomposition algorithm.

- 'results': high-resoultion figures in our paper

All experimental results can be found in the paper (manuscript and electronic companion).


## Replicating

- To run the code, you will need to make sure that you have already installed **Anaconda3**.

- You also need to install the solver **CVXPY**, **Gurobi 9.5.2** (license required), and **MOSEK** (license required).

Once the environment has set up, run the Data Generator code to generate the problem instance, and run the GBD algorithm code for generating and solving the instance. 

For example, to generate the data for the UPHM-CBFL instances, run 'Data_UPHM.py'. To generate and solve UPHM-CBFL instances, simply run 'GBD_UPHM.py'.

The other tests also follow the same procedure. 


## Results

All results have been reported in the paper Section 6 and EC.4. In addition, we report the figures of our paper in the Folder 'results'


## License

This software is released under the MIT license, which we report in file 'LICENSE'.
