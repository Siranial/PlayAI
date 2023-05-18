import os

#filepath = input()
#print(os.path.exists(filepath))
#filename = input()

#with open(filepath + filename, 'w') as f:
#    f.write('it works')


    
print('Input file location for storing keylogs')
print('Example: C:/Users/USERNAME/Desktop')
filepath = input()
#Ensure filepath exists
while not os.path.exists(filepath):
        print('Folder not found, please enter existing folder location')
        filepath = input()

with open(filepath + '/keylog.txt', 'w') as f:
    f.write('woggy loggy')