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

### 4. Create the environment configuration

Create logs directory:

```bash
mkdir logs
```

### 5. Start the project

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

## Run tests
You can run tests using either the Makefile or Docker Compose.

#### Option 1: Using Makefile

```bash
make pytest
```

#### Option 2: Using Docker Compose

```bash
docker compose -f docker-compose.dev.yaml exec -it backend pytest
```
## Database Design

The database design is based on a layered approach to separating the current state of product inventory from its historical changes.

[Database ERD](https://drive.google.com/file/d/1BveuCDWvc_25eyWPjaXIS9L9FDVtstD5/view?usp=sharing)


## Project Structure

This project follows a **modular Django application structure** that separates business domains, API concerns, shared infrastructure, and environment-specific configuration.

The goal of this structure is to keep the codebase **maintainable, testable, scalable, and easy to navigate** as the project grows.

## Directory Structure

```text
.
├── apps/
│   ├── api/
│   ├── core/
│   └── product/
├── config/
│   ├── django/
│   └── settings/
├── docker/
├── logs/
├── requirements/
├── tests/
├── manage.py
├── Makefile
├── docker-compose.dev.yaml
├── pytest.ini
└── README.md
```

---

## Why This Structure?

The project is organized around **clear responsibilities** rather than putting everything into a single Django application.

This provides several benefits:

* **Separation of concerns** — each part of the project has a clear responsibility.
* **Domain-based organization** — business logic is grouped by domain, such as `product`.
* **Scalability** — new domains can be added without making existing applications unnecessarily complex.
* **Maintainability** — developers can quickly find where functionality belongs.
* **Testability** — business logic can be tested independently from API and infrastructure code.
* **Environment separation** — development and production configuration can evolve independently.
* **Reusable shared components** — common functionality is placed in `core` instead of being duplicated across applications.

---

# `apps/`

The `apps` directory contains the project's Django applications.

Each application represents a specific responsibility or domain.

```text
apps/
├── api/
├── core/
└── product/
```

This approach prevents the project from becoming a single large Django application containing unrelated models, views, serializers, and business logic.

---

## `apps/product/`

The `product` application contains the main product and inventory domain.

```text
product/
├── api/
│   ├── serializers.py
│   └── views.py
├── migrations/
├── tests/
│   └── test_product_services.py
├── admin.py
├── apps.py
├── enums.py
├── models.py
├── schema.py
├── services.py
└── urls.py
```

### `models.py`

Contains the database models belonging to the product domain.

### `services.py`

Contains business logic that should not live directly inside views or serializers.

This is particularly useful because the same business operation can potentially be called from multiple interfaces, not only HTTP endpoints.

Instead of:

```text
View → Business Logic
```

the project follows:

```text
View → Service → Model
```

This keeps API views relatively thin and makes business logic easier to test.

### `enums.py`

Contains domain-specific enumerations and constants.

Keeping these values in one place prevents duplicated string literals throughout the application.

### `api/`

The API layer is separated from the domain itself.

```text
product/api/
├── serializers.py
└── views.py
```

### `tests/`

Tests are kept close to the application they belong to.

```text
product/tests/
└── test_product_services.py
```

In particular, business logic in `services.py` can be tested independently of the HTTP layer.

This encourages testing the actual behavior of the application rather than only testing HTTP endpoints.

---

# `apps/core/`

The `core` application contains functionality shared across multiple applications.

```text
core/
├── custom_response.py
├── exception_handlers.py
├── exceptions.py
└── pagination.py
```

Examples include:

* Custom API responses
* Global exception handling
* Custom exceptions
* Pagination
* Shared Django functionality

The important principle is that `core` should contain **truly shared infrastructure**, not product-specific business logic.

For example:

```text
Product-specific logic → apps/product/
Shared API infrastructure → apps/core/
```

This prevents unrelated domains from becoming coupled to each other.

---

# `apps/api/`

The `api` application provides project-level API configuration.

```text
api/
├── apps.py
└── urls.py
```

It acts as a central entry point for API routing and allows the API layer to grow independently from individual business applications.

For example:

```text
/api/
    /product/
    /users/
    /orders/
```

Each domain can then own its own API implementation.

---

# `config/`

The `config` directory contains Django project configuration rather than business logic.

```text
config/
├── django/
│   ├── base.py
│   ├── dev.py
│   └── prod.py
├── settings/
│   ├── drf.py
│   ├── logging.py
│   └── spectacular.py
├── asgi.py
├── urls.py
└── wsgi.py
```

This separation is important because Django configuration can become large very quickly.

---

## Environment-specific settings

The project uses separate configuration files:

```text
config/django/
├── base.py
├── dev.py
└── prod.py
```

The idea is:

```text
base.py
   │
   ├── dev.py
   │
   └── prod.py
```

### `base.py`

Contains configuration shared across environments.

### `dev.py`

Contains development-specific configuration.

### `prod.py`

Contains production-specific configuration.

This is preferable to putting development and production settings into one large file full of conditional statements.

---

# `config/settings/`

Additional Django/DRF configuration is split into focused modules:

```text
settings/
├── drf.py
├── logging.py
└── spectacular.py
```

For example:

* `drf.py` → Django REST Framework configuration
* `logging.py` → logging configuration
* `spectacular.py` → OpenAPI / API documentation configuration

This keeps `base.py` from becoming a large configuration file.

---

# `requirements/`

Dependencies are separated by purpose:

```text
requirements/
├── base.txt
└── dev.txt
```

`base.txt` contains dependencies required to run the application.

`dev.txt` contains development-specific dependencies such as testing and development tooling.

Conceptually:

```text
base.txt
   ↑
dev.txt
```

This allows production environments to install only what they need while development environments can include additional tools.

---

# `docker/`

Docker-related files are isolated from the application code.

```text
docker/
└── Dockerfile
```

This makes infrastructure configuration easier to find and keeps the project root less cluttered.

---

# `logs/`

Application logs are kept separately:

```text
logs/
└── apps.log
```

Logging configuration itself belongs in:

```text
config/settings/logging.py
```

while generated log files belong in `logs/`.

In production, these files would typically be handled by a centralized logging system rather than stored permanently inside the application container.

---

# `Makefile`

The `Makefile` provides convenient commands for common development operations.

For example:

```bash
make up-build
```

Instead of requiring developers to remember long Docker commands, common operations can have short, consistent commands.

This also provides a simple interface for developers:

```text
make <command>
```

rather than exposing implementation details.

---

# `docker-compose.dev.yaml`

The development Docker environment is defined separately from the application code.

```text
docker-compose.dev.yaml
```

This makes it easy to start the complete development environment consistently across machines.

---

# `pytest.ini`

Pytest configuration is kept at the project root:

```text
pytest.ini
```

This provides a single place for test configuration and ensures that tests are executed consistently.

---

# Overall Architecture

The structure can be viewed as several layers:

```text
                    HTTP Request
                         │
                         ▼
                  ┌─────────────┐
                  │ API / Views │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Serializers │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  Services   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Models    │
                  └──────┬──────┘
                         │
                         ▼
                    Database
```

Shared infrastructure such as exceptions, pagination, responses, logging, and configuration is kept outside the domain-specific business logic.

---

# Why This Structure Works Well

The main advantage is that **each layer has a clear responsibility**.

A developer looking for product business logic knows to look in:

```text
apps/product/services.py
```

A developer looking for product API endpoints knows to look in:

```text
apps/product/api/views.py
```

A developer looking for database models knows to look in:

```text
apps/product/models.py
```

A developer looking for shared exception handling knows to look in:

```text
apps/core/exception_handlers.py
```

And a developer looking for environment configuration knows to look in:

```text
config/django/
```

This predictability becomes increasingly valuable as the project grows.

