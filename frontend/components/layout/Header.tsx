import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { FiMessageSquare, FiSearch, FiHome } from 'react-icons/fi';

const Header: React.FC = () => {
  const router = useRouter();

  const navigation = [
    { name: 'Home', href: '/', icon: <FiHome className="mr-2" /> },
    { name: 'Chat', href: '/chat', icon: <FiMessageSquare className="mr-2" /> },
    { name: 'Search', href: '/search', icon: <FiSearch className="mr-2" /> },
  ];

  const isActive = (href: string) => router.pathname === href;

  return (
    <header className="bg-white dark:bg-gray-900 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-primary-600 dark:text-primary-400">Security Vulnerabilities KB</span>
            </Link>
          </div>
          <nav className="flex space-x-4 items-center">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`inline-flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  isActive(item.href)
                    ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-800'
                }`}
              >
                {item.icon}
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;