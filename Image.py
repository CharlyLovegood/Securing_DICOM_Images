import numpy as np

def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    assert h % nrows == 0, "{} rows is not evenly divisble by {}".format(h, nrows)
    assert w % ncols == 0, "{} cols is not evenly divisble by {}".format(w, ncols)
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))

def From_blocks_to_arr_image(image_blocks, Nb,k):
    arr = []

    for i in range(0, Nb, k): # cобираем блоки [16 х 16] по k штук в массивы
        arr.append(image_blocks[i:i+k])

    arr1 = [0] * len(arr)

    for i in range(0, len(arr)): # cобираем блоки [16 х 16] в строки
        for j in range(len(arr[0])):
            if j == 0:
                arr1[i] = arr[i][j]
            else:
                arr1[i] = np.concatenate((arr1[i], arr[i][j]), axis=1)

    for i in range(len(arr1)): # cобираем строки [16 х (16*k)] в картинку
        if i == 0:
            arr2 = arr1[i]
        else:
            arr2 = np.concatenate((arr2, arr1[i]), axis=0)
    
    return arr2
