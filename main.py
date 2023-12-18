#-------------------------------------------------------------------------------
# Imports
import face_recognition
import cv2
import numpy as np

#-------------------------------------------------------------------------------
# Variables & Setup

video_capture = cv2.VideoCapture(0) # Get a reference to the webcam

test_image = face_recognition.load_image_file('res/face_0.jpg')
test_encod = face_recognition.face_encodings(test_image) [0]

known_face_encodings = [
    #test_encod
]
known_face_names = [
    #"Ewerton"
]

counter = 1

#-------------------- -----------------------------------------------------------
while True:
    ret, frame = video_capture.read()

    # rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(frame,10,"hog")
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    if len(known_face_encodings) > 0:
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                
            if name == 'Unknown':
                # Save the unknown face image in the "res/" directory
                filename = f"res/Subject_{counter}.jpg"
                cv2.imwrite(filename, frame[top:bottom, left:right])

                new_image = face_recognition.load_image_file(filename)
                face_locations = face_recognition.face_locations(new_image)

                if face_locations:
                    # Assuming there is at least one face detected
                    new_encod = face_recognition.face_encodings(new_image, face_locations)[0]

                    known_face_encodings.append(new_encod)
                    known_face_names.append(f"Subject_{counter}")
                else:
                    print("No face found in the image.")
                counter += 1
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font,  1.0, (255, 255, 255), 1)
            print(f'{name} was here')
    else:
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"

            if name == 'Unknown':
                # Save the unknown face image in the "res/" directory
                filename = f"res/Subject_{counter}.jpg"
                cv2.imwrite(filename, frame[top:bottom, left:right])

                new_image = face_recognition.load_image_file(filename)
                face_locations = face_recognition.face_locations(new_image)

                if face_locations:
                    # Assuming there is at least one face detected
                    new_encod = face_recognition.face_encodings(new_image, face_locations)[0]

                    known_face_encodings.append(new_encod)
                    known_face_names.append(f"Subject_{counter}")
                else:
                    print("No face found in the image.")
                counter += 1
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(frame, name, (left + 6, bottom - 6), font,  1.0, (255, 255, 255), 1)
            print(f'{name} was here')


    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# # # Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
# # # #-------------------------------------------------------------------------------