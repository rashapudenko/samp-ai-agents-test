import React, { useState, useEffect } from 'react';
import { getPackages, getSeverities } from '../../services/api';

interface FiltersProps {
  onFilterChange: (filters: { package?: string; severity?: string }) => void;
  className?: string;
}

const Filters: React.FC<FiltersProps> = ({ onFilterChange, className = '' }) => {
  const [packages, setPackages] = useState<string[]>([]);
  const [severities, setSeverities] = useState<string[]>([]);
  const [selectedPackage, setSelectedPackage] = useState<string>('');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  // Fetch filter options
  useEffect(() => {
    const fetchFilterOptions = async () => {
      setIsLoading(true);
      try {
        const [packagesData, severitiesData] = await Promise.all([
          getPackages(),
          getSeverities(),
        ]);
        setPackages(packagesData);
        setSeverities(severitiesData);
      } catch (error) {
        console.error('Error fetching filter options:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchFilterOptions();
  }, []);

  // Handle filter changes
  const handlePackageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedPackage(value);
    onFilterChange({ package: value || undefined, severity: selectedSeverity || undefined });
  };

  const handleSeverityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedSeverity(value);
    onFilterChange({ package: selectedPackage || undefined, severity: value || undefined });
  };

  const handleClearFilters = () => {
    setSelectedPackage('');
    setSelectedSeverity('');
    onFilterChange({});
  };

  return (
    <div className={`flex flex-wrap gap-4 items-center ${className}`}>
      <div className="w-full sm:w-auto">
        <label htmlFor="package-filter" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Package
        </label>
        <select
          id="package-filter"
          className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-700 dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
          value={selectedPackage}
          onChange={handlePackageChange}
          disabled={isLoading || packages.length === 0}
        >
          <option value="">All Packages</option>
          {packages.map((pkg) => (
            <option key={pkg} value={pkg}>
              {pkg}
            </option>
          ))}
        </select>
      </div>

      <div className="w-full sm:w-auto">
        <label htmlFor="severity-filter" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Severity
        </label>
        <select
          id="severity-filter"
          className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-700 dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
          value={selectedSeverity}
          onChange={handleSeverityChange}
          disabled={isLoading || severities.length === 0}
        >
          <option value="">All Severities</option>
          {severities.map((severity) => (
            <option key={severity} value={severity}>
              {severity}
            </option>
          ))}
        </select>
      </div>

      {(selectedPackage || selectedSeverity) && (
        <button
          type="button"
          className="mt-4 sm:mt-6 px-3 py-1 text-sm text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300"
          onClick={handleClearFilters}
        >
          Clear Filters
        </button>
      )}
    </div>
  );
};

export default Filters;