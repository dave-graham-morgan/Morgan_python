"""Word Finder: finds random words from a dictionary."""
import random

class WordFinder:
    def __init__(self, path):
      self.path = path
      self.contents = self.open_file().splitlines()

    def open_file(self):
        try:
            with open(self.path, 'r') as file:
                # Read the contents of the file
                file_contents = file.read()
                #count the number of lines read in and return it to user
                num_lines = file_contents.split('\n')
                print(f"there were {len(num_lines)} read in")
                return file_contents
        except FileNotFoundError:
            print("The file was not found.")   
        except PermissionError:
            print("Permission denied to open the file.")
        except Exception as e:
            print("An error occurred:", str(e))

    def random(self):
        random_int = random.randrange(len(self.contents))
        print(self.contents[random_int])

class SpecialWordFinder(WordFinder):
    def __init__(self, path):
        super().__init__(path)
        self.contents = self.clean_lines()

    def clean_lines(self):
        cleaned_lines = []
        for curr_line in self.contents:
            if curr_line.strip() and not curr_line.strip().startswith('#'):
                cleaned_lines.append(curr_line)
        return cleaned_lines

    