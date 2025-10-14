/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['security.snyk.io'],
  },
  env: {
    API_URL: process.env.API_URL || 'http://localhost:8000',
  },
  // Enable compression for better performance
  compress: true,
  // Security optimizations
  poweredByHeader: false,
  generateEtags: false,
};

module.exports = nextConfig;