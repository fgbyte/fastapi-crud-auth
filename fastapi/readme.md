Instalar deps

```sh
poetry install
```

Ejecutar server
```sh
fastapi dev api/main.py
```

OR (en caso de no funcionar 'fastapi command')

```sh
uvicorn api.main:app --reload
```

