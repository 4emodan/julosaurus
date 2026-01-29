# Photo Pile

A simple photo library service that displays images in a random 'pile on a table' layout.

## Features

- Interactive dragging of photos.
- Bulk file uploads.
- Random rotation and positioning for a 'physical photo' aesthetic.
- Automatic fallback to static mode if the backend is unavailable.

## Deployment

### GitHub Pages

This project is configured to be automatically deployed to GitHub Pages via GitHub Actions.

To enable GitHub Pages:
1. Go to your repository settings on GitHub.
2. Navigate to **Pages** in the sidebar.
3. Under **Build and deployment**, set the **Source** to **GitHub Actions**.

Once configured, any push to the `main` branch will trigger a new deployment.

### Local Development

To run the backend and frontend locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   uvicorn main:app --reload --port 3000
   ```

3. Open `http://localhost:3000` in your browser.

## Testing

Run tests using:
```bash
PYTHONPATH=. pytest tests/test_main.py
```
