import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize the video capture and hand detector
cap = cv2.VideoCapture(0)  # Use the default camera
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

detector = HandDetector(detectionCon=0.8)  # Initialize hand detector with confidence level

while True:
    success, img = cap.read()  # Read the frame from the camera
    # draw a rectangle

    cv2.rectangle(img, (100, 100), (300, 300), (255, 0, 0), cv2.FILLED)
    if not success:
        break

    # Flip the image horizontally (mirror effect)
    img = cv2.flip(img, 1)

    # Detect hands without drawing default annotations
    hands, _ = detector.findHands(img, draw=False)



    if hands:
        for hand in hands:
            # Access the hand data
            lmList = hand['lmList']  # List of 21 Landmark points
            bbox = hand['bbox']  # Bounding box info x, y, w, h
            handType = hand['type']  # Hand type: Left or Right

            # Correct the hand type after flipping
            if handType == "Left":
                handType = "Right"
            else:
                handType = "Left"

            # Draw the bounding box
            x, y, w, h = bbox
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)  # Purple box

            # Draw all landmarks
            for lm in lmList:
                cv2.circle(img, (lm[0], lm[1]), 5, (0, 255, 0), cv2.FILLED)  # Green circles for landmarks

            # Display hand type
            cv2.putText(img, handType, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)



    # Display the frame
    cv2.imshow("Hand Tracking", img)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
