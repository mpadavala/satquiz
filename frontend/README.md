# SAT Vocabulary Frontend

React frontend for the SAT Vocabulary Learning App.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

3. Start development server:
```bash
npm run dev
```

## Build

Build for production:
```bash
npm run build
```

The build output will be in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── pages/        # Page components
│   │   ├── LoginPage.jsx
│   │   ├── Dashboard.jsx
│   │   ├── WordDetail.jsx
│   │   ├── Favorites.jsx
│   │   └── UploadPage.jsx
│   ├── components/    # Reusable components
│   │   └── Layout.jsx
│   ├── api/          # API client
│   │   ├── client.js
│   │   ├── auth.js
│   │   └── words.js
│   ├── hooks/        # React hooks
│   │   └── useAuth.js
│   ├── App.jsx       # Main app component
│   └── main.jsx      # Entry point
├── public/           # Static assets
└── package.json
```

## Technologies

- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **React Query** - Data fetching
- **Axios** - HTTP client
- **Tailwind CSS** - Styling

## Environment Variables

- `VITE_API_URL` - Backend API URL

## Docker

Build image:
```bash
docker build -t satquiz-frontend .
```

Run container:
```bash
docker run -p 80:80 satquiz-frontend
```
