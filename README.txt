# render:
python display_json.py medical.json
# parse:

 aws textract analyze-document --document '{"S3Object":{"Bucket":"evaltext
ract","Name":"grammerly.png"}}' --feature-types '["TABLES","FORMS"]' --region us

aws textract analyze-document --document '{"S3Object":{"Bucket":"evaltextract","Name":"medical.jpg"}}' --feature-types '["TABLES","FORMS"]' --region us-east-1

  501  cd ~
  502  ls -la
  503  ls cli-ve
  504  ls cli-ve/bin
  505  source cli/bin/activate
  506  source cli-ve/bin/activate
