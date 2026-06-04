# Frontend

This folder contains the React frontend for the Smart Incident Risk Predictor.

## Setup

To initialize the React app:

```bash
cd frontend
npx create-react-app . --template cra-template
npm install
npm start
```

## Project Structure

Once initialized:
- `src/pages/` - Page components (Login, Dashboard, Upload, etc.)
- `src/components/` - Reusable components
- `src/services/` - API service layer (axios)
- `src/hooks/` - Custom React hooks
- `src/styles/` - Styling

## API Integration

The frontend communicates with the backend API at `http://localhost:8000/api`.

See `package.json` for required dependencies (Material UI, Chart.js, etc.).
