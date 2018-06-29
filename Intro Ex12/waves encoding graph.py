i_list = [1,3,5,7,9]
n_list = [1.5,3,6,9]
for i in i_list:
    for n in n_list:
        n = float(n)
        t1 = ((2*1.5)/(n+1.5))**i
        t2 = ((2*n/(n+1.5))**i)
        function = 0.8* 1.2 * float(t1) * float(t2)
        print ('n = %s, i = %d, T = %s' %(n, i, function))