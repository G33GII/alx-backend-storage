#!/usr/bin/env python3
""" 101-students """

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    
    :param mongo_collection: pymongo collection object
    :return: list of students with their average score
    """
    # Use aggregation pipeline to calculate average score and sort by it
    students = mongo_collection.aggregate([
        {
            "$addFields": {
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        {
            "$sort": { "averageScore": -1 }
        }
    ])

    # Convert the cursor to a list and return it
    return list(students)
