Markdown
## Question 1: Understanding Docker Images

**Task:** Run the `python:3.13` image with a bash entrypoint to identify the `pip` version.

**Options:**
- [x] <span style="color:green">**25.3**</span>
- [ ] 24.3.1
- [ ] 24.2.1
- [ ] 23.3.1

**Solution:**

1. Run the container in interactive mode:
   ```bash
   docker run -it --rm --entrypoint bash python:3.13-slim
2. Execute the version check command:
    ```
    pip --version

**Output:**
```text
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

If multiple answers are correct, select any