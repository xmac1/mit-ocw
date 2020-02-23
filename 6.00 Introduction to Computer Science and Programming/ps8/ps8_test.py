def f():
    l = []
    m = 1
    def c():
        nonlocal m
        m += 1
        print m+1
    c()


f()