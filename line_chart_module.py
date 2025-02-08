# # import pandas as pd
# # import matplotlib.pyplot as plt
# # import datetime

# # def load_data(csv_file):
# #     """
# #     Load the CSV file into a pandas DataFrame.
# #     """
# #     df = pd.read_csv(csv_file, index_col='timestamp', parse_dates=True)
# #     return df

# # def filter_latest_data(df, seconds=15):
# #     """
# #     Filter the DataFrame to include only the latest `seconds` of data.
# #     """
# #     now = datetime.datetime.now()
# #     time_threshold = now - datetime.timedelta(seconds=seconds)
# #     return df[df.index >= time_threshold]

# # def plot_line_chart(df, threshold):
# #     """
# #     Plot a line chart with timestamps on the x-axis and the number of persons on the y-axis.
# #     Also, draw a horizontal line for the threshold value.
# #     """
# #     plt.figure(figsize=(10, 4))
    
# #     # Plot each camera's data (assuming columns are cam1, cam2, etc.)
# #     for column in df.columns:
# #         plt.plot(df.index, df[column], label=column)
    
# #     # Draw a horizontal line for the threshold value
# #     plt.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold ({threshold})')
    
# #     # Set labels and title
# #     plt.xlabel('Time')
# #     plt.ylabel('Number of Persons')
# #     plt.title('Number of Persons Over Time (Latest 15 Seconds)')
    
# #     # Add legend
# #     plt.legend()
    
# #     # Return the plot object
# #     return plt
# import pandas as pd
# import matplotlib.pyplot as plt
# import datetime
# import os

# def load_data(csv_file):
#     """
#     Load the CSV file into a pandas DataFrame.
#     Handles cases where the file is empty, missing, or malformed.
#     """
#     try:
#         # Check if the file exists
#         if not os.path.exists(csv_file):
#             # Create an empty DataFrame with the required columns
#             df = pd.DataFrame(columns=['timestamp', 'cam1'])
#             df.set_index('timestamp', inplace=True)
#             return df

#         # Load the CSV file
#         df = pd.read_csv(csv_file)

#         # Check if the 'timestamp' column exists
#         if 'timestamp' not in df.columns:
#             # If 'timestamp' column is missing, create it
#             df['timestamp'] = pd.to_datetime('now')  # Add current timestamp
#             df.set_index('timestamp', inplace=True)
#         else:
#             # Set 'timestamp' as the index and parse it as datetime
#             df['timestamp'] = pd.to_datetime(df['timestamp'])
#             df.set_index('timestamp', inplace=True)

#         return df

#     except Exception as e:
#         # Handle any other errors (e.g., malformed CSV)
#         print(f"Error loading CSV file: {e}")
#         # Return an empty DataFrame with the required columns
#         df = pd.DataFrame(columns=['timestamp', 'cam1'])
#         df.set_index('timestamp', inplace=True)
#         return df


# def filter_latest_data(df, seconds=15):
#     """
#     Filter the DataFrame to include only the latest `seconds` of data.
#     """
#     now = datetime.datetime.now()
#     time_threshold = now - datetime.timedelta(seconds=seconds)
#     return df[df.index >= time_threshold]


# def plot_line_chart(df, threshold):
#     """
#     Plot a line chart with timestamps on the x-axis and the number of persons on the y-axis.
#     Also, draw a horizontal line for the threshold value.
#     Handles cases where the DataFrame is empty.
#     """
#     plt.figure(figsize=(10, 4))

#     # Check if the DataFrame is empty
#     if df.empty:
#         plt.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
#         plt.xlabel('Time')
#         plt.ylabel('Number of Persons')
#         plt.title('Number of Persons Over Time (Latest 15 Seconds)')
#         return plt

#     # Plot each camera's data (assuming columns are cam1, cam2, etc.)
#     for column in df.columns:
#         plt.plot(df.index, df[column], label=column)

#     # Draw a horizontal line for the threshold value
#     plt.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold ({threshold})')

#     # Set labels and title
#     plt.xlabel('Time')
#     plt.ylabel('Number of Persons')
#     plt.title('Number of Persons Over Time (Latest 15 Seconds)')

#     # Add legend
#     plt.legend()

#     # Return the plot object
#     return plt


import pandas as pd
import plotly.graph_objects as go

def generate_graph(file_path, threshold, num_rows=15):
    """
    Generates a Plotly graph for the latest camera data from a CSV file.

    Parameters:
        file_path (str): Path to the CSV file.
        threshold (int): Threshold value for the horizontal line.
        num_rows (int): Number of latest rows to plot (default is 15).

    Returns:
        fig (plotly.graph_objects.Figure): The Plotly figure object.
    """
    try:
        # Load the CSV file
        data = pd.read_csv(file_path)

        # Select the latest `num_rows` rows
        latest_data = data.iloc[-num_rows:]

        # Create a Plotly figure
        fig = go.Figure()

        # Add traces for each camera
        fig.add_trace(go.Scatter(y=latest_data['cam1'], mode='lines', name='Cam1', line=dict(color='blue')))
        fig.add_trace(go.Scatter(y=latest_data['cam2'], mode='lines', name='Cam2', line=dict(color='green')))
        fig.add_trace(go.Scatter(y=latest_data['cam3'], mode='lines', name='Cam3', line=dict(color='red')))
        fig.add_trace(go.Scatter(y=latest_data['cam4'], mode='lines', name='Cam4', line=dict(color='purple')))

        # Add a horizontal threshold line
        # fig.add_hline(y=threshold, line_dash="dash", line_color="black", annotation_text="Threshold")
        fig.add_hline(y=threshold, line_dash="dash", line_color="white", line_width=3,  # Thicker for visibility
              annotation_text="Threshold", annotation_position="top right",
              annotation_font=dict(size=12, color="white", family="Arial"),
              annotation_bgcolor="black")

        # Customize the layout
        fig.update_layout(
            title="Camera Data Over Time",
            xaxis_title="Time",
            yaxis_title="Values",
            showlegend=True,
            xaxis=dict(showticklabels=False),  # Hide x-axis labels
        )

        return fig

    except Exception as e:
        print(f"An error occurred: {e}")
        return None