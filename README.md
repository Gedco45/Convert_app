# Converter App

A simple web-based tool to convert **Shapefile/GeoJSON** into **GeoPackage (GPKG)**.  
The project uses **Flask (Python backend)** and a minimal **HTML/JavaScript frontend**.  

---

## Project Structure

```
converter_app/
│
├── app.py                # Flask backend
├── converted_files/       # Saved GPKG outputs (auto-created)
└── templates/
    └── index.html         # Frontend HTML (upload + download)
```

---

## Requirements

Make sure you have **Python 3.9+** and install dependencies:

```bash
pip install flask geopandas
```

Optional (if you want to support raster data in the future):
```bash
pip install rasterio
```

---

## Run the App

1. Open a terminal and navigate into the project folder:

   ```bash
   cd converter_app
   ```

2. Start the Flask backend:

   ```bash
   python app.py
   ```

   You should see:

   ```
   * Running on http://127.0.0.1:5000
   ```

3. Open your browser and go to:  
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## How It Works

1. Select a **Shapefile (.shp)** or **GeoJSON (.geojson)** in the web page.  
2. Click **Upload & Convert**.  
3. Flask backend:
   - Receives the uploaded file.
   - Uses **GeoPandas** to convert it into a `.gpkg`.
   - Saves the file into `converted_files/`.
   - Returns the file to the browser.
4. Your browser downloads the `.gpkg` automatically.  

---

## Output

- Every converted file is saved in:
  ```
  converter_app/converted_files/
  ```
- Each file has a timestamped name, e.g.:
  ```
  output_20250922_153045.gpkg
  ```

---

## Notes

- This is a **development server** (Flask’s built-in).  
  Do **not** use it in production.  
- If running inside **Jupyter Notebook**, use:
  ```python
  app.run(debug=True, use_reloader=False)
  ```
  to avoid `SystemExit` errors.  
- For production deployment, use a WSGI server like **Gunicorn** or **uWSGI**.  

---

## Next Steps (Future Work)

- Add support for **raster data (GeoTIFF → GPKG)** using `rasterio`.  
- Add better frontend UX (progress bar, success/fail messages).  
- Deploy to the cloud (Heroku, Render, Railway).  
