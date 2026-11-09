
def a_not_b(ls_a, ls_b):
    if not(isinstance(ls_a,list) and isinstance(ls_b, list)):
        raise TypeError("Both arguments must be lists.")
        
    res = []
    for i in ls_a:
        if i not in ls_b:
            res.append(i)

    return res

if __name__=="__main__":

    a = [0,1,2,3,5,5,3,5,6]
    b = [9,4,7,2,4,6]
    print(a_not_b(a,b))
    #for error checking 
    #print(a_not_b(2,2))
