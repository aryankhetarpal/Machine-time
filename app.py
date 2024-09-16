from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Machine data
machine_data = [
    {'ID': 1, 'Machine Name': 'DROOP & REIN', 'Cutter Diameter (mm)': 170.0, 'Feed Rate (mm/min)': 350.0, 'Speed (rpm)': 270.0, 'Depth of Cut (mm)': 3.0},
    {'ID': 2, 'Machine Name': 'WALDRICH COBURG', 'Cutter Diameter (mm)': 170.0, 'Feed Rate (mm/min)': 350.0, 'Speed (rpm)': 270.0, 'Depth of Cut (mm)': 3.0},
    {'ID': 3, 'Machine Name': 'HEYLIGENSTAEDT', 'Cutter Diameter (mm)': 170.0, 'Feed Rate (mm/min)': 350.0, 'Speed (rpm)': 270.0, 'Depth of Cut (mm)': 3.0},
    {'ID': 4, 'Machine Name': 'ingersel (BHOLE)', 'Cutter Diameter (mm)': 170.0, 'Feed Rate (mm/min)': 350.0, 'Speed (rpm)': 270.0, 'Depth of Cut (mm)': 3.0},
    {'ID': 5, 'Machine Name': 'B W', 'Cutter Diameter (mm)': 80.0, 'Feed Rate (mm/min)': 450.0, 'Speed (rpm)': 735.0, 'Depth of Cut (mm)': 2.0},
    {'ID': 6, 'Machine Name': 'T/C-1000', 'Cutter Diameter (mm)': 80.0, 'Feed Rate (mm/min)': 450.0, 'Speed (rpm)': 735.0, 'Depth of Cut (mm)': 2.0}
]

# Function to calculate machining time
def calculate_machining_time(block_length, block_width, block_height, final_length, final_width, final_height, cutter_diameter, depth_per_pass, feed_rate):
    depth_cut_length = block_length - final_length
    depth_cut_width = block_width - final_width
    depth_cut_height = block_height - final_height

    num_passes_length = math.ceil(block_length / cutter_diameter)
    num_passes_width = math.ceil(block_width / cutter_diameter)
    num_passes_height = math.ceil(block_height / cutter_diameter)

    time_per_length_pass = block_length / feed_rate
    time_per_width_pass = block_width / feed_rate
    time_per_height_pass = block_height / feed_rate

    total_time_for_length = time_per_length_pass * num_passes_length
    total_time_for_width = time_per_width_pass * num_passes_width
    total_time_for_height = time_per_height_pass * num_passes_height

    num_depth_passes_length = math.ceil(depth_cut_length / depth_per_pass)
    num_depth_passes_width = math.ceil(depth_cut_width / depth_per_pass)
    num_depth_passes_height = math.ceil(depth_cut_height / depth_per_pass)

    total_machining_time_length = total_time_for_length * num_depth_passes_length
    total_machining_time_width = total_time_for_width * num_depth_passes_width
    total_machining_time_height = total_time_for_height * num_depth_passes_height

    total_machining_time = total_machining_time_length + total_machining_time_width + total_machining_time_height

    return total_machining_time

# Main route to display the form and calculate results
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from the form
        machine_id = int(request.form['machine'])
        block_length = float(request.form['block_length'])
        block_width = float(request.form['block_width'])
        block_height = float(request.form['block_height'])
        final_length = float(request.form['final_length'])
        final_width = float(request.form['final_width'])
        final_height = float(request.form['final_height'])

        # Find the selected machine
        selected_machine = next((machine for machine in machine_data if machine['ID'] == machine_id), None)

        if selected_machine:
            # Calculate machining time
            machining_time = calculate_machining_time(
                block_length,
                block_width,
                block_height,
                final_length,
                final_width,
                final_height,
                selected_machine['Cutter Diameter (mm)'],
                selected_machine['Depth of Cut (mm)'],
                selected_machine['Feed Rate (mm/min)']
            )

            total_time_hours = machining_time / 60
            return render_template('index.html', machine_data=machine_data, result=machining_time, total_time_hours=total_time_hours)

    # Default GET request
    return render_template('index.html', machine_data=machine_data)

if __name__ == '__main__':
    app.run(debug=True)
