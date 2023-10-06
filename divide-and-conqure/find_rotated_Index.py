import math

"""Write a function called findRotatedIndex which accepts a rotated array of sorted numbers and an integer. 
The function should return the index of num in the array. 
If the value is not found, return -1."""

class MyApp:
   def __init__(self):
      pass

   def find_rotated_index(self, my_list, num):
      highIdx = len(my_list)-1
      lowIdx = 0
      pointer = math.floor((highIdx+lowIdx)/2)

      pivot = self.find_pivot(my_list, pointer)
      print(f"pivot completed and pivot: {pivot}")

      while(True):
         if num > my_list[pivot] or num < my_list[pivot+1]: return -1
         if num == my_list[pivot]: return pivot

         elif num > my_list(lowIdx):
            print("search left")
            highIdx = pivot
            pointer = math.floor((highIdx + lowIdx)/2)
         elif num < my_list(highIdx):
            print("search right")
            lowIdx = pivot
            pointer = math.floor((highIdx+lowIdx)/2)

   def find_pivot(self, my_list, pointer):
      lowIdx = 0
      highIdx = len(my_list)-1
      while(True):
         if my_list[pointer] > my_list[pointer + 1] and my_list[pointer] > my_list[pointer-1]:
            return pointer
         elif my_list[pointer] < my_list[lowIdx]:
            print("pivot is left")
            highIdx = pointer
            pointer = math.floor((pointer + lowIdx)/2)
         elif my_list[pointer] > my_list[highIdx]:
            print("pivot is right")
            lowIdx = pointer
            pointer = math.floor((pointer + highIdx)/2)
         else:
            print("something went wrong")
            print(pointer)
            return -1

   def start(self):
      print("this working?")
      self.find_rotated_index([6,7,8,9,10,11,1,2,3,4], 8) #2

      # findRotatedIndex([3,4,1,2],4) # 1
      # findRotatedIndex([6, 7, 8, 9, 1, 2, 3, 4], 8) #2
      # findRotatedIndex([6, 7, 8, 9, 1, 2, 3, 4], 3) # 6
      # findRotatedIndex([37,44,66,102,10,22],14) # -1
      # findRotatedIndex([6, 7, 8, 9, 1, 2, 3, 4], 12) # -1


if __name__ == "__main__":
    app = MyApp()
    app.start()