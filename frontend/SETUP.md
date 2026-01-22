# Frontend setup instructions

Create a `.env` file in the `frontend` directory with the following configuration:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME="IKMS Multi-Agent RAG"
REACT_APP_APP_VERSION="1.0.0"
REACT_APP_ENABLE_CITATIONS=true
REACT_APP_ENABLE_HEATMAP=true
REACT_APP_ENABLE_SOURCE_PANEL=true
REACT_APP_CITATION_HIGHLIGHT_DEBOUNCE=200
REACT_APP_MAX_ANSWER_LENGTH=5000
```

## For Production Builds

Set:
```env
REACT_APP_API_URL=https://your-production-api.com
```

## Build Commands

```bash
# Development
npm start

# Production build
npm run build

# Run tests
npm test
```

## Dependencies

All dependencies are already included in `package.json`. Simply run:

```bash
npm install
```

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── QAInterface.js
│   │   ├── QAInterface.css
│   │   ├── CitationHighlight.js
│   │   ├── CitationHighlight.css
│   │   ├── SourcePanel.js
│   │   ├── SourcePanel.css
│   │   ├── CitationHeatmap.js
│   │   └── CitationHeatmap.css
│   ├── api.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── Dockerfile
```
