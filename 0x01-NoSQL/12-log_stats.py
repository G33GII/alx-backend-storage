#!/usr/bin/env python3
"""Prints statistics about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def log_stats():
    """Prints statistics about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count total documents
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count documents by HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count documents with method=GET and path=/status
    status_check = collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check} status check")
