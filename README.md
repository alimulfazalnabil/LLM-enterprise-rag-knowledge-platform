# Enterprise RAG Knowledge Platform

[![CI/CD Quality Gates](https://github.com/enterprise-rag-knowledge-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/enterprise-rag-knowledge-platform/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-005571?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL + pgvector](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Executive Summary

The **Enterprise RAG Knowledge Platform** is a production-grade, multi-tenant Retrieval-Augmented Generation (RAG) system engineered for secure enterprise deployments. It solves the critical institutional knowledge fragmentation problem faced by large organizations where crucial operational guidelines, technical manuals, HR policies, and compliance standards are locked across unstructured repositories (PDF, DOCX, Markdown, TXT).

Unlike basic chatbot demos or naive vector search wrappers, this platform implements a rigorous engineering pipeline combining **Hybrid Retrieval (Dense `pgvector` + Sparse BM25)**, **Reciprocal Rank Fusion (RRF)**, **Cross-Encoder Reranking**, **Contextual Compression**, **Hierarchical Chunking**, **Deterministic Citation Verification**, and **Defense-in-Depth Tenant-Scoped RBAC**.

---

## Business Problem

In enterprise environments, employees waste hundreds of hours annually searching fragmented internal knowledge bases. Traditional keyword search fails when users describe concepts using synonyms, acronyms, or phrasing different from source documents. Conversely, naive vector search suffers from:
* **Poor exact-term matching** for product codes, part numbers, and technical identifiers.
* **Weak handling of domain acronyms** and rare professional terminology.
* **Retrieval noise**, pulling highly semantic but factually irrelevant passages.
* **Hallucination risks**, where LLMs synthesize unverified claims when internal knowledge is missing.

**The Solution**: An enterprise-ready RAG pipeline that guarantees strict tenant isolation, verified factual grounding, and auditability across all knowledge operations.

---

## System Architecture

```mermaid
flowchart TB
    subgraph Client ["Client Layer"]
        SPA[React + TypeScript SPA Dashboard]
    end

    subgraph Gateway ["API Gateway Layer"]
        FastAPI[FastAPI Gateway]
        Auth[JWT & RBAC Middleware]
        Tenant[Tenant Isolation Enforcer]
    end

    subgraph Services ["Core Processing & RAG Services"]
        Ingestion[Asynchronous Ingestion Worker]
        Retrieval[Hybrid Retrieval Engine]
        Generation[Grounded Generation & Citation Svc]
    end

    subgraph Pipeline ["Retrieval & Ranking Pipeline"]
        Parser[MIME & Document Parser]
        Chunker[Hierarchical Chunker]
        VectorStore[(PostgreSQL + pgvector)]
        BM25[BM25 Sparse Index]
        RRF[Reciprocal Rank Fusion]
        Reranker[Cross-Encoder Reranker]
        Compressor[Contextual Compressor]
    end

    subgraph Storage ["Persistence Layer"]
        Postgres[(PostgreSQL Relational DB)]
        Redis[(Redis Cache & Celery Broker)]
        Blob[(Blob Storage / Azure Blob)]
    end

    SPA --> FastAPI --> Auth --> Tenant
    Tenant --> Ingestion & Retrieval & Generation
    
    Ingestion --> Parser --> Chunker --> VectorStore & Postgres
    Ingestion --> Blob
    
    Retrieval --> VectorStore & BM25 --> RRF --> Reranker --> Compressor --> Generation
    Generation --> Postgres
```