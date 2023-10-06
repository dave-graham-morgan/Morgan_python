
import math

"""Given an array of 1s and 0s which has all 1s first followed by all 0s, 
write a function called countZeroes, which returns the number of zeroes in the array."""

class MyApp:
    def __init__(self):
        pass
 
    def count_zeros(self, myList):
        rightmost_zero = len(myList)-1
        leftmost_one = 0
        curr_index = math.floor((leftmost_one + rightmost_zero) / 2)

        if myList[leftmost_one] == 0:
            return len(myList)
        if myList[rightmost_zero] == 1:
            return 0

        while curr_index != leftmost_one and curr_index != rightmost_zero: 
            if myList[curr_index] == 0:
               rightmost_zero = curr_index
               curr_index = math.floor((curr_index + leftmost_one)/2)
            else:
                leftmost_one = curr_index
                curr_index = math.floor((curr_index + rightmost_zero)/2)
        
        if myList[curr_index] == 1:
            return (len(myList)-1)-curr_index
        else:
            return (len(myList)-1)- curr_index + 1
       
    def start(self):
        print(self.count_zeros([1,1,1,1,0,0])) # 2
        print(self.count_zeros([1,0,0,0,0])) # 4
        print(self.count_zeros([0,0,0])) # 3
        print(self.count_zeros([1,1,1,1])) # 0
        print(self.count_zeros([1,1,1,1,0,0,0,0,0,0,0])) # 7
 
    
if __name__ == "__main__":
    app = MyApp()
    app.start()
