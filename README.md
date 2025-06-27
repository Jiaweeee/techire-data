# TechHire Data Scraper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.0+-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)

> A comprehensive tech job aggregation platform that automatically scrapes, processes, and indexes job postings from major technology companies.

## 🚀 Features

- **Multi-Company Job Scraping**: Automated data collection from 7+ major tech companies including Google, Microsoft, Meta, NVIDIA, ByteDance, TikTok, and Uber
- **Real-time Search**: Elasticsearch-powered job search with advanced filtering capabilities
- **Modern Web Interface**: React-TypeScript frontend with responsive design and Tailwind CSS
- **RESTful API**: FastAPI backend with comprehensive job search and company data endpoints
- **Intelligent Data Processing**: Automated job analysis, information extraction, and indexing
- **Database Management**: SQLAlchemy-based data modeling with Alembic migrations
- **Development Tools**: Integrated database viewer and comprehensive development scripts

## 🏗️ Architecture

```
├── 🕷️  data_scrape/     # Scrapy-based web crawlers
├── 🗄️  data_storage/    # Database models and migrations  
├── ⚙️  data_processor/   # Elasticsearch indexing and job analysis
├── 🌐 backend/          # FastAPI REST API service
├── 💻 frontend/         # React-TypeScript web application
└── 🔍 db-viewer/        # Database management interface
```

## 🛠️ Tech Stack

### Backend
- **Web Scraping**: Scrapy, Twisted
- **API Framework**: FastAPI, Uvicorn
- **Database**: MySQL, SQLAlchemy, Alembic
- **Search Engine**: Elasticsearch 8.x
- **Data Processing**: Python, asyncio

### Frontend
- **Framework**: React 18, TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Routing**: React Router DOM
- **Testing**: Jest

### Infrastructure
- **Database Viewer**: Drizzle Studio
- **Development**: Docker, Node.js

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **MySQL 8.0+**
- **Docker** (for Elasticsearch)
- **Git**

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/techhire-data-scraper.git
cd techhire-data-scraper
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

**Required Environment Variables:**
```bash
DATABASE_URL=mysql://username:password@localhost:3306/techhire
ELASTICSEARCH_HOST=localhost:9200
```

### 3. Database Setup
```bash
# Connect to MySQL and create database
mysql -u root -p
CREATE DATABASE techhire;
EXIT;
```

### 4. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install database viewer dependencies
cd db-viewer && npm install && cd ..
```

### 5. Initialize Services

**Start Elasticsearch:**
```bash
# Create Docker network
docker network create elastic

# Start Elasticsearch
docker run -d \
  --name elasticsearch \
  --net elastic \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:8.12.1
```

**Initialize Database:**
```bash
# Run database migrations
./local_dev.sh db:migrate

# Ingest company data
./local_dev.sh ingest

# Initialize Elasticsearch index
./local_dev.sh es init
```

### 6. Start Development Services

The platform includes a convenient development script for managing all services:

```bash
# Make script executable
chmod +x local_dev.sh

# Start backend API (Terminal 1)
./local_dev.sh api

# Start frontend application (Terminal 2)  
./local_dev.sh ui

# Start database viewer (Terminal 3)
./local_dev.sh db:view
```

## 🌐 Access URLs

- **Frontend Application**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database Viewer**: http://localhost:4983
- **Elasticsearch**: http://localhost:9200

## 📊 Usage

### Running Web Scrapers

**Scrape all companies:**
```bash
./local_dev.sh crawl
```

**Scrape specific company:**
```bash
./local_dev.sh crawl microsoft
```

### Data Processing

**Extract job information:**
```bash
./local_dev.sh process extract
```

**Index jobs to Elasticsearch:**
```bash
./local_dev.sh process index
```

### API Endpoints

The REST API provides comprehensive job search functionality:

- `POST /api/v1/jobs/search` - Advanced job search with filters
- `GET /api/v1/jobs/detail` - Get detailed job information
- `GET /api/v1/companies` - List all supported companies
- `GET /api/v1/companies/detail` - Get company details

### Database Management

**Generate new migration:**
```bash
./local_dev.sh db:migrate "Add new field to jobs table"
```

**Apply existing migrations:**
```bash
./local_dev.sh db:migrate
```

## 🏢 Supported Companies

The platform currently supports job scraping from:

| Company | Industry | Headquarters |
|---------|----------|--------------|
| Microsoft | Software Development | Redmond, WA |
| Google | Software Development | Mountain View, CA |
| Meta | Software Development | Menlo Park, CA |
| NVIDIA | Computer Hardware | Santa Clara, CA |
| ByteDance | Software Development | China |
| TikTok | Entertainment | Los Angeles, CA |
| Uber | Internet Marketplace | San Francisco, CA |

## 🔧 Adding New Companies

1. **Add company configuration:**
   ```bash
   # Edit company data
   nano data_storage/configs/companies.json
   ```

2. **Create spider implementation:**
   ```bash
   # Add new spider file
   nano data_scrape/spiders/new_company.py
   ```

3. **Ingest company data:**
   ```bash
   ./local_dev.sh ingest
   ```

## 🧪 Testing

**Frontend tests:**
```bash
cd frontend && npm test
```

**Backend tests:**
```bash
cd backend && python -m pytest
```

## 📦 Production Deployment

### Docker Deployment
```bash
# Build and start all services
docker-compose up -d
```

### Manual Deployment
```bash
# Backend (Production)
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# Frontend (Build)
cd frontend && npm run build
```

## 🛠️ Development Commands

| Command | Description |
|---------|-------------|
| `./local_dev.sh api` | Start FastAPI backend |
| `./local_dev.sh ui` | Start React frontend |
| `./local_dev.sh db:view` | Launch database viewer |
| `./local_dev.sh crawl` | Run web scrapers |
| `./local_dev.sh process extract` | Start data extraction |
| `./local_dev.sh process index` | Start Elasticsearch indexing |
| `./local_dev.sh es init` | Initialize search index |
| `./local_dev.sh es delete` | Delete search index |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'data_storage'**
```bash
# Install in development mode
pip install -e .
```

**Elasticsearch connection refused**
```bash
# Check Elasticsearch status
docker logs elasticsearch

# Restart Elasticsearch
docker restart elasticsearch
```

**Frontend build errors**
```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📈 Roadmap

- [ ] Support for additional tech companies
- [ ] Machine learning-based job matching
- [ ] Real-time job alerts and notifications
- [ ] Advanced analytics and reporting
- [ ] Mobile application
- [ ] Integration with job boards APIs

## 💬 Support

- **Documentation**: [Wiki](https://github.com/your-username/techhire-data-scraper/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-username/techhire-data-scraper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/techhire-data-scraper/discussions)

## 🙏 Acknowledgments

- [Scrapy](https://scrapy.org/) - Web scraping framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - Frontend framework
- [Elasticsearch](https://www.elastic.co/) - Search and analytics engine
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

**⭐ Star this repository if you find it helpful!**