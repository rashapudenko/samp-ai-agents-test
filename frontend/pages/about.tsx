import React from 'react';
import Layout from '../components/layout/Layout';

const AboutPage: React.FC = () => {
  return (
    <Layout title="About - Security Vulnerabilities Knowledge Base" description="Learn about the Security Vulnerabilities Knowledge Base project">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">About the Project</h1>
          
          <div className="prose dark:prose-invert max-w-none">
            <p>
              The Security Vulnerabilities Knowledge Base is a Retrieval-Augmented Generation (RAG) system
              that provides context-aware responses about security vulnerabilities from package vulnerability
              listings at <a href="https://security.snyk.io/vuln/pip/" className="text-primary-600 dark:text-primary-400">Snyk Security</a>.
            </p>
            
            <h2>How It Works blahblah</h2>
            
            <p>
              The system collects vulnerability data from Snyk's vulnerability database, processes it, and stores
              it in both a traditional database (SQLite) and a vector database (ChromaDB) for semantic search.
              When you ask a question, the system:
            </p>
            
            <ol>
              <li>Converts your question into a vector embedding</li>
              <li>Searches for similar vectors in the database</li>
              <li>Retrieves the most relevant vulnerabilities</li>
              <li>Uses AI to generate a response based on the retrieved context</li>
              <li>Provides you with both the answer and the source vulnerabilities</li>
            </ol>
            
            <h2>Features</h2>
            
            <ul>
              <li>Natural language queries about security vulnerabilities</li>
              <li>Regular updates from Snyk's vulnerability database</li>
              <li>Search functionality for finding specific vulnerabilities</li>
              <li>Detailed information about vulnerability severity, affected versions, and remediation</li>
              <li>Citations and sources for all information provided</li>
            </ul>
            
            <h2>Technology Stack</h2>
            
            <p>This project is built using:</p>
            
            <ul>
              <li><strong>Backend:</strong> Python, FastAPI, SQLite, ChromaDB/FAISS</li>
              <li><strong>AI:</strong> Azure OpenAI API for embeddings and completions</li>
              <li><strong>Frontend:</strong> Next.js, React, Tailwind CSS</li>
              <li><strong>Data Processing:</strong> BeautifulSoup, Pandas</li>
            </ul>
            
            <h2>Limitations</h2>
            
            <p>
              The system is limited to information available in the Snyk vulnerability database for Python packages.
              It may not have information on very recent vulnerabilities (less than a few days old) as the database
              is updated periodically. The AI-generated responses, while based on real data, should always be
              verified against the source vulnerabilities provided.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AboutPage;