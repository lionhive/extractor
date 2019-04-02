#Analyzes text in a document stored in an S3 bucket. Display polygon box around text and angled text
import boto3
import io
from io import BytesIO
import sys
import json
import time

document = sys.argv[1]

import math
from PIL import Image, ImageDraw, ImageFont

import demo_rows


def ExtractAndWrite(doc_name):
  # set up s3 object
  # try:
  #   s3_connection = boto3.resource('s3', region_name='us-east-1')
  #   s3_object = s3_connection.Object(bucket_name.encode("ascii"), doc_name.key)
  #   s3_response = s3_object.get()
  #   stream = io.BytesIO(s3_response['Body'].read())
  #   image=Image.open(stream)
  #   image_binary = stream.getvalue()
  #   response = client.analyze_document(
  #       Document={'Bytes': image_binary},
  #       FeatureTypes=["TABLES", "FORMS"])
  # except:
  #   print('skipping', doc_name)
  response = None
  try:
    response = client.analyze_document(
      Document={'S3Object': {'Bucket': bucket_name, 'Name': doc_name}},
      FeatureTypes=["TABLES", "FORMS"])
  except Exception as e:
    print("skipped", doc_name, e)
    return False
  print('*** processed ... ', doc_name)

  # Write to file
  prefix = 'output_json/'
  suffix = '.json'
  filename = prefix + bucket_name + '/' + doc_name + suffix
  try:
    with open(filename, 'w') as outfile:
      json.dump(response, outfile)
  except:
    print('failed to write file', prefix + doc_name.key + suffix, response)
  return True

def Unused():
  #Get the text blocks
  blocks=response['Blocks']
  width, height = image.size
  draw = ImageDraw.Draw(image)
  canvas = Image.new('RGB', (width, height), color = 'white')
  canvas_draw = ImageDraw.Draw(canvas)
  print ('Detected Document Text')

  # Create image showing bounding box/polygon the detected lines/text
  for block in blocks:
    DisplayBlockInformation(block)
    # demo_rows.ExtractBlockRow(block)
    draw=ImageDraw.Draw(image)
    if block['BlockType'] == "KEY_VALUE_SET":
        if block['EntityTypes'][0] == "KEY":
            DrawBoundingBox(draw, block['Geometry']['BoundingBox'],width,height,'red')
        else:
            DrawBoundingBox(draw, block['Geometry']['BoundingBox'],width,height,'green')

    if block['BlockType'] == 'TABLE':
        DrawBoundingBox(draw, block['Geometry']['BoundingBox'],width,height, 'blue')

    if block['BlockType'] == 'CELL':
        DrawBoundingBox(draw, block['Geometry']['BoundingBox'],width,height, 'yellow')

    if block['BlockType'] == 'LINE':
        text = None
        # this line down to draw text over top of the existing doc.
        DrawBoundingBox(draw, block['Geometry']['BoundingBox'],width,height, 'orange', text)
        if 'Text' in block:
            text = block['Text']
        if canvas:
            DrawBoundingBox(canvas_draw, block['Geometry']['BoundingBox'],width,height, 'orange', text)

    # Highlignt individual words
    if block['BlockType'] == 'WORD' and 'Text' in block:
        filter = ['Padilla', 'Leonard', 'Dowda', 'Fields', 'Misty', 'Croslin',
                  'REEVES', 'JOE', 'JOE T', 'THORAX', 'CT THORAX']
        if any(word in block['Text'] for word in filter):
            DrawBoundingBox(draw, block['Geometry']['BoundingBox'],width,height, 'red', None, True)

          #uncomment to draw polygon for all Blocks
          #points=[]
          #for polygon in block['Geometry']['Polygon']:
          #    points.append((width * polygon['X'], height * polygon['Y']))
          #draw.polygon((points), outline='blue')

    image.show()
    canvas.show()

if __name__ == "__main__":
    # Test code - view s3 connect
    ec2 = boto3.client('ec2', region_name='us-east-1')
    bucket_name=sys.argv[1]

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    for object in my_bucket.objects.all():
        print(object)

    s3 = boto3.client('s3')
    response = s3.list_buckets()
    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    # Print out the bucket list
    print("Bucket List: %s" % buckets)
    # end test code

    #Get the document from S3
    s3_connection = boto3.resource('s3', region_name='us-east-1')

    # Create textract client
    client = boto3.client('textract', region_name='us-east-1')
    # Textract all images in this s3 bucket
    # ExtractAndWrite('8500_001.3B.tif')
    exp_delay = 5
    for doc_name in my_bucket.objects.all():
      while ExtractAndWrite(doc_name.key) == False:
        exp_delay += 5
        time.sleep(exp_delay)
      time.sleep(exp_delay)