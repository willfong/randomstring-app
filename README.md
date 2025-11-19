# RandomString API

A high-performance FastAPI microservice that generates cryptographically secure random strings in various formats. Built with Python 3.12, following TDD principles, and implementing OWASP security best practices.

## Features

- **Interactive Web Interface**: Beautiful dark-themed UI with Tailwind CSS for browser users
- **Multiple String Types**: Alphanumeric, distinguishable characters, passwords (ASCII-printable), URL-safe, and lowercase
- **Customizable Length**: Generate strings from 1 to 128 characters
- **RESTful JSON API**: Modern API design with automatic OpenAPI documentation
- **Security Hardened**: OWASP security headers, rate limiting, input validation
- **Structured Logging**: JSON-formatted logs with correlation IDs for request tracing
- **Health Monitoring**: Built-in health check endpoint for load balancers
- **High Test Coverage**: 92%+ test coverage with unit and integration tests
- **Production Ready**: Multi-stage Docker build, non-root user, minimal attack surface

## Live Demo

🌐 API Documentation: Visit the `/docs` endpoint for interactive Swagger UI
📘 Alternative Documentation: Visit the `/redoc` endpoint for ReDoc UI

## Web Interface

When you visit the application in a web browser, you'll see an interactive web interface where you can:

- **View all 5 string types** simultaneously (alphanumeric, distinguishable, password, URL-safe, lowercase)
- **Customize string length** using an interactive slider (1-128 characters)
- **Generate new strings** on-demand with a single click
- **Copy strings** to clipboard with one click
- **Access API documentation** via a direct link

The web interface features a modern design with:
- Dark theme using Tailwind CSS (Stone background, Amber accents)
- Responsive layout that works on mobile, tablet, and desktop
- Real-time string generation without page reloads
- Clear explanations of each string type's use case

Simply navigate to `http://localhost:8000/` in your browser to access the web interface.

**Note**: The root endpoint `/` intelligently detects if you're using a browser or an API client. Browsers get the web UI, while API clients (curl, httpie, etc.) receive plain text strings for backward compatibility.

## API Endpoints

### Generate Random Strings

**GET** `/api/v1/random?length=32`

Query Parameters:
- `length` (optional): Length of strings to generate (1-128, default: 32)

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/random?length=32"
```

**Example Response:**
```json
{
  "length": 32,
  "strings": {
    "alphanumeric": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "distinguishable": "23456789ABCDEFGHJKMNPQRSTWXYZ2345",
    "password": "!@#$%^&*()_+-=[]{}|;:,.<>?abc123XYZ",
    "urlsafe": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh",
    "lowercase": "abcdefghijklmnopqrstuvwxyzabcdefgh"
  },
  "generated_at": "2025-01-15T12:34:56.789Z"
}
```

### Health Check

**GET** `/health`

Returns service health status, timestamp, and version.

**Example Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-01-15T12:34:56.789Z",
  "version": "0.1.0"
}
```

## String Types Explained

| Type | Character Set | Use Case |
|------|--------------|----------|
| **Alphanumeric** | a-z, A-Z, 0-9 | General purpose random strings |
| **Distinguishable** | Excludes confusing chars (0/O, 1/l/I) | User-facing codes that need to be typed |
| **Password** | ASCII printable (33-126) | Strong passwords with special characters |
| **URL-safe** | a-z, A-Z, 0-9, -, _ | URL parameters, tokens, identifiers |
| **Lowercase** | a-z | Lowercase-only requirements |

## Local Development

### Prerequisites

- **Python 3.12** or higher
- **uv** package manager (recommended) or pip
- **Node.js 22+** and npm (for building Tailwind CSS)
- Git

### Quick Start with uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/yourusername/randomstring-app.git
cd randomstring-app

# Install Python dependencies
uv sync --all-extras

# Install Node dependencies and build CSS
npm install
npm run build:css

# Run tests
uv run pytest

# Start development server
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### CSS Development

The web interface uses Tailwind CSS with a custom build process:

```bash
# Build CSS for production (minified)
npm run build:css

# Watch mode for development (auto-rebuild on changes)
npm run watch:css
```

**Important**: You must build the CSS before running the application, otherwise the web interface will have no styling.

### Alternative: Using pip

```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -e ".[dev]"

# Install Node dependencies and build CSS
npm install
npm run build:css

# Run tests
pytest

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- OpenAPI Spec: http://localhost:8000/openapi.json

### Running Tests

```bash
# Run all tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/

# Run with verbose output
uv run pytest -v

# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code with ruff
uv run ruff format src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking with mypy
uv run mypy src/

# Run all quality checks
uv run ruff check src/ tests/ && uv run mypy src/
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at `http://localhost:5002`

### Building Docker Image Manually

```bash
# Build the image
docker build -t randomstring-app .

# Run the container
docker run -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  -e RATE_LIMIT_ENABLED=true \
  randomstring-app

# Run with custom environment file
docker run -p 8000:8000 --env-file .env randomstring-app
```

### Docker Image Features

- **Multi-stage build** for minimal image size (~100MB)
- **Python 3.12 Alpine** base for security and efficiency
- **Non-root user** (appuser:1001) for security
- **Health check** built-in for container orchestration
- **Tini init system** for proper signal handling
- **Optimized for production** with uvicorn

## Configuration

The application uses environment variables for configuration. See `.env.example` for all available options.

### Key Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | Server port |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FORMAT` | json | Log format (json or text) |
| `RATE_LIMIT_ENABLED` | true | Enable rate limiting |
| `RATE_LIMIT_TIMES` | 100 | Requests allowed per period |
| `RATE_LIMIT_SECONDS` | 60 | Rate limit time window |
| `SECURITY_HEADERS_ENABLED` | true | Enable OWASP security headers |
| `CORS_ENABLED` | true | Enable CORS |
| `DEBUG` | false | Debug mode |

### Creating a Configuration File

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your preferred settings
nano .env
```

## Security Features

This application implements multiple security best practices:

- **OWASP Security Headers**:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
  - Strict-Transport-Security
  - Content-Security-Policy
  - Referrer-Policy
  - Permissions-Policy

- **Rate Limiting**: 100 requests/minute per IP (configurable)
- **Input Validation**: Pydantic-based request validation
- **Cryptographic Security**: Uses Python's `secrets` module for CSPRNG
- **Non-root Container**: Docker runs as user 1001
- **Minimal Attack Surface**: Alpine Linux base, minimal dependencies

## Architecture

```
randomstring-app/
├── src/
│   ├── api/
│   │   └── routes.py          # API endpoint handlers
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── logging.py         # Structured logging setup
│   ├── middleware/
│   │   ├── security.py        # Security headers middleware
│   │   ├── rate_limit.py      # Rate limiting middleware
│   │   └── logging.py         # Request logging middleware
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── static/
│   │   └── css/
│   │       ├── input.css      # Tailwind CSS source
│   │       └── output.css     # Compiled CSS (generated)
│   ├── templates/
│   │   └── index.html         # Web interface template
│   ├── utils/
│   │   └── string_generator.py # String generation logic
│   └── main.py                # FastAPI application
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── conftest.py            # Pytest fixtures
├── tailwind.config.js         # Tailwind CSS configuration
├── package.json               # Node.js dependencies
├── pyproject.toml             # Python project configuration
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Docker Compose config
└── README.md                  # This file
```

## Performance

- **Fast startup**: <1 second
- **Low memory**: ~50MB base memory footprint
- **High throughput**: Handles 1000+ requests/second
- **Async**: Full async/await support with uvicorn

## Contributing

Contributions are welcome! This project follows Test-Driven Development (TDD) principles.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Write tests for your feature (TDD)
4. Implement the feature to pass the tests
5. Ensure all tests pass: `uv run pytest`
6. Ensure code quality: `uv run ruff check src/ tests/`
7. Commit your changes: `git commit -m 'Add amazing feature'`
8. Push to the branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide (enforced by ruff)
- Write comprehensive tests (maintain 80%+ coverage)
- Use type hints (checked by mypy)
- Write clear docstrings for all functions/classes
- Keep functions focused and reasonably sized

## Technology Stack

- **Framework**: FastAPI 0.115+
- **Server**: Uvicorn with uvloop
- **Validation**: Pydantic 2.10+
- **Templating**: Jinja2 3.1+
- **UI**: Tailwind CSS 4.1+ (compiled build)
- **Testing**: pytest, pytest-asyncio, httpx
- **Linting**: Ruff (replaces black, isort, flake8)
- **Type Checking**: mypy
- **Logging**: python-json-logger
- **Rate Limiting**: slowapi
- **Package Manager**: uv (Python), npm (Node)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 0.1.0 (2025-01-15)
- ✨ Complete rewrite in Python with FastAPI
- 🎨 Added interactive web interface with Tailwind CSS (Stone/Amber theme)
- ✅ Implemented TDD approach with 92%+ test coverage
- 🔒 Added OWASP security headers and rate limiting
- 📝 Structured JSON logging with correlation IDs
- 🐳 Multi-stage Docker build with Python 3.12 Alpine
- 📚 Auto-generated OpenAPI documentation
- 🚀 Async/await support for high performance

---

**Note**: This is a refactored version of the original Node.js application, now built with Python, FastAPI, and modern development practices.
