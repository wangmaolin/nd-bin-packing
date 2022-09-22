# Environmne Setup Through Miniconda
conda activate 

pip install cvxpy

conda install -c conda-forge coin-or-cbc

pip install cylp

(Tested on macOS Monteray and Ubuntu 18.04)

# Problem Defination

The input is a 2D array($n \times p$) named bit_map $B$. It has $n$ rows and $p=16$ columns. Each element in the array is either 0 or 1. Here is an example of $n=10$:

 [0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0]

 [0 0 0 0 1 1 0 0 1 1 0 0 0 1 0 0]

 [1 0 0 0 0 1 0 1 1 0 0 1 0 0 1 0]

 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]

 [0 0 0 0 1 0 1 0 0 1 0 0 1 0 1 0]

 [1 0 1 0 0 1 0 1 0 0 0 1 0 0 0 0]

 [1 0 0 0 0 0 1 0 1 0 0 1 0 1 0 0]

 [1 0 0 1 1 1 0 0 0 0 0 0 1 0 0 1]

 [0 0 0 1 0 0 1 0 1 0 1 0 0 0 0 0]

 [0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1]


## Objective
Define a box as one row of 16 columns.
$k$ rows of $B$ can be put in the same box if the 1s are prefectly interleaved.

In the above example, row 1 and row 2 can't be put into the same box because both 14th column of these 2 rows are 1. It's okay to put row 1, 9 and 10 into the same box.

The object is to find a way to pack these rows so the number of boxes is minimized. The way of packing can be described as a 1D array $S$ of size $n$. Assume that box is enumerated from top to down(the first row is box 0). $S_k=t$ means the $k$ th row should be put in the $t$ th box.

Here is an sample solution for the above example:[0, 1, 0, 1, 2, 2, 3, 4, 5, 5].

# CVXPY Description
A CVXPY modeling of the problem can be found as the cvx_condense function in vector_packing.py. It's based on the following example:
https://stackoverflow.com/questions/48866506/binpacking-multiple-constraints-weightvolume

# Problem Scale
Current maximum $n$ is about $60,000$ in the OSQP benchmarks.
The current hardware uses $p=16$.
Later $p$ will scaled to $p=16 \times 5$ and $p=16 \times 12$ on larger hardware.