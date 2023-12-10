import os, sys, argparse
from time import perf_counter as time
from glob import glob
import os,sys
from pandas import read_csv
from scipy.sparse import csr_matrix
from scipy.sparse import coo_matrix


#==========================triangle Function==============================#

# the input file is in mmio format
def triangle(adj_mtx_file, inc_mtx_file):

    dataset_name = os.path.split(os.path.split(adj_mtx_file)[0])[1]

    print(('Processing ' + dataset_name))
    # figure out the shape of the adjacency matrix
    a = read_csv(adj_mtx_file, sep='\s+', header=None, skiprows=2, nrows=1, dtype=float).to_numpy()

    M = a[0,0]
    N = a[0,1]
    
    # read adjacency matrix
    print('Reading adjacency matrix')
    t0 = time()
    y = read_csv(adj_mtx_file, sep='\s+', header=None, skiprows=3, dtype=float).to_numpy()

    t_read_adj = time() - t0
    # print read time
    print('Read time: ' + str(t_read_adj) + ' seconds')
    # convert data to sparse matrix using the coo_matrix function
    t0 = time()
    A = coo_matrix((y[:, 2], (y[:, 0]-1, y[:, 1]-1)), shape=(int(M), int(N)))
    if A.shape == A.transpose().shape:
        A = A + A.transpose()
    else:
        # Handle the case when shapes are not compatible
        print("Inconsistent shapes for addition: {} and {}.".format(A.shape, A.transpose().shape))
        sys.exit(1)


    adjMtx = A.tocsr()
    t_adj_reshape = time() - t0

    print('COO to CSR time : ' + str(t_adj_reshape) + ' seconds')

    # figure out shape of incidence matrix
    a = read_csv(inc_mtx_file, sep='\s+', header=None, skiprows=2, nrows=1, dtype=float).to_numpy()
    M = int(a[0,0])
    N = int(a[0,1])
    
    # read incidence matrix
    print('Reading incidence matrix')
    t0 = time()
    y = read_csv(inc_mtx_file, sep='\s+', header=None, skiprows=3, dtype=float).to_numpy()
    t_read_inc = time() - t0

    #print read time
    print('Read time: ' + str(t_read_inc) + ' seconds')

    # reshape incidence matrix
    t0 = time()
    B = coo_matrix( ( y[:,2], (y[:,0]-1, y[:,1]-1) ) , shape=(M,N) )
    incMtx = B.tocsr()
    t_inc_reshape = time() - t0

    print('COO to CSR time : ' + str(t_inc_reshape) + ' seconds' + "\n")

    # count triangles
    print('Counting triangles')
    t0 = time()
    C =  adjMtx * incMtx
    num_triangles = (C==2).nnz/3
    t_triangle_count = time() - t0

    print('triangle count time : ' + str(t_triangle_count) + ' seconds')

    print('number of triangles in ' + dataset_name + ' : ' + str(num_triangles))

    return (num_triangles,t_read_adj,t_adj_reshape,t_read_inc,t_inc_reshape,t_triangle_count)


#==========================Main Function==============================#

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("adj_mtx_file", nargs="?", action="store", type=str, default="A_adj.mmio")
    parser.add_argument("inc_mtx_file", nargs="?", action="store", type=str, default="A_inc.mmio")
    args = parser.parse_args()

    inc_mtx_file = args.inc_mtx_file
    adj_mtx_file = args.adj_mtx_file

    #Handle the case when the file is error
    if not os.path.isfile(inc_mtx_file):
        print("File doesn't exist: '{}'!".format(inc_mtx_file))
        sys.exit(1)
    elif not os.path.isfile(adj_mtx_file):
        print("File doesn't exist: '{}'!".format(adj_mtx_file))
        sys.exit(1)

    print("Running 'triangle' function with adj_mtx_file={} and inc_mtx_file={}".format(adj_mtx_file, inc_mtx_file))

    #run triangle function
    triangle(adj_mtx_file, inc_mtx_file)

    print("Execution completed.")




