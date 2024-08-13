from pymongo import MongoClient

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    """
    # Use aggregation to calculate the average score and sort the students
    pipeline = [
        {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': {'$avg': '$topics.score'}
            }
        },
        {
            '$sort': {'averageScore': -1}
        }
    ]
    
    return list(mongo_collection.aggregate(pipeline))

# Example usage with your main script
if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    # Insert example data
    j_students = [
        { 'name': "John", 'topics': [{'title': "Algo", 'score': 10.3}, {'title': "C", 'score': 6.2}, {'title': "Python", 'score': 12.1}]},
        { 'name': "Bob", 'topics': [{'title': "Algo", 'score': 5.4}, {'title': "C", 'score': 4.9}, {'title': "Python", 'score': 7.9}]},
        { 'name': "Sonia", 'topics': [{'title': "Algo", 'score': 14.8}, {'title': "C", 'score': 8.8}, {'title': "Python", 'score': 15.7}]},
        { 'name': "Amy", 'topics': [{'title': "Algo", 'score': 9.1}, {'title': "C", 'score': 14.2}, {'title': "Python", 'score': 4.8}]},
        { 'name': "Julia", 'topics': [{'title': "Algo", 'score': 10.5}, {'title': "C", 'score': 10.2}, {'title': "Python", 'score': 10.1}]}
    ]
    students_collection.insert_many(j_students)

    # Fetch and print the top students
    top_students_list = top_students(students_collection)
    for student in top_students_list:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'), student.get('averageScore')))
