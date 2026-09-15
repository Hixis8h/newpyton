filename = input('Enter a filename: ')
try:
    infile = open(filename,'r')
    contents = infile.read()
    print.close()
except IOError:
    print('An error occurred try to read')
    print('The file',filename)
    
print("End of program")
