import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
from scipy.sparse import coo_matrix
from scipy.sparse import lil_matrix
from time import perf_counter as time
import os, sys, argparse
import scipy.io as sio


#=============================[StrArrayRead Function]=============================#
# read file
def StrArrayRead(filename):
    
    f=open(filename,'r')
    edgelist = []
    with open(filename, 'r') as f:
        for line in f:
            edgelist.append(list(map(float, line.split('\t'))))
    f.close()
    return np.asarray(edgelist)


#=============================[set_zero_rows Function]=============================#
# set the elements of row are zero
def set_zero_rows(sparray, rowNum):
    for row in rowNum:
        sparray.data[sparray.indptr[row]:sparray.indptr[row+1]]=0
    

#=============================[StrArrayWrite Function]=============================#
# write array into file
def StrArrayWrite(nparray, filename):
    with open(filename, "wt", buffering=20*(1024**2)) as f:
        for row in nparray:
            # Convert each element to a string
            data = [str(int(value)) if not isinstance(value, csr_matrix) else str(value) for value in row]
            f.write('\t'.join(data) + '\n')


#=============================[ktruss Function]=============================#

def ktruss (inc_mat_file,k):
    
    ii=StrArrayRead(inc_mat_file) # read file
    
    startTime=time() # time start process
    
    E = csr_matrix((ii[:,2], (ii[:,0]-1, ii[:,1]-1)), shape=(int(max(ii[:,0])), int(max(ii[:,1]))))

    
    readTime=time()
    
    tmp=np.transpose(E)*E   # A=(E^T)E
    sizeX,sizeY=np.shape(tmp)
    
    print ("Time to Read Data:  " + str(readTime-startTime) + "s"+"\n")
    print ("Computing k-truss")
    tmp.setdiag(np.zeros(sizeX),k=0)

    tmp.eliminate_zeros()
    R= E * tmp  #R=EA
    
    s=lil_matrix(((R==2).astype(float)).sum(axis=1))
    xc= (s >=k-2).astype(int)
    
    # The loop executes until there are no more xc==0
    while xc.sum() != np.unique(sp.sparse.find(E)[0]).shape:
        x=sp.sparse.find(xc==0)[0]

        set_zero_rows(E, x)  # set the element of x row are zero
        E=(E>0).astype(int)

        tmp=np.transpose(E)*E # A=(E^T)E
        (tmp).setdiag(np.zeros(np.shape(tmp)[0]),k=0)
        tmp.eliminate_zeros()
        R=E*tmp # R=EA
        s=csr_matrix(((R==2).astype(float)).sum(axis=1))
        xc= (s >=k-2).astype(int)

    ktrussTime=time()
    print ("Time to Compute k=truss:  " + str(ktrussTime-startTime) + "s")
    print("Ktruss matrix:")
    print(E.toarray()) # print ktruss matrix

    StrArrayWrite(E.toarray(), filename) # write ktruss matrix into file

    return E


#=============================[Main Function]=============================#

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", nargs="?", action="store", type=str, default="ktruss_example.tsv")
    args = parser.parse_args()

    inc_mtx_file = args.input_filename

    # Handle the case when the file is error
    if not os.path.isfile(inc_mtx_file):
        print("File doesn't exist: '{}'!".format(inc_mtx_file))
        sys.exit(1)


    filename="ktruss_matrix.txt"    # name file load ktruss matrix

    print("Processing")
    # run ktruss function
    E=ktruss(inc_mtx_file,3)

    print("Execution completed.")



