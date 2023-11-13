class MyApp:
   def __init__(self):
      pass

   def start(self):
      print("this working?")
      myDict = {"a": 1, "b": 2}
      print(myDict.get('c'))
      try:
         print(myDict['c'])
      
      except:
         print("there was an error")


if __name__ == "__main__":
    app = MyApp()
    app.start()