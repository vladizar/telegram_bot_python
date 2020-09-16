import face_recognition
from famous_persons import FAMOUS_PERSONS

def get_similar_celebrities(num):
    famous_encodings    = []
    similar_celebrities = []
    
    try:
        face          = face_recognition.load_image_file("#ppl/normal/0.jpg")
        face_encoding = face_recognition.face_encodings(face)[0]
    except Exception:
        return None

    for person in FAMOUS_PERSONS:
        famous_encodings.append(person["encoding"])
        person["name"] = person["name"].strip("\n")

    face_distances = face_recognition.face_distance(famous_encodings, face_encoding)

    for distance, (i, person) in zip(face_distances, enumerate(FAMOUS_PERSONS, 1)):
        person["distance"] = distance
        person["image"]    = f"#ppl/famous/picture{i}.jpg"

    for i, person in enumerate(sorted(FAMOUS_PERSONS, key=lambda x: x.get("distance"), reverse=True)):
        if i >= len(FAMOUS_PERSONS) - num:
            similar_celebrities.append(person)

    return similar_celebrities