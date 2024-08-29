def gcd(a, b):
    if (a == 0):
        return b
    return gcd(b % a, a)

def phi(n):
    result = 1;
    for i in range(2,n):
        if (gcd(i, n) == 1):
            result+=1
    return result

print(f"30   ==> {phi(30)}")
print(f"100   ==> {phi(100)}")
print(f"1225  ==> {phi(1225)}")