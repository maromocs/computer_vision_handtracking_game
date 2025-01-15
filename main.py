import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize the video capture and hand detector
cap = cv2.VideoCapture(0)  # Use the default camera
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height
colorR=(255,0,0)
if not cap.isOpened():
    print("Error opening video stream check camera connection")

detector = HandDetector(detectionCon=0.8)  # Initialize hand detector with confidence level
try:
        while True:
            success, img = cap.read()  # Read the frame from the camera

            # draw a rectangle
            # Create an overlay for transparency
            overlay = img.copy()
            cv2.rectangle(overlay, (100, 100), (300, 300), colorR, cv2.FILLED)

            # Add transparency (alpha = 0.5 for 50% transparency)
            alpha = 0.3
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
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
                    handType = "Right" if handType == "Left" else "Left"

                    # Adjust landmark coordinates for flipped frame (flip the  lm coordinates as well)
                    adjusted_lmList = [(1280 - lm[0], lm[1]) for lm in lmList]

                    # Draw the bounding box
                    x, y, w, h = bbox
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)  # Purple box

                    # Draw all landmarks
                    for lm in lmList:
                        cv2.circle(img, (lm[0], lm[1]), 5, (0, 255, 0), cv2.FILLED)  # Green circles for landmarks

                    # Display hand type
                    cv2.putText(img, handType, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

                    if adjusted_lmList:
                        cursor=adjusted_lmList[8]
                        if 100<cursor[0]<300 and 100<cursor[1]<300:
                            colorR = (0, 255, 0)
                        else:
                            colorR = (255, 0, 0)

            # Display the frame
            cv2.imshow("Hand Tracking", img)

            # Exit the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
except Exception as e:
    print(f"An error occurred: {e}")
# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
