# Security Vulnerabilities Knowledge Base - Frontend

This is the frontend application for the Security Vulnerabilities Knowledge Base, a RAG (Retrieval Augmented Generation) application that provides information about Python package vulnerabilities.

## Features

- Chat interface for natural language queries
- Search interface for finding specific vulnerabilities
- Detailed view of vulnerability information
- Dark/light mode support
- Responsive design for all device sizes

## Tech Stack

- **Framework**: [Next.js](https://nextjs.org/)
- **UI Library**: [React](https://reactjs.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Icons**: [React Icons](https://react-icons.github.io/react-icons/)
- **HTTP Client**: [Axios](https://axios-http.com/)
- **Markdown Rendering**: [React Markdown](https://github.com/remarkjs/react-markdown)
- **Syntax Highlighting**: [React Syntax Highlighter](https://github.com/react-syntax-highlighter/react-syntax-highlighter)

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Copy the `.env.local.example` file to `.env.local` and update the configuration:
   ```
   cp .env.local.example .env.local
   ```
4. Start the development server:
   ```
   npm run dev
   ```
5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Environment Variables

- `API_URL`: URL of the backend API (default: `http://localhost:8000`)

## Building for Production

To build the application for production:

```
npm run build
```

To start the production server:

```
npm start
```

## Folder Structure

- `components/`: React components
  - `chat/`: Chat interface components
  - `search/`: Search interface components
  - `ui/`: Reusable UI components
  - `layout/`: Layout components
- `pages/`: Next.js pages
  - `api/`: API routes
  - `index.tsx`: Home page
  - `chat.tsx`: Chat page
  - `search.tsx`: Search page
  - `about.tsx`: About page
- `services/`: API service functions
- `styles/`: Global styles and Tailwind CSS configuration
- `public/`: Static assets

## Pages

- **Home**: Introduction to the project with links to main features
- **Chat**: Interface for asking questions using natural language
- **Search**: Interface for searching vulnerabilities with filters
- **About**: Information about the project and how it works

## API Integration

The frontend connects to the backend API using Axios. The main API service functions are in `services/api.ts`.

For development, the API is expected to run on `http://localhost:8000`, but this can be configured using the `API_URL` environment variable.