# Abzorithm Frontend (React)

Modern React frontend for Abzorithm coding platform.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd frontend-react
npm install
```

### 2. Start Development Server
```bash
npm start
```

Frontend will run on: **http://localhost:3000**

Backend should be running on: **http://localhost:8000**

## 📁 Project Structure

```
frontend-react/
├── public/
│   └── index.html
├── src/
│   ├── components/      # Reusable components
│   ├── pages/          # Page components
│   │   ├── LoginPage.js
│   │   ├── ProblemsPage.js
│   │   ├── ProblemSolverPage.js
│   │   └── LeaderboardPage.js
│   ├── services/       # API services
│   │   └── api.js
│   ├── hooks/          # Custom hooks
│   ├── styles/         # CSS files
│   │   └── index.css
│   ├── App.js          # Main app component
│   └── index.js        # Entry point
├── package.json
└── README.md
```

## 🛠️ Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests

## 📝 Features

- ✅ Login/Register
- ✅ Problems List
- ✅ Problem Solver
- ✅ Code Editor
- ✅ Leaderboard
- ✅ Responsive Design

## 🔧 Configuration

Backend API URL is configured in `src/services/api.js`:
```javascript
const API_URL = 'http://localhost:8000';
```

## 📦 Dependencies

- React 18
- React Router DOM
- Axios
- CodeMirror (for code editor)

## 🎨 Styling

Uses CSS modules and inline styles.
Main styles in `src/styles/index.css`.

## 🚀 Deployment

```bash
npm run build
```

Build files will be in `build/` directory.
