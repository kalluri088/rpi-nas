# Raspberry Pi Hybrid NAS + AWS Sync

A Raspberry Pi based NAS with optional AWS S3 synchronization.

Users can choose which folders stay local and which folders are synchronized to the cloud.

## Features

### NAS

* File Upload & Download
* Folder Management
* Storage Monitoring
* JWT Authentication
* FastAPI Backend
* Web UI
* External HDD Storage

### Cloud Sync

* Folder-level sync selection
* SQLite metadata database
* Recursive folder scanning
* File change detection
* AWS S3 integration
* Frontend sync management

## Tech Stack

* Python
* FastAPI
* SQLite
* boto3
* JavaScript
* Raspberry Pi 4
* AWS S3

## Current Progress

Completed:

* Folder sync management
* Metadata indexing
* File status detection
* AWS S3 upload integration
* Frontend ↔ Backend sync workflow

In Progress:

* Incremental sync engine
* Scheduled synchronization

## Example

```text
Photos      → Sync to AWS
Documents   → Sync to AWS
Movies      → Local Only
Games       → Local Only
```
