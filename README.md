INFORMS Journal on Computing Logo

A New Approximation Algorithm for Minimum-Weight $(1,m)$--Connected Dominating Set

This archive is distributed in association with the INFORMS Journal on Computing under the MIT License.

The software and data in this repository are a snapshot of the software and data that were used in the research reported on in the paper A New Approximation Algorithm for Minimum-Weight $(1,m)$--Connected Dominating Set
by Jiao Zhou

Cite

To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

https://doi.org/10.1287/ijoc.2023.0306

https://doi.org/10.1287/ijoc.2023.0306.cd

Below is the BibTex for citing this snapshot of the repository.

@misc{Antoniadis2024,
  author =        {Jiao Zhou},
  publisher =     {INFORMS Journal on Computing},
  title =         {A New Approximation Algorithm for Minimum-Weight $(1,m)$--Connected Dominating Set},
  year =          {2024},
  doi =           {10.1287/ijoc.2023.0306.cd},
  url =           {https://github.com/INFORMSJoC/2023.0306},
  note =          {Available for download at https://github.com/INFORMSJoC/2023.0306},
}  

Description

The goal of this repository is to demonstrate the efficiency of our algorithm for Minimum-Weight $(1,m)$--Connected Dominating Set.

The algorithm is implemented by three python scripts, ../src/algorithm_GK.py, ../src/algorithm_two_step.py and ../src/algorithm_OPT.py.

1. algorithm_GK.py compares the algorithm proposed in this paper with the GK algorithm, 
   including comparisons between the weights of the computed CDSs and the runtime of the program. 
   Experimental results are in document results_GK.txt
   The results illustrate the outputs of the two algorithms are nearly identical. 
   However, our algorithm is significantly faster. On a graph of size 10, 
   our algorithm outpaces the GK algorithm by $4.4\times 10^{-3}$. 
   As graph sizes increase, the advantage of our algorithm's running time becomes increasingly apparent. 
   For a graph with 50 nodes, our algorithm is faster than the GK algorithm by $2\times 10^{-5}$.

2. algorithm_two_step.py compares the weights of computed $(1,3)$-CDSs using our algorithm 
   and the latter two-step algorithm presented in Zhou. Experimental results are in document results_two_step.txt. 
   The results show that the weights of the solutions computed by our algorithm is at least $20\%$ 
   lighter than those computed by the two-step algorithm.

3. algorithm_OPT.py compare the performance of our algorithm with an optimal solution. 
   Experimental results are in document results_OPT.txt. The results show that our solutions 
   are close to the optimal solutions.

Running Algoritm

Run with Python 2.6.6 or later.

Results

The running results are saved in the ../results.

Figure1 show our algorithm and GK algorithm results.
![Figure1-5aaa](https://github.com/user-attachments/assets/eab47149-6c69-4271-9fbb-b88e5a719639)

Figure2 show our algorithm and two-step algorithm results.
![Figure-1aa](https://github.com/user-attachments/assets/7ba1cbe8-e964-4426-ace1-db955dadbb5a)


