import sys

def main():
    if len(sys.argv) > 2:
    	print("aa: {}".format(sys.argv[1]))
    	print("bb: {}".format(sys.argv[2]))
    if len(sys.argv) == 4:
    	print("cc: {}".format(sys.argv[3]))

if __name__ == '__main__':
	main()