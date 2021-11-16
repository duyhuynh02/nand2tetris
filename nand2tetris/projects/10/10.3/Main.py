import sys, os, glob
import Parser 


def main():
    if len(sys.argv) == 1:
        print("Please choose file or folder to analyze.")
    else:
        infiles, outfile = change_extention(sys.argv[1])
        # print(infiles)
        # print(outfile)
        for infile in infiles:
            Parser.Parser(infile)


def change_extention(file_or_dir):
    #Put infile to the array for loop each file 
    if os.path.isdir(file_or_dir):
        return glob.glob(file_or_dir + '/*.jack'), file_or_dir + '/'+ file_or_dir + '.xml'
    elif os.path.isfile(file_or_dir) and file_or_dir.endswith('.jack'):
        return [file_or_dir], file_or_dir.replace('.jack', '.xml')
    else:
        print("It's not a JACK file.")


if __name__ == '__main__':
    main()