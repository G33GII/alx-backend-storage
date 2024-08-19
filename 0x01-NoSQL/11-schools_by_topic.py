#!/usr/bin/env python3
"""
Module to find schools by a specific topic in MongoDB.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic searched.

    Returns:
        List of dictionaries representing the schools that have the specific topic.
    """
    return list(mongo_collection.find({"topics": topic}))
