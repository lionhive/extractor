class RowExtractor():
  key_value_sets = []
  row_sets = []

  # def __init__(self):

  def ExtractBlockRow(self, block):
    print(block['BlockType'], block)
    if block['BlockType'] == 'CELL':
        print('row_sets len', len(RowExtractor.row_sets))
        row_index = block['RowIndex']
        while len(RowExtractor.row_sets) < row_index + 1:
            print(len(RowExtractor.row_sets))
            RowExtractor.row_sets.append([])
            print(len(RowExtractor.row_sets))

        content = ''
        if 'Text' in block:
            text = block['Text']
        print('row_index', row_index, 'content', content)
        RowExtractor.row_sets[row_index] += [content]
    else:
        print('skipping row')

      # if block['BlockType'] == "KEY_VALUE_SET":
      #     key_value_sets[]
  def RowsToCsv(self):
    for row in RowExtractor.row_sets:
        print(','.join(row))
