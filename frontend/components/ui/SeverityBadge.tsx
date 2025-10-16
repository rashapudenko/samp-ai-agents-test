import React from 'react';
import Badge from './Badge';

interface SeverityBadgeProps {
  severity: string;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

const SeverityBadge: React.FC<SeverityBadgeProps> = ({ 
  severity, 
  className = '',
  size = 'md'
}) => {
  const normalizedSeverity = severity.toLowerCase();
  
  const variantMap: Record<string, 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'> = {
    critical: 'danger',
    high: 'warning',
    medium: 'warning',
    moderate: 'warning',
    low: 'success',
    info: 'info',
  };

  const variant = variantMap[normalizedSeverity] || 'default';

  return (
    <Badge variant={variant} size={size} className={className}>
      {severity.charAt(0).toUpperCase() + severity.slice(1)}
    </Badge>
  );
};

export default SeverityBadge;