# College Lost & Found API

A beginner-friendly REST API for college students to report lost or found items, update their status, and search reports. Item data is stored persistently in a local SQLite database.

## Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn

## Installation

Open a terminal in the project folder (or clone/open the project first), then create and activate a virtual environment on Windows:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once, or activate from Command Prompt with `.venv\Scripts\activate.bat`.

## Run the API

```powershell
uvicorn main:app --reload
```

The SQLite database is created as `lost_found.db` when the application starts.

## Swagger UI

Open the interactive API documentation at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Available Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/items` | Create a lost/found item report. |
| GET | `/items` | Return all item reports. |
| GET | `/items/{item_id}` | Return one report by its ID. |
| PUT | `/items/{item_id}` | Update an existing report. |
| DELETE | `/items/{item_id}` | Delete an existing report. |
| GET | `/items/status/{status}` | Return reports with status `Lost`, `Found`, or `Returned`. |
| GET | `/items/category/{category}` | Return reports in a category, or an empty list if none match. |

## Validation and Error Handling

- Empty or whitespace-only titles and descriptions are rejected with HTTP 422.
- Empty required text fields are rejected with HTTP 422.
- Status must be `Lost`, `Found`, or `Returned`; other values are rejected with HTTP 422.
- Missing required request fields are rejected with HTTP 422.
- Missing item IDs return HTTP 404 with `{ "detail": "Item not found" }`.
- An update with no fields returns HTTP 400.
