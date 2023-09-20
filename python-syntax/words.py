def print_upper_words (words, must_start_with):
   for word in words:
      for letter in must_start_with:
         if word.startswith(letter):
            print(word.upper())

print_upper_words (['words', 'people', 'bananas', 'echo', 'edward'], ['e','b'])