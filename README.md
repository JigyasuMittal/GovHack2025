# GovMate AI Assistant

An intelligent AI-powered platform that helps Australians access government services by providing personalized recommendations based on real government datasets and location-specific information.

## Features

- **AI-Powered Responses**: Uses Llama 2 model for intelligent, contextual responses
- **Real Government Data**: Integrates SEIFA 2021 and AGOR 2025 datasets
- **Location-Specific**: Provides suburb-level recommendations across Australia
- **Multi-Service Support**: Covers housing, employment, transport, health, education, and more
- **Step-by-Step Guides**: Generates actionable steps for accessing services
- **Modern Web Interface**: Beautiful, responsive Next.js frontend

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js 14 (React/TypeScript)
- **AI Model**: Llama 2 via Ollama
- **Data**: Real Australian government datasets
- **Deployment**: Docker Compose

## Prerequisites

- Docker and Docker Compose
- Ollama (for Llama 2 model)
- Node.js 18+ (for local development)

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd govmate
```

### 2. Install Ollama and Pull Llama Model
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the Llama 2 model
ollama pull llama2
```

### 3. Start the Application
```bash
# Start all services
docker-compose up --build
```

### 4. Access the Application
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Core Endpoints
- `POST /v1/intent` - Get AI-powered intent analysis
- `GET /v1/services` - Get relevant government services
- `GET /v1/seifa/{location}` - Get SEIFA data for location
- `GET /v1/labour/{state}` - Get employment data for state
- `GET /v1/rulecards` - Get step-by-step guides
- `GET /v1/suburbs-list/{state}` - Get suburbs for state

### Example Usage
```bash
# Get AI analysis for housing assistance
curl -X POST "http://localhost:8000/v1/intent" \
  -H "Content-Type: application/json" \
  -d '{"category":"housing","state":"QLD","suburb":"Brisbane City","user_query":"student accommodation"}'

# Get SEIFA data
curl "http://localhost:8000/v1/seifa/Brisbane%20City"

# Get employment data
curl "http://localhost:8000/v1/labour/QLD"
```

## Data Sources

- **SEIFA 2021**: Socio-Economic Indexes for Areas (population, socio-economic indicators)
- **AGOR 2025**: Australian Government Organisations Register (government services)
- **ABS Labour Force Survey**: Employment and unemployment statistics

## Project Structure

```
govmate/
├── apps/web/                 # Next.js frontend
│   ├── app/                 # App router pages
│   └── Dockerfile
├── services/
│   ├── api/                 # FastAPI backend
│   │   ├── main_final.py   # Main API file
│   │   └── Dockerfile
│   └── worker/              # Background worker
├── datasets/                # Government datasets
├── docker-compose.yml       # Service orchestration
└── README.md
```

## Development

### Local Development Setup
```bash
# Backend
cd services/api
pip install -r requirements.txt
python main_final.py

# Frontend
cd apps/web
npm install
npm run dev
```

### Environment Variables
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_BASE=http://localhost:8000/v1

# Backend (docker-compose.yml)
OLLAMA_HOST=http://ollama:11434
```



### Individual Endpoints
```bash
# AI Intent Analysis
curl -X POST "http://localhost:8000/v1/intent" -H "Content-Type: application/json" -d '{"category":"housing","state":"QLD","suburb":"Brisbane City","user_query":"student accommodation"}'

# SEIFA Data
curl "http://localhost:8000/v1/seifa/Brisbane%20City"

# Employment Data
curl "http://localhost:8000/v1/labour/QLD"

# Services
curl "http://localhost:8000/v1/services?category=housing&state=QLD&suburb=Brisbane%20City&limit=3"

# Rulecards
curl "http://localhost:8000/v1/rulecards?category=housing&suburb=Brisbane%20City"
```




## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue in the repository.
