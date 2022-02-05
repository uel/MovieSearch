import os
 
def Merge(directory, output_file):
    output = open(output_file, 'w')
    i = 0
    for filename in os.listdir(directory):
        i+=1
        if filename.endswith('.txt'):
            input = open(os.path.join(directory, filename), 'r')
            contents = input.read()
            output.write(contents)
            input.close()
        if ( i % 1000 == 0 ):
            print(i)
    output.close()

Merge("data/parsed", "data/merged.txt")