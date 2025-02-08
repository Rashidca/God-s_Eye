# import cv2
# from ultralytics import YOLO
# import csv
# import datetime
# import telegram

# # Load YOLO model
# model = YOLO("yolov8n.pt")

# # Open video stream (DroidCam or webcam)
# cap = cv2.VideoCapture(0)  # Change to 0 for default webcam

# # Define the crowd threshold
# THRESHOLD = 2  # Adjust this based on your requirements

# # Telegram Bot Setup
# TELEGRAM_BOT_TOKEN = "7967710076:AAG9L6Fg_ggdQ3rFlU4xOpDGSwCNC3-ozi8"  # Replace with your bot token
# CHAT_ID = "1195861485"  # Replace with your chat ID or group ID

# # Initialize Telegram bot
# bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# def send_alert(captured_value):
#     """Sends an alert message to Telegram if the crowd exceeds the threshold."""
#     alert_message = f"🚨 *Crowd Alert!* 🚨\n\n*Threshold Exceeded!*\n📌 *Threshold:* {THRESHOLD}\n👥 *People Count:* {captured_value}\n📍 *Location:* Camera 1"
    
#     try:
#         bot.send_message(chat_id=CHAT_ID, text=alert_message, parse_mode=telegram.ParseMode.MARKDOWN)
#         print("🚀 Alert sent to Telegram!")
#     except Exception as e:
#         print(f"❌ Error sending alert: {e}")

# # Open (or create) CSV file to append data
# csv_file = 'person_detection_data.csv'

# # Create CSV file and write header if it doesn't exist
# try:
#     with open(csv_file, 'x', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(["Timestamp", "cam1", "cam2", "cam3", "cam4"])  # Write header
# except FileExistsError:
#     pass  # If file exists, continue without writing the header again

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame.")
#         break

#     # Perform object detection
#     results = model(frame)

#     # Count persons and store bounding boxes
#     num_persons = 0
#     for result in results:
#         for box in result.boxes:
#             cls = int(box.cls)  # Class index
#             if model.names[cls] == 'person':  # Only process persons
#                 num_persons += 1
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
#                 confidence = float(box.conf[0])  # Confidence score

#                 # Draw bounding box around detected persons
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, f"Person: {confidence:.2f}", (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     # Get the current timestamp
#     timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     # Print detection info
#     print(f"Timestamp: {timestamp} - Number of persons detected: {num_persons}")

#     # Send Telegram alert if threshold is exceeded
#     if num_persons > THRESHOLD:
#         send_alert(num_persons)

#     # Prepare and log data (Timestamp, cam1, cam2, cam3, cam4)
#     data = [timestamp, num_persons, 0, 0, 0]
#     with open(csv_file, 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(data)

#     # Display the frame with only person detections
#     cv2.imshow("YOLO Person Detection", frame)

#     # Exit on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()




import requests

def send_telegram_notification(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification.")

# Usage
# bot_token = '7653411143:AAEfDXGBPkIECekfdMnfMCyoArUZS2CFxNE'
# chat_id = ['998562781']
# message = 'ALERT!!!'
# send_telegram_notification(bot_token, chat_id, message)