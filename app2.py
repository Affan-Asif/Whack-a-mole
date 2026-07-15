# import cv2
# import random
# import time
# import mediapipe as mp
# import numpy as np

# # Load images
# bottom_img = cv2.imread("bottom.png", cv2.IMREAD_UNCHANGED)
# mole_img = cv2.imread("mole.png", cv2.IMREAD_UNCHANGED)
# wood_img = cv2.imread("wood.png", cv2.IMREAD_UNCHANGED)

# # Resize images
# bottom_img = cv2.resize(bottom_img, (1280, 171), interpolation=cv2.INTER_AREA)
# mole_img = cv2.resize(mole_img, (120, 120), interpolation=cv2.INTER_AREA)
# wood_img = cv2.resize(wood_img, (120, 120), interpolation=cv2.INTER_AREA)

# # Pose setup
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose(min_detection_confidence=0.5)
# mp_draw = mp.solutions.drawing_utils

# # Webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# # Overlay helper
# def overlay_transparent(background, overlay, x, y):
#     h, w = overlay.shape[:2]
#     if x + w > background.shape[1] or y + h > background.shape[0]:
#         return background
#     alpha = overlay[:, :, 3] / 255.0
#     for c in range(3):
#         background[y:y+h, x:x+w, c] = (1 - alpha) * background[y:y+h, x:x+w, c] + alpha * overlay[:, :, c]
#     return background

# # Game reset function
# def reset_game():
#     return {
#         "score": 0,
#         "start_time": time.time(),
#         "duration": 30,
#         "last_spawn_time": 0,
#         "current_obj": {"type": "mole", "pos": (0, 0), "shown": False}
#     }

# # Initial game state
# game = reset_game()
# hole_positions = [(i * 256 + 50, 500) for i in range(5)]

# # Main loop
# while True:
#     success, frame = cap.read()
#     if not success:
#         break

#     frame = cv2.flip(frame, 1)
#     img = frame.copy()

#     # Pose detection
#     rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = pose.process(rgb)
#     if results.pose_landmarks:
#         mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
#                                mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

#     # Draw bottom.png
#     img = overlay_transparent(img, bottom_img, 0, 720 - bottom_img.shape[0])

#     # Timer logic
#     elapsed = int(time.time() - game["start_time"])
#     remaining = max(0, game["duration"] - elapsed)

#     # Spawn object
#     if time.time() - game["last_spawn_time"] > 1 and remaining > 0:
#         game["current_obj"]["type"] = random.choice(["mole", "wood"])
#         game["current_obj"]["pos"] = random.choice(hole_positions)
#         game["current_obj"]["shown"] = True
#         game["last_spawn_time"] = time.time()

#     # Draw and check collision
#     if game["current_obj"]["shown"] and remaining > 0:
#         obj_img = mole_img if game["current_obj"]["type"] == "mole" else wood_img
#         img = overlay_transparent(img, obj_img, *game["current_obj"]["pos"])

#         if results.pose_landmarks:
#             h, w, _ = img.shape
#             for id in [15, 16]:  # wrists
#                 x = int(results.pose_landmarks.landmark[id].x * w)
#                 y = int(results.pose_landmarks.landmark[id].y * h)
#                 cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)

#                 ox, oy = game["current_obj"]["pos"]
#                 if ox < x < ox + 120 and oy < y < oy + 120:
#                     if game["current_obj"]["type"] == "mole":
#                         game["score"] += 1
#                     else:
#                         game["score"] -= 5
#                     game["current_obj"]["shown"] = False

#     # Display score and time
#     if remaining > 0:
#         cv2.putText(img, f"SCORE: {game['score']} | TIME: {remaining}", (20, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)
#     else:
#         cv2.putText(img, f"FINAL SCORE: {game['score']}", (350, 360),
#                     cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6)
#         cv2.putText(img, "Press R to restart or X to exit", (300, 420),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

#     # Quit or Restart
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('x'):
#         break
#     elif key == ord('r') and remaining == 0:
#         game = reset_game()

#     cv2.imshow("Whack-a-Mole Pose Edition", img)

# cap.release()
# cv2.destroyAllWindows()



import cv2
import random
import time
import mediapipe as mp
import numpy as np

# Load images
bottom_img = cv2.imread("bottom.png", cv2.IMREAD_UNCHANGED)
mole_img = cv2.imread("mole.png", cv2.IMREAD_UNCHANGED)
wood_img = cv2.imread("wood.png", cv2.IMREAD_UNCHANGED)

# Resize images
bottom_img = cv2.resize(bottom_img, (1280, 171), interpolation=cv2.INTER_AREA)
mole_img = cv2.resize(mole_img, (120, 120), interpolation=cv2.INTER_AREA)
wood_img = cv2.resize(wood_img, (120, 120), interpolation=cv2.INTER_AREA)

# Pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Overlay helper
def overlay_transparent(background, overlay, x, y):
    h, w = overlay.shape[:2]
    if x + w > background.shape[1] or y + h > background.shape[0]:
        return background
    alpha = overlay[:, :, 3] / 255.0
    for c in range(3):
        background[y:y+h, x:x+w, c] = (1 - alpha) * background[y:y+h, x:x+w, c] + alpha * overlay[:, :, c]
    return background

# Game reset function
def reset_game():
    return {
        "score": 0,
        "start_time": time.time(),
        "duration": 30,
        "last_spawn_time": 0,
        "spawn_interval": 1,  # faster spawning
        "current_obj": {"type": "mole", "pos": (0, 0), "shown": False}
    }

# Initial game state
game = reset_game()
hole_positions = [(i * 256 + 50, 500) for i in range(5)]

# Main loop
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    img = frame.copy()

    # Pose detection
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)
    if results.pose_landmarks:
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                               mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
                               mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

    # Draw bottom holes
    img = overlay_transparent(img, bottom_img, 0, 720 - bottom_img.shape[0])

    # Timer
    elapsed = int(time.time() - game["start_time"])
    remaining = max(0, game["duration"] - elapsed)

    # Spawn mole/wood
    if time.time() - game["last_spawn_time"] > game["spawn_interval"] and remaining > 0:
        game["current_obj"]["type"] = random.choice(["mole", "wood"])
        game["current_obj"]["pos"] = random.choice(hole_positions)
        game["current_obj"]["shown"] = True
        game["last_spawn_time"] = time.time()

    # Draw object and check collision
    if game["current_obj"]["shown"] and remaining > 0:
        obj_img = mole_img if game["current_obj"]["type"] == "mole" else wood_img
        img = overlay_transparent(img, obj_img, *game["current_obj"]["pos"])

        if results.pose_landmarks:
            h, w, _ = img.shape
            for id in [15, 16]:  # wrists
                x = int(results.pose_landmarks.landmark[id].x * w)
                y = int(results.pose_landmarks.landmark[id].y * h)
                cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)

                ox, oy = game["current_obj"]["pos"]
                if ox < x < ox + 120 and oy < y < oy + 120:
                    if game["current_obj"]["type"] == "mole":
                        game["score"] += 1
                    else:
                        game["score"] -= 5
                    game["current_obj"]["shown"] = False

    # Display score and timer
    if remaining > 0:
        cv2.putText(img, f"SCORE: {game['score']} | TIME: {remaining}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)
    else:
        cv2.putText(img, f"FINAL SCORE: {game['score']}", (350, 360),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6)
        cv2.putText(img, "Press R to restart or X to exit", (300, 420),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    # Handle key input
    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        break
    elif key == ord('r') and remaining == 0:
        game = reset_game()

    cv2.imshow("Whack-a-Mole Pose Edition", img)

cap.release()
cv2.destroyAllWindows()
