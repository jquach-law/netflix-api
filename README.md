# Netflix Titles API

A REST API for querying, filtering, and managing a dataset of Netflix titles (movies and TV shows), built with FastAPI and PostgreSQL, containerized with Docker, and deployed on Google Cloud Run with Cloud SQL.

## Features

- CRUD endpoints for Netflix title records (create, search, update, delete)
- Dynamic filtering by any combination of fields (title, director, cast, country, rating, release year, etc.)
- Sorting and pagination on search results
- Aggregate summary endpoints (counts and stats by type, rating, release year, duration, etc.)
- HTTP Basic Auth on all endpoints
- Auto-generated interactive docs via FastAPI's `/docs`
- CI pipeline with GitHub Actions running pytest on push

## Tech Stack

- **API:** Python, FastAPI, Uvicorn
- **Database:** PostgreSQL (Google Cloud SQL), SQLAlchemy
- **Data loading:** pandas (CSV -> SQL ingestion)
- **Deployment:** Docker, Google Cloud Run
- **CI:** GitHub Actions, pytest

## Project Structure

- `netflix_api.py` - FastAPI app and route definitions
- `parsing.py` - loads the raw Netflix titles CSV into the Postgres database
- `check_database.py` - utility script to inspect tables in Cloud SQL
- `test_netflix_api.py` - pytest test suite
- `Dockerfile` / `cloudbuild.yaml` - container build and Cloud Build/Cloud Run deployment config

## Example Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/search` | Search/filter titles with optional query params, sorting, and pagination |
| GET | `/create/{show_id}/{title}` | Add a new title record |
| GET | `/update/{show_id}` | Update fields on an existing title |
| GET | `/delete` | Delete titles matching given filters |
| GET | `/summary/type` | Count of titles by type (Movie/TV Show) |
| GET | `/summary/release_year` | Avg/min/max/count of release years |

## Notes

This was a personal project built to practice REST API design, SQLAlchemy queries, and deploying a containerized service to GCP. It's not actively maintained and has known rough edges (e.g., mutation endpoints using GET instead of POST/PUT/DELETE).
=======
