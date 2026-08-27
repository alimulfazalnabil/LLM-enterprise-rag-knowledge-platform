# Enterprise RAG Knowledge Platform

Enterprise-grade, multi-tenant Retrieval-Augmented Generation (RAG) platform scaffold designed for portfolio, interview, and enterprise demo use.

## Executive Summary
This project implements a secure, modular enterprise knowledge platform with hybrid retrieval (dense + BM25 + RRF + reranking + compression), grounded generation, citation verification, evaluation, and observability.

## Business Problem
Enterprise knowledge is fragmented across PDFs, DOCX, markdown, and operational documents. This platform reduces search and response time while enforcing strict tenant isolation.

## Key Features
- Multi-tenant RBAC and tenant-scoped retrieval contracts
- Hybrid retrieval: vector + BM25 + Reciprocal Rank Fusion
- Cross-encoder reranking interface and compression interface
- Grounded response schema with citations and verification
- Async ingestion pipeline states (PENDING/PROCESSING/COMPLETED/FAILED)
- FastAPI backend, React frontend scaffold, worker scaffold
- Docker Compose local stack (API, worker, Postgres, Redis, Prometheus, Grafana)
- Evaluation and benchmark scaffolding with synthetic AcmeCloud dataset

## Local Quick Start
```bash
git clone <repository>
cd enterprise-rag-knowledge-platform
cp .env.example .env
docker compose up --build
```

Expected URLs:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Notes
- Benchmark metrics are only reported when executed; otherwise: **Benchmark pending execution.**
- This repository contains synthetic enterprise data only.
