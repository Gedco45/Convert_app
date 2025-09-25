from flask import Flask, request, send_file, render_template
import geopandas as gpd
import os
import rasterio
from rasterio.shutil import copy as raster_copy
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# Make sure converted_files directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "converted_files")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    # Serve the frontend HTML page
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    # 1. Receive uploaded file from frontend
    file = request.files["file"]
    input_path = f"/tmp/{file.filename}"

    # Check for raster extensions
    filename_lower = file.filename.lower()
    is_raster = filename_lower.endswith(('.tif', '.tiff', '.img', '.png', '.jpg', '.jpeg'))

    # 2. Save the uploaded file temporarily
    file.save(input_path)

    # 3. Define output filename (use timestamp to avoid overwriting)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"output_{timestamp}.gpkg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    if is_raster:
        # Raster conversion into GeoPackage
        with rasterio.open(input_path) as src:
            # Write raster into a GeoPackage
            raster_copy(src, output_path, driver="GPKG")
    else:
        # Vector conversion into GeoPackage
        gdf = gpd.read_file(input_path)
        gdf.to_file(output_path, driver="GPKG")

    # 5. Return the converted file back to frontend for download
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    # Run Flask server in development mode
    app.run(debug=True)
