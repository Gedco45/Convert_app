from flask import Flask, request, send_file, render_template
import geopandas as gpd
import rasterio
from rasterio.shutil import copy as raster_copy
from datetime import datetime
import tempfile
import os

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    # Serve the frontend HTML page
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    # 1. Receive uploaded file
    file = request.files["file"]

    # Save input to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_in:
        input_path = tmp_in.name
        file.save(input_path)

    # Create a temp file for output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gpkg") as tmp_out:
        output_path = tmp_out.name

    # Check if file is raster
    filename_lower = file.filename.lower()
    is_raster = filename_lower.endswith(('.tif', '.tiff', '.img', '.png', '.jpg', '.jpeg'))

    # Perform conversion
    if is_raster:
        with rasterio.open(input_path) as src:
            raster_copy(src, output_path, driver="GPKG")
    else:
        gdf = gpd.read_file(input_path)
        gdf.to_file(output_path, driver="GPKG")

    # Send result to user
    return send_file(output_path, as_attachment=True, download_name="converted.gpkg")

if __name__ == "__main__":
    app.run(debug=True)
