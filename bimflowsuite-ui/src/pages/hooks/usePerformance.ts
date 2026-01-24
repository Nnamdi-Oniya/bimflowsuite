import { useEffect } from 'react';

export const usePerformance = () => {
  useEffect(() => {
    // Log performance metrics
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        console.log(`${entry.name}: ${entry.startTime}`);
      });
    });

    observer.observe({ entryTypes: ['navigation', 'paint', 'largest-contentful-paint'] });

    return () => observer.disconnect();
  }, []);
};

export const usePreload = (paths: string[]) => {
  useEffect(() => {
    paths.forEach(path => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = path;
      link.as = path.endsWith('.css') ? 'style' : 
                path.endsWith('.js') ? 'script' : 'image';
      document.head.appendChild(link);
    });
  }, [paths]);
};