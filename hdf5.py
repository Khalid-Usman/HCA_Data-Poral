import h5py
import numpy as np

filename = './ica_cord_blood_h5.h5'
f = h5py.File(filename, 'r')

#print('Keys :',f.keys())
a_group_key = list(f.keys())[0]
#print('Group Key = ', a_group_key)

# Get the data
data = list(f[a_group_key])
print('data = ', data)

# Get all genes data
data = f[a_group_key]

#print(type(data))
#print(type(data['genes'].value))
#print(data['barcodes'].value[:10])

data_data = data['data'].value
data_indices = data['indices'].value
data_indptrs = data['indptr'].value

total_rows = data['shape'].value[0]
total_columns = data['shape'].value[1]

# Create a new numpy array
counter = 20    # We want to divide data in 20 different files
new_columns = int(total_columns/counter)
for k in range(counter):
    data_matrix_k = np.zeros(shape=(total_rows,new_columns))
    for j in range(new_columns):
        index_start = data_indptrs[(k*counter)+j]
        index_end = data_indptrs[(k*counter)+j + 1]
        #print('Start = ', index_start, ' index_end = ', index_end, ' index = ', k)
        for i in range(index_end - index_start):
            index = data_indices[i + index_start]
            expValue = data_data[i + index_start]
            #print('Column =', j, ' Row =', index, ' Exp_Value =', expValue)
            # Inser into matrix
            data_matrix_k[index][j] = expValue

    fileName = './genes_cord_{0}.csv' .format(k)
    np.savetxt(fileName,  data_matrix_k, fmt='%i', delimiter=',')

#print('data : ', len(set(data_data)))
#print('indices : ', len(set(data_indices)))
#print('indptr : ', len(set(data_indptr)))