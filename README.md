# Ecommerce Microservices Platform with AI/ML

## 🚀 Project Overview
Designed and implemented a production-ready ecommerce platform with microservices architecture featuring an ML-powered recommendation system. Implemented full CI/CD pipeline, containerization, and monitoring for 5+ services handling user management, products, orders, and real-time recommendations.

## 📁 Project Structure
ecommerce-ml-platform/
├── shared/ # Shared utilities
├── api-gateway/ # API Gateway (FastAPI)
├── user-service/ # User management
├── product-service/ # Product catalog
├── order-service/ # Order processing
├── docker-compose.yml # Container orchestration
└── README.md # This file


## 🛠️ Technologies
- **FastAPI** - Python web framework
- **SQLModel** - SQL database ORM
- **Kafka** - Event streaming
- **Docker** - Containerization
- **PostgreSQL** - Database
- **Circuit Breaker** - Fault tolerance
- **Saga Pattern** - Distributed transactions


## 🚦 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Git

### Installation
```bash
# Clone repository
git clone <your-repo>
cd ecommerce-ml-platform

# Start all services
docker-compose up --build -d

# Check services
docker-compose ps

```

## 🚦 Access Services

API Gateway: http://localhost:8000/docs

User Service: http://localhost:8001/docs

Product Service: http://localhost:8002/docs

Order Service: http://localhost:8003/docs

Kafka UI: http://localhost:8080


## 🗺️ Roadmap

Basic microservices

Database integration

Event-driven architecture (Kafka)

Circuit breaker pattern

Saga pattern

ML Recommendation service

CI/CD pipeline

Kubernetes deployment

Monitoring & logging

Authentication & authorization