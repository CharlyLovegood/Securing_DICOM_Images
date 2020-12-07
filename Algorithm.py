import numpy as np

def VC(p_i, k_i, n):
    """
    p_i: число для шифрования
    k_i: ключ (задает смещение в алфавите)
    n: число бит для шифрования пикселя картинки
    """
    c_i = (p_i + k_i) % (2**n)
    return c_i


def VD(c_i, k_i, n):
    """
    c_i: зашифрованное число
    k_i: ключ (задает смещение в алфавите)
    n: число бит для шифрования пикселя картинки
    """
    p_i = (c_i - k_i) % (2**n)
    return p_i


def Arnold(matrix):
    """
    matrix[m x m]: матрица, к которой применяется преобразование Арнольда
    """
    m = len(matrix)
    new_matrix = np.zeros((m, m), dtype=int)
    for x in range(m):
        for y in range(m):
            new_matrix[(x + y) % m][(x + 2*y) % m] = matrix[x][y]
    return new_matrix


def key_expansion(k1, k2, k3, k4):
    """
    k1, k2, k3, k4: вектора размерности [16]
    """
    V1, V3 = k1[0] ^ k1[1], k3[0] ^ k3[1]
    V2, V4 = VC(k2[0], k2[1], 8), VC(k4[0], k4[1], 8)

    for i in range(2, 16):
        V1 = V1 ^ k1[i]  # XOR
        V3 = V3 ^ k3[i]  # XOR

        V2 = VC(V2, k2[i], 8)
        V4 = VC(V4, k4[i], 8)
    
    o1 = np.zeros((16, 16), dtype=int)
    o2 = np.zeros((16, 16), dtype=int)
    o = np.zeros((16, 16), dtype=int)
    key_B = np.zeros((16, 16), dtype=int)

    for i in range(16):
        for j in range(16):
            o1[i][j] = VC(k1[i], VC(V2, V1, 8), 8) ^ VC(k2[j], V2 ^ V1, 8)
            o2[i][j] = VC(k3[i], VC(V4, V3, 8), 8) ^ VC(k4[j], V4 ^ V3, 8)
            o[i][j] = o1[i][j] ^ o2[i][j]
    
    arnold_iterations = (o1[1][1] + o1[1][1]) % (2**8)
    
    for i in range(arnold_iterations):
        key_B = Arnold(o)
        
    return key_B


def ciphering_block(B, key_B, n):
    """
    B[16 x 16]: блок для шифрования
    key_B[16 x 16]: ключ шифрования блока
    n: число бит для шифрования пикселя картинки
    """
    B_C = np.zeros((16, 16), dtype=np.uint8)

    for i in range(16):
        for j in range(16):
            B_C[i][j] = VC(B[i][j], key_B[i][j], n)

    return B_C


def deciphering_block(B_C, key_B, n):
    """
    B_C[16 x 16]: зашифрованный блок
    key_B[16 x 16]: ключ расшифрования блока
    n: число бит для шифрования пикселя картинки
    """
    B_D = np.zeros((16, 16), dtype=np.uint8)

    for i in range(16):
        for j in range(16):
            B_D[i][j] = VD(B_C[i][j], key_B[i][j], n)

    return B_D


def s(k1, k2, k3, k4):
    k = np.vstack([k1, k2, k3, k4]).T
    return np.dot(k,k.T)

def key_update(key_B, B_C, B, k1, k2, k3, k4, n):
    """
    B[16 x 16]: предыдущий блок B
    B_C[16 x 16]: зашифрованный блок В
    key_B[16 x 16]: ключ для шифрования предыдущего блока B
    k1, k2, k3, k4: вектора размерности [16]
    n: число бит для шифрования пикселя картинки
    """
    key_B = np.array(key_B)
    B_C = np.array(B_C)
    B_D = np.array(B)
    k1 = np.array(k1)
    k2 = np.array(k2)
    k3 = np.array(k3)
    k4 = np.array(k4)
    
    res = Arnold((key_B + np.outer(B_C.sum(0),B_D.sum(1)) + s(k1, k2, k3, k4)) % (2**n))
    return res


def permute_rows(img, S, n):
    """
    img[n x n]: картинка
    S[n]: блок для перестановки элементов в строках картинки
    n: размерность
    """
    img_pi = np.zeros((n, n), dtype=np.uint8)
    
    for i in range(n):
        arr = []
        for j in range(n):
            arr.append([S[j], img[i][j]])
        
        for j in range(n - 1, 0, -1):
            for k in range(0, j):
                if arr[k][0] > arr[k + 1][0]: 
                    arr[k], arr[k + 1] = arr[k + 1], arr[k]
        
        for j in range(n):
            img_pi[i][j] = arr[j][1]
   
    return img_pi


def permute_columns(img, S, n):
    """
    img[n x n]: картинка
    S[n]: блок для перестановки элементов в строках картинки
    n: размерность
    """
    img_spi = np.zeros((n, n), dtype=np.uint8)
    
    for i in range(n):
        arr = []
        for j in range(n):
            arr.append([S[j], img[j][i]])
        
        for j in range(n - 1, 0, -1):
            for k in range(0, j):
                if arr[k][0] > arr[k + 1][0]: 
                    arr[k], arr[k + 1] = arr[k + 1], arr[k]
        
        for j in range(n):
            img_spi[j][i] = arr[j][1]
        
    return img_spi


def repermute_rows(img, S, n):
    """
    img[n x n]: картинка
    S[n]: блок для перестановки элементов в строках картинки
    n: размерность
    """
    img_pi = np.zeros((n, n), dtype=np.uint8)
    
    for i in range(n):
        arr = []
        for j in range(n):
            arr.append([S[j], j])
        
        for j in range(n - 1, 0, -1):
            for k in range(0, j):
                if arr[k][0] > arr[k + 1][0]: 
                    arr[k], arr[k + 1] = arr[k + 1], arr[k]
        
        for j in range(n):
            img_pi[i][arr[j][1]] = img[i][j]
    
    return img_pi


def repermute_columns(img, S, n):
    """
    img[n x n]: картинка
    S[n]: блок для перестановки элементов в строках картинки
    n: размерность
    """
    img_spi = np.zeros((n, n), dtype=np.uint8)
    
    for i in range(n):
        arr = []
        for j in range(n):
            arr.append([S[j], j])
        
        for j in range(n - 1, 0, -1):
            for k in range(0, j):
                if arr[k][0] > arr[k + 1][0]: 
                    arr[k], arr[k + 1] = arr[k + 1], arr[k]
        
        for j in range(n):
            img_spi[arr[j][1]][i] = img[j][i]
        
    return img_spi