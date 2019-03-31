import json
import sys
import demo_rows

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
#args = len(sys.argv) == 0

if len(sys.argv) < 2:
  print("missing argument filename")
#  exit
rowExtractor = demo_rows.RowExtractor()
with open(sys.argv[1]) as json_file:
    data = json.load(json_file)
    for block in data['Blocks']:
         # Create image showing bounding box/polygon the detected lines/text
        rowExtractor.ExtractBlockRow(block)

      # if 'Text' in block:
      #   t = p['Text']
      #   if t:
      #     print(t)
      #   else:
      #     print('skipping')
rowExtractor.RowsToCsv()