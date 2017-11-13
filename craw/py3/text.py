arr = {}
arr['a']='ssssss'
arr['b']='kkkk'
arr['c']='ccccc'
if 'c' in arr.keys():
    print('no')
else:
    arr['a'] += 'vvvv' + arr['b']
print(arr['a'])