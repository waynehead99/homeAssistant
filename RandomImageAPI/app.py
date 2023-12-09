from flask import Flask, send_file
import os
import random
import threading
import time

app = Flask(__name__)

image_folder = '/mnt/nfs'  # NFS mount point
current_image_path = None

def choose_random_image():
    global current_image_path
    while True:
        try:
            images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
            if images:
                random_image_filename = random.choice(images)
                current_image_path = os.path.join(image_folder, random_image_filename)
            time.sleep(60)  # Wait for 1 minute
        except Exception as e:
            print(f"Error choosing image: {e}")

# Start the background thread
threading.Thread(target=choose_random_image, daemon=True).start()

@app.route('/random-image')
def random_image():
    if current_image_path:
        return send_file(current_image_path, mimetype='image/jpeg')
    else:
        return "No image available"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

