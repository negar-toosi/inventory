## Run the Project

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 3. Create the environment configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` with the required configuration values.

### 4. Start the project

You can run the project using either the Makefile or Docker Compose.

#### Option 1: Using Makefile

```bash
make up-build
```

#### Option 2: Using Docker Compose

```bash
docker compose -f docker-compose.dev.yaml up --build -d
```

The project will start in the background when using Docker Compose.

## Database Design

The database design is based on a layered approach to separating the current state of product inventory from its historical changes.

[Database ERD](https://drive.google.com/file/d/1BveuCDWvc_25eyWPjaXIS9L9FDVtstD5/view?usp=sharing)

