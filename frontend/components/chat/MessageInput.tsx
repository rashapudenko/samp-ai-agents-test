import React, { useState, KeyboardEvent } from 'react';
import Button from '../ui/Button';
import { FiSend } from 'react-icons/fi';

interface MessageInputProps {
  onSendMessage: (content: string) => void;
  isLoading?: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, isLoading = false }) => {
  const [content, setContent] = useState('');

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    
    if (content.trim() && !isLoading) {
      onSendMessage(content.trim());
      setContent('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end">
      <div className="relative flex-1 mr-2">
        <textarea
          className="w-full resize-none rounded-md border-gray-300 focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white px-4 py-3 pr-10"
          placeholder="Ask about Python package vulnerabilities..."
          rows={2}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <div className="absolute right-2 bottom-2 text-xs text-gray-500 dark:text-gray-400">
          {isLoading ? 'Processing...' : 'Press Enter to send'}
        </div>
      </div>
      <Button
        type="submit"
        disabled={!content.trim() || isLoading}
        isLoading={isLoading}
        endIcon={<FiSend />}
      >
        Send
      </Button>
    </form>
  );
};

export default MessageInput;