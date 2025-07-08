import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext('sample_contract.png', detail=0)

print(result)