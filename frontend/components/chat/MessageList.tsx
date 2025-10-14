import React from 'react';
import Message, { MessageProps } from './Message';

interface MessageListProps {
  messages: MessageProps[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <div key={message.id}>
          <Message
            id={message.id}
            role={message.role}
            content={message.content}
            sources={message.sources}
          />
        </div>
      ))}
    </div>
  );
};

export default MessageList;