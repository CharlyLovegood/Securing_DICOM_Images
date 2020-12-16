import numpy as np

#Encryption Quality
def EQ(im, enc_im, n):
    arr_fl = np.array(im).flatten()
    addi = np.array(list(range(0,2**n)))
        
    H_L = np.unique(np.concatenate((arr_fl,addi)), return_counts=True)[1]
    
    H_L_e = np.unique(np.concatenate((np.array(enc_im).flatten(),addi)), return_counts=True)[1]
    
    Len = 2**n-1

    assert H_L.shape[0] != Len
    assert H_L_e.shape[0] != Len
    
    return (np.abs(H_L-H_L_e)).sum()/(Len+1)

def Entr(img):
    arr_fl = np.array(img).flatten()

    P_i = np.unique(arr_fl, return_counts=True)[1]/(img.shape[0]*img.shape[1])
    
    return (P_i * np.log2(P_i**(-1))).sum()

def Hist(img,n):
    return plt.hist(np.array(img).flatten(),bins=2**n)

def NPCR(img,cr_img):
    img_a = np.array(img)
    cr_img_a = np.array(cr_img)
    sh = img_a.shape
    M_N = sh[0]*sh[1]
    return ((img_a != cr_img_a).astype(int).sum()/M_N)*100

def UACI(img,cr_img,n):
    img_a = np.array(img)
    cr_img_a = np.array(cr_img)
    sh = img_a.shape
    M_N_255 = sh[0]*sh[1]*(2**n - 1)
    return (np.abs((img_a - cr_img_a)).sum()/M_N_255)*100
