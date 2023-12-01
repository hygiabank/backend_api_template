# Backend System Setup and Update

## Overview

This README outlines the commands necessary to start and update a backend system composed of a FastAPI application and a PostgreSQL database.

## Prerequisites

**Ensure Docker and Docker Compose are installed on your system.**

## Starting the System

#### Clean Up Previous Containers:

```bash
docker compose down --volumes --remove-orphans
```

#### Start PostgreSQL Database:

```bash
docker compose up -d postgres
```

#### Database Migrations

- Initialize Aerich for Database Migrations:

```bash
aerich init -t app.database.TORTOISE_ORM
```

- Initialize the Database:

```bash
aerich init-db
```

- Create New Migrations (if needed):

```bash
aerich migrate
```

- Apply Migrations:

```bash
aerich upgrade
```

## Running the Backend

```bash
docker compose up -d backend
```

## Visit the Docs for Reference

http://localhost:8000/docs
