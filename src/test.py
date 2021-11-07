from concurrent.futures import ProcessPoolExecutor
def add_numb(x, y):
    print(x+y)

items = (1,2,)

with ProcessPoolExecutor() as exe:
    exe.map(add_numb, 