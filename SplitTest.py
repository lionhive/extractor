# Splits text into an array
# SplitText('b', 'a b c') => ('a', 'b', 'c')
def SplitText(split_by, text):
    split_text = text.split(split_by)
    if len(split_text) > 1:
      split_text.insert(1, split_by)
    return split_text

split_by = 'George Clooney'
text = 'The suspect George Clooney is on the loose.'

split = SplitText(split_by, text)
print(split)

split = SplitText(split_by, 'The Suspect Mary is on the loose.')
print(split)