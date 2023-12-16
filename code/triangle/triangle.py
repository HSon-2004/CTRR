import os, sys, argparse
from time import perf_counter as time
from glob import glob
import os,sys
from pandas import read_csv
from scipy.sparse import csr_matrix
from scipy.sparse import coo_matrix


#==========================triangle Function==============================#

# the input file is in mmio format
def triangle(adj_file, inc_file):

    dataset_name = os.path.split(os.path.split(adj_file)[0])[1]

    print(('Processing ' + dataset_name))
    # figure out the shape of the adjacency matrix
    a = read_csv(adj_file, sep='\s+', header=None, skiprows=2, nrows=1, dtype=float).to_numpy()

    M =int(a[0,0])
    N =int(a[0,1])
    
    # read adjacency matrix
    print('Reading adjacency matrix')
    y = read_csv(adj_file, sep='\s+', header=None, skiprows=3, dtype=float).to_numpy()


    # convert data to sparse matrix using the coo_matrix function
    A = coo_matrix((y[:, 2], (y[:, 0]-1, y[:, 1]-1)), shape=(int(M), int(N)))
    if A.shape == A.transpose().shape:
        A = A + A.transpose()
    else:
        # Handle the case when shapes are not compatible
        print("Inconsistent shapes for addition: {} and {}.".format(A.shape, A.transpose().shape))
        sys.exit(1)

    adjMtx = A.tocsr()

    # figure out shape of incidence matrix
    a = read_csv(inc_file, sep='\s+', header=None, skiprows=2, nrows=1, dtype=float).to_numpy()
    M = int(a[0,0])
    N = int(a[0,1])
    
    # read incidence matrix
    print('Reading incidence matrix'+"\n")
    y = read_csv(inc_file, sep='\s+', header=None, skiprows=3, dtype=float).to_numpy()

    # reshape incidence matrix
    B = coo_matrix( ( y[:,2], (y[:,0]-1, y[:,1]-1) ) , shape=(M,N) )
    incMtx = B.tocsr()

    # count triangles
    print('Counting triangles')
    C =  adjMtx * incMtx
    num_triangles = (C==2).nnz/3

    print('Number of triangles in ' + dataset_name + ' : ' + str(num_triangles))

    return num_triangles


#==========================Main Function==============================#

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("adj_file", nargs="?", action="store", type=str, default="H_adj.mmio")
    parser.add_argument("inc_file", nargs="?", action="store", type=str, default="H_inc.mmio")
    args = parser.parse_args()

    inc_file = args.inc_file
    adj_file = args.adj_file

    # Handle the case when the file is error
    if not os.path.isfile(inc_file):
        print("File doesn't exist: '{}'!".format(inc_file))
        sys.exit(1)
    elif not os.path.isfile(adj_file):
        print("File doesn't exist: '{}'!".format(adj_file))
        sys.exit(1)

    print("Running 'triangle' function with adj_file={} and inc_file={}".format(adj_file, inc_file))

    # run triangle function
    triangle(adj_file, inc_file)

    print("Execution completed.")




