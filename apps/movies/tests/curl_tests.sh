echo -----------------------PERSONS-------------------------
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/persons/fc9f27d2-aaee-46e6-b263-40ec8d2dd355' \
  -H 'accept: application/json'
echo
echo ------------------------------------------------
echo
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/persons/search?page_size=20&page_number=1' \
  -H 'accept: application/json'
echo
echo ------------------------------------------------
echo
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/persons/fc9f27d2-aaee-46e6-b263-40ec8d2dd355/films?page_size=20&page_number=1' \
  -H 'accept: application/json'
echo
echo -----------------------GENRES-------------------------
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/genres/' \
  -H 'accept: application/json'
echo
echo ------------------------------------------------
echo
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/genres/237fd1e4-c98e-454e-aa13-8a13fb7547b5' \
  -H 'accept: application/json'
echo -----------------------FILMS-------------------------
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/films/?page_size=20&page_number=1' \
  -H 'accept: application/json'
echo
echo ------------------------------------------------
echo
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/films/cd54d6fb-0aa4-4262-845f-6d32665613a8' \
  -H 'accept: application/json'
