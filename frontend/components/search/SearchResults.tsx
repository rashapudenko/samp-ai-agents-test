import React from 'react';
import { Vulnerability } from '../../services/api';
import Card from '../ui/Card';
import SeverityBadge from '../ui/SeverityBadge';

interface SearchResultsProps {
  results: Vulnerability[];
  isLoading: boolean;
  onVulnerabilityClick?: (vulnerability: Vulnerability) => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({
  results,
  isLoading,
  onVulnerabilityClick,
}) => {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="spinner" />
        <span className="ml-2 text-gray-500 dark:text-gray-400">Loading results...</span>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="text-center p-8 text-gray-500 dark:text-gray-400">
        No vulnerabilities found. Try adjusting your search or filters.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {results.map((vulnerability) => (
        <Card
          key={vulnerability.id}
          hover
          onClick={() => onVulnerabilityClick?.(vulnerability)}
          className="cursor-pointer"
        >
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">{vulnerability.package}</h3>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Published: {vulnerability.published_date}
              </p>
            </div>
            <SeverityBadge severity={vulnerability.severity} />
          </div>
          <p className="mt-3 text-gray-700 dark:text-gray-300">{vulnerability.description}</p>
          
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-2">
            {vulnerability.affected_versions && (
              <div className="text-sm">
                <span className="font-medium text-gray-700 dark:text-gray-300">Affected versions: </span>
                <span className="text-gray-600 dark:text-gray-400">{vulnerability.affected_versions}</span>
              </div>
            )}
            {vulnerability.remediation && (
              <div className="text-sm">
                <span className="font-medium text-gray-700 dark:text-gray-300">Remediation: </span>
                <span className="text-gray-600 dark:text-gray-400">{vulnerability.remediation}</span>
              </div>
            )}
          </div>
        </Card>
      ))}
    </div>
  );
};

export default SearchResults;