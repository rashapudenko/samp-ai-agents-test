import React, { useState, useEffect } from 'react';
import Layout from '../components/layout/Layout';
import SearchBar from '../components/search/SearchBar';
import Filters from '../components/search/Filters';
import SearchResults from '../components/search/SearchResults';
import { getVulnerabilities, Vulnerability } from '../services/api';
import { useRouter } from 'next/router';

const SearchPage: React.FC = () => {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<{ package?: string; severity?: string }>({});
  const [results, setResults] = useState<Vulnerability[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  const resultsPerPage = 10;

  // Handle search
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setCurrentPage(1); // Reset to first page on new search
  };

  // Handle filter changes
  const handleFilterChange = (newFilters: { package?: string; severity?: string }) => {
    setFilters(newFilters);
    setCurrentPage(1); // Reset to first page on filter change
  };

  // Handle vulnerability click
  const handleVulnerabilityClick = (vulnerability: Vulnerability) => {
    // Navigate to detail page or open modal with details
    console.log('Clicked vulnerability:', vulnerability);
  };

  // Fetch results when search or filters change
  useEffect(() => {
    const fetchResults = async () => {
      setIsLoading(true);
      try {
        // Calculate offset
        const offset = (currentPage - 1) * resultsPerPage;

        // Build params
        const params: any = {
          limit: resultsPerPage,
          offset,
        };

        if (filters.package) params.package = filters.package;
        if (filters.severity) params.severity = filters.severity;

        // Fetch results
        const data = await getVulnerabilities(params);
        setResults(data);
        
        // Normally would get total from API
        setTotalResults(data.length > 0 ? data.length + offset : 0);
      } catch (error) {
        console.error('Error fetching results:', error);
        setResults([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [searchQuery, filters, currentPage]);

  return (
    <Layout title="Search - Security Vulnerabilities Knowledge Base" description="Search for Python package security vulnerabilities">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Search Vulnerabilities</h1>
          
          <div className="space-y-6">
            <SearchBar onSearch={handleSearch} placeholder="Search for package vulnerabilities..." />
            
            <Filters onFilterChange={handleFilterChange} />
            
            <div className="mt-8">
              <SearchResults
                results={results}
                isLoading={isLoading}
                onVulnerabilityClick={handleVulnerabilityClick}
              />
              
              {/* Pagination controls would go here */}
              {results.length > 0 && !isLoading && (
                <div className="mt-6 flex justify-between items-center">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Showing {(currentPage - 1) * resultsPerPage + 1} to{' '}
                    {Math.min(currentPage * resultsPerPage, totalResults)} of {totalResults} results
                  </div>
                  
                  <div className="flex space-x-2">
                    <button
                      className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm disabled:opacity-50"
                      disabled={currentPage === 1}
                      onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    >
                      Previous
                    </button>
                    <button
                      className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm disabled:opacity-50"
                      disabled={currentPage * resultsPerPage >= totalResults}
                      onClick={() => setCurrentPage((prev) => prev + 1)}
                    >
                      Next
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SearchPage;