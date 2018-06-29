def func(n):
    for i in range(1,n):
        if i%9 == 0:
            print (i)
            break
    else: #will enter only if for loop was not broken
        print ('not broken')

func(8)