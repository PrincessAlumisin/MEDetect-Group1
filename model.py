from ultralytics import YOLO
from werkzeug.utils import secure_filename
from PIL import Image
from matplotlib import cm
import os

def process_image(mode, file, destination_folder):
    #loads model
    model = YOLO(mode)

    #gets file type
    file_type = file.filename.split('.')[-1]

    filename = secure_filename(str(os.urandom(24)) + '.' + file_type)

    file.save(os.path.join(destination_folder, filename))

    #predicts image
    results = model.predict(source=destination_folder + '/' + filename)
    result_image = results[0]
    output_array = result_image.plot()

    output_array = output_array / output_array.max()
    output_array = (output_array * 255).astype('uint8')
    output_array = output_array[:, :, ::-1]
    output_image = Image.fromarray(output_array)

    file_path = os.path.join(destination_folder + '/outputs/', filename)

    output_image.save(file_path)
    return file_path