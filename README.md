# Image Filter Processing App — Django + OpenCV

A small interactive web app for the requested image pipeline:

**Image → Grayscale → Noise reduction → Sobel gradient → Canny → Edges**

Choose Gaussian, Median, or Bilateral denoising, an odd kernel size, and the low/high Canny thresholds. The results show the original, grayscale, filtered, gradient, and final edge images.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000. No database setup is needed. Uploads are processed in memory and limited to 10 MB. Kernel size is restricted to odd values from 3 through 31; thresholds must satisfy `0 ≤ low < high ≤ 255`.

## Required combinations

The filter menu lets you run all required pairings independently with the same image and thresholds:

- Gaussian + Canny
- Median + Canny
- Bilateral + Canny

## Pipeline notes

OpenCV decodes the uploaded image, converts it to grayscale, applies the selected smoothing filter, computes a Sobel gradient magnitude for inspection, and applies Canny to the filtered grayscale image. Canny internally computes its gradient and performs non-maximum suppression and hysteresis thresholding; the displayed Sobel image makes the gradient stage visible in the requested pipeline.

This project uses Django's development server and a development-only secret key. Configure production settings before deploying publicly.
