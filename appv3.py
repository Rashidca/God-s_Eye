
# ------------------------------------


import streamlit as st
import cv2
import datetime
from yolo_detection import YOLODetector
from csv_logger import CSVLogger
from sent_alert import send_telegram_notification
from line_chart_module import generate_graph
import time

# Telegram bot details
bot_token = '7653411143:AAEfDXGBPkIECekfdMnfMCyoArUZS2CFxNE'
chat_id = ['998562781']
# message = 'ALERT!!!'
file_path = 'person_detection_data.csv'
# threshold = 3

# Initialize YOLO detector and CSV logger
detector = YOLODetector("yolov8n.pt")
csv_logger = CSVLogger('person_detection_data.csv')

# Streamlit app title
st.title("Gods’ Eye")
# Placeholder for animation
placeholder = st.empty()
tagline = "See. Predict. Protect."
display_text = ""

for char in tagline:
    display_text += char  # Add one character at a time
    placeholder.write(f"**{display_text}**")  # Update the text dynamically
    time.sleep(0.1)  # Adjust speed as needed

# Sidebar for controls
st.sidebar.header("Controls")

threshold_input = st.sidebar.text_input(
    "Set Threshold",  # Label for the input
    value="3",        # Default value
    key="threshold"   # Unique key for the widget
)

# Convert the input to an integer (with error handling)
try:
    threshold = int(threshold_input)
except ValueError:
    st.sidebar.error("Please enter a valid integer for the threshold.")
    threshold = 3  # Fallback to the default value
threshold2=1.5*threshold


# Button to start the video capture
start_button = st.sidebar.button("Start Video")
stop_button = st.sidebar.button("Stop Video")


# Custom CSS to style all placeholders
st.markdown(
    """
    <style>
    .custom-placeholder {
        max-width: 100px;  /* Adjust the max-width as needed */
        height: 100px;      /* Maintain aspect ratio */
        margin: 5px;      /* Add margin for spacing */
        border: 2px solid #ccc;  /* Add a border */
        padding: 10px;     /* Add padding */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Placeholder for dynamic information (timestamp and number of persons detected)
timestamp_placeholder = st.sidebar.empty()
person_count_placeholder = st.sidebar.empty()
telegram_alert_placeholder1 = st.sidebar.empty()
telegram_alert_placeholder2 = st.sidebar.empty()
# graph_placeholder = st.empty()

col11, col12 = st.columns([1,1])

with col11:
    video_placeholder1 = st.empty()
    header_placeholder1 = st.empty()
    video_placeholder3 = st.empty()
    header_placeholder3 = st.empty()

with col12:
    video_placeholder2 = st.empty()
    header_placeholder2 = st.empty()
    video_placeholder4 = st.empty()
    header_placeholder4 = st.empty()   

# video_placeholder3 = st.empty()
# header_placeholder3 = st.empty()

# video_placeholder4 = st.empty()
# header_placeholder4 = st.empty()

# Variable to track the video capture status
header_placeholder5 = st.empty() 
graph_placeholder = st.empty()
video_started = False

# Create two columns for horizontal layout

# st.write("Cam 1: Real-Time Video Feed")

update_interval = 5  # Update graph every 5 iterations
counter = 0


if start_button and not video_started:
    video_started = True
    # Open the default webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Failed to open the camera. Please check your camera connection.")
        st.stop()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to grab frame.")
            break
        
        num_persons, boxes = detector.detect_persons(frame)

        # Draw bounding boxes around detected persons
        frame = detector.draw_boxes(frame, boxes)

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Log data to CSV
        csv_logger.log_data(timestamp, num_persons)

        # Update the timestamp and number of persons detected every second
        timestamp_placeholder.text(f"Timestamp: {timestamp}")
        person_count_placeholder.text(f"Number of persons detected: {num_persons}")

        # Convert the frame to RGB for Streamlit display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Send alert if the number of persons exceeds the threshold
        if num_persons > threshold:
            message = f"ALERT!!! Number of people entered more than {num_persons}"
            send_telegram_notification(bot_token, chat_id, message)
            telegram_alert_placeholder1.success(f"Telegram Alert Sent: {message}")
        if num_persons > threshold2:
            message = "informed nearest firestation and ambulance"
            send_telegram_notification(bot_token, chat_id, message)
            telegram_alert_placeholder2.success(f"Telegram Alert Sent: {message}")


        col1, col2 = st.columns([1,1])

        # with col1:
        header_placeholder1.caption("Cam 1: Real-Time Video Feed")
        video_placeholder1.image(frame_rgb, channels="RGB", use_container_width=False,width=400)
        
        # with col2:
        header_placeholder2.caption("Cam 2: camera disconnected")
        local_image_path = "Screenshot 2025-02-07 012726.jpg"  # Replace with the actual path to your local image
        video_placeholder2.image(local_image_path, use_container_width=False,width=400)
        header_placeholder3.caption("Cam 3: camera disconnected ")
        video_placeholder3.image(local_image_path, use_container_width=False,width=400)
        header_placeholder4.caption("Cam 4: camera disconnected")
        video_placeholder4.image(local_image_path, use_container_width=False,width=400)
       
        # Generate line chart
        header_placeholder5.subheader("No of people in each cam")
        counter += 1
        if counter % update_interval == 0:
            fig = generate_graph(file_path, threshold)
            if fig:
                graph_placeholder.plotly_chart(fig, use_container_width=True, key=f"plotly_chart_{counter}")

        

        # Exit loop if the 'Stop' button is pressed
        if stop_button:
                st.sidebar.write("Stopping video feed...")
                break
#         # Release resources after stopping
    cap.release()
    cv2.destroyAllWindows()
    video_started = False

elif not start_button:
    st.write("Click the 'Start Video' button to begin detection.")
