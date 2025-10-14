import React, { ReactNode } from 'react';

interface CardProps {
  title?: string;
  subtitle?: string;
  children: ReactNode;
  footer?: ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

const Card: React.FC<CardProps> = ({
  title,
  subtitle,
  children,
  footer,
  className = '',
  hover = false,
  onClick,
}) => {
  const cardClasses = `bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden ${hover ? 'card-hover' : ''} ${onClick ? 'cursor-pointer' : ''} ${className}`;

  return (
    <div className={cardClasses} onClick={onClick}>
      {(title || subtitle) && (
        <div className="px-4 py-4 border-b border-gray-200 dark:border-gray-700">
          {title && <h3 className="text-lg font-medium text-gray-900 dark:text-white">{title}</h3>}
          {subtitle && <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{subtitle}</p>}
        </div>
      )}
      <div className="px-4 py-4">{children}</div>
      {footer && <div className="px-4 py-3 bg-gray-50 dark:bg-gray-700">{footer}</div>}
    </div>
  );
};

export default Card;