# Random String Generator

A simple web service that generates random strings in various formats. Live at: https://randomstring.app

## Features

- **Multiple string types**: Alphanumeric, distinguishable characters, ASCII-printable, URL-safe, and lowercase
- **Customizable length**: Specify string length via URL parameter (max 128 characters)
- **RESTful API**: Simple HTTP endpoints for easy integration
- **Health check endpoint**: Built-in ALB health check support

## API Usage

### Generate random strings (default length: 32)
```bash
curl https://randomstring.app
```

### Generate custom length strings
```bash
curl https://randomstring.app/5
```

**Example Response:**
```
Random Stuff:
onETjSjzANNie8UFlWcmNleuAgqgo2dI

Easy to read:
28P04RKE1KM55M402TYPWUCM8KTU2PX2

Passwords:
)jRjA-^o>_h9enj^9A'd>M%Zl6~`P_"I

URL-safe:
AbC123_-XyZ789

Lower-case:
abcdefghijklmnop
```

## Local Development

### Prerequisites
- Node.js 22.0.0 or higher
- npm

### Installation
```bash
git clone https://github.com/willfong/randomstring-app.git
cd randomstring-app
npm install
```

### Running the application
```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm start
```

The server will start on `http://localhost:3000` by default.

## Docker

### Pre-built Image
The application is available as a pre-built ARM64 image on Docker Hub:
```bash
# Pull and run the latest image
docker run -p 3000:3000 wfong/randomstring-app:latest
```

### Build and run with Docker
```bash
# Build the image locally
docker build -t randomstring-app .

# Build for ARM64 architecture
docker buildx build --platform linux/arm64 -t randomstring-app .

# Run the container
docker run -p 3000:3000 randomstring-app
```

### Docker Image Features
- **Multi-stage build** for minimal image size
- **ARM64 optimized** for modern architectures
- **Security hardened** with non-root user
- **Memory optimized** with 64MB heap limit and aggressive GC
- **Alpine Linux** base for reduced attack surface

### Using Docker Compose
Create a `docker-compose.yml` file:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - PORT=3000
```

Then run:
```bash
docker-compose up
```

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Port number for the server to listen on |

## Health Check

The application includes a health check endpoint for load balancers:
```bash
curl http://localhost:3000/alb-health-check
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
