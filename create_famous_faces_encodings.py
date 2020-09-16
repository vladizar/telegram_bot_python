print("Starting the programm...")
import face_recognition

FAMOUS_DIRECTORY = "#ppl/famous"

famous_persons = []

print("Calculating famous faces encodings and reading their names...")
with open(f"{FAMOUS_DIRECTORY}/names.txt", "r") as names:
    for i, name in enumerate(names, 1):
        try:
            face_image = face_recognition.load_image_file(f"{FAMOUS_DIRECTORY}/picture{i}.jpg")
            famous_persons.append(dict(name=name.strip("/n"), encoding=face_recognition.face_encodings(face_image)[0]))
        except Exception:
            print(f"\nError with image #{i}. I'll skip it! :)")

    print(f"Persons processed: {len(famous_persons)}")

print("Writing data to file...")
with open("famous_persons.py", "w") as file:
    file.write("from numpy import array\n")
    file.write(f"FAMOUS_PERSONS = {famous_persons}")