# -*- coding: utf-8 -*- 
#author : zhongzhen.cai
#CreateDate : 2015-12-05


from Spider import Spider
from Voter import Voter
import getopt, sys

#-------- 程序入口处 ------------------
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "svh", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-s":
            s = Spider()
            s.run()
        elif o == "-v":
            voter = Voter()
            voter.run()
        else:
            assert False, "unhandled option"

def usage():
    print('-s: Spider, -v: Voter')
        

if __name__ == "__main__":
    main()


    
