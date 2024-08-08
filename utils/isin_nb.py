import numpy as np

def in1d_vec_nb(matrix, index_to_remove):
  #matrix and index_to_remove have to be numpy arrays
  #if index_to_remove is a list with different dtypes this 
  #function will fail

  out=np.empty(matrix.shape[0],dtype=nb.boolean)
  index_to_remove_set=set(index_to_remove)

  for i in nb.prange(matrix.shape[0]):
    if matrix[i] in index_to_remove_set:
      out[i]=False
    else:
      out[i]=True

  return out

def in1d_scal_nb(matrix, index_to_remove):
  #matrix and index_to_remove have to be numpy arrays
  #if index_to_remove is a list with different dtypes this 
  #function will fail

  out=np.empty(matrix.shape[0],dtype=nb.boolean)
  for i in nb.prange(matrix.shape[0]):
    if (matrix[i] == index_to_remove):
      out[i]=False
    else:
      out[i]=True

  return out


def isin_nb(matrix_in, index_to_remove):
  #both matrix_in and index_to_remove have to be a np.ndarray
  #even if index_to_remove is actually a single number
  shape=matrix_in.shape
  if index_to_remove.shape==():
    res=in1d_scal_nb(matrix_in.reshape(-1),index_to_remove.take(0))
  else:
    res=in1d_vec_nb(matrix_in.reshape(-1),index_to_remove)

  return res.reshape(shape)