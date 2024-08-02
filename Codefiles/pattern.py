class pattern:
    n=0;
    def __init__(self,n):
        self.n = n
    
    def makepattern(self):
        for i in range(self.n):
            print(" "*(self.n-i-1) + "* "*(i+1))
        for i in range(self.n):
             print(" "*(i+1) + "* "*(self.n-i-1))
             
p = pattern(int(input("Enter the Number : ")))
p.makepattern()