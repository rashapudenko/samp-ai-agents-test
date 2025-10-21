import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import { Vulnerability } from '../../services/api';
import Card from '../ui/Card';
import SeverityBadge from '../ui/SeverityBadge';

//TODO review this interface
export interface MessageProps {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  sources?: Vulnerability[];
}

const Message: React.FC<MessageProps> = ({ role, content, sources }) => {
  return (
    <div className={`message-container ${role}`}>
      <div className="flex items-start">
        <div className="flex-shrink-0 mr-3">
          {role === 'user' ? (
            <div className="bg-primary-600 text-white h-8 w-8 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium">U</span>
            </div>
          ) : (
            <div className="bg-gray-600 text-white h-8 w-8 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium">A</span>
            </div>
          )}
        </div>
        <div className="flex-1">
          <div className="prose dark:prose-invert max-w-none">
            <ReactMarkdown
              components={{
                code: (props: any) => {
                  const { inline, className, children } = props;
                  const match = /language-(.*)/.exec(className || '');
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={vscDarkPlus}
                      language={match[1]}
                      PreTag="div"
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                },
              }}
            >
              {content}
            </ReactMarkdown>
          </div>

          {sources && sources.length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Sources:</h4>
              <div className="space-y-2">
                {sources.map((source) => (
                  <Card key={source.id} className="text-sm">
                    <div className="flex flex-col">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">{source.package}</span>
                        <SeverityBadge severity={source.severity} />
                      </div>
                      <p className="text-gray-700 dark:text-gray-300 line-clamp-2">{source.description}</p>
                      <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 flex justify-between">
                        <span>ID: {source.id}</span>
                        <span>Published: {source.published_date}</span>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Message;
