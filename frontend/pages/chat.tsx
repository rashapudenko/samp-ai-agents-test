import React from 'react';
import Layout from '../components/layout/Layout';
import ChatBox from '../components/chat/ChatBox';

const ChatPage: React.FC = () => {
  return (
    <Layout title="Chat - Security Vulnerabilities Knowledge Base" description="Chat with our AI assistant about Python package security vulnerabilities">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden h-[80vh]">
          <div className="bg-primary-700 dark:bg-gray-900 px-4 py-3 border-b border-gray-200 dark:border-gray-700">
            <h1 className="text-white font-medium">Security Vulnerabilities Assistant</h1>
          </div>
          <ChatBox />
        </div>
      </div>
    </Layout>
  );
};

export default ChatPage;