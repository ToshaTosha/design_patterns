curl -X 'GET' \
  'http://127.0.0.1:8001/api/reports/formats' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://127.0.0.1:8001/api/reports/nomenclature/CSV' \
  -H 'accept: application/text'

 curl -X 'POST' \
  'http://127.0.0.1:8001/api/filter/measurement' \
  -H 'accept: application/text' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "г",
  "unique_code": "",
  "type": "like"
}'

curl -X 'POST' \
  'http://127.0.0.1:8001/api/transactions' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "start_period": "1900-01-01",
  "end_period": "2024-12-31",
  "warehouse": {
    "name": "name",
    "unique_code": "",
    "type": "equals"
  },
  "nomenclature": {
    "name": "С",
    "unique_code": "",
    "type": "like"
  }
}'

curl -X 'GET' \
  'http://127.0.0.1:8001/api/block_period' \
  -H 'accept: application/json'

 curl -X 'POST' \
  'http://127.0.0.1:8000/api/new_block_period' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "block_period": "2024-12-31"
}'