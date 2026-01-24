import React from 'react';

interface ImageOptimizerProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  lazy?: boolean;
}

const ImageOptimizer: React.FC<ImageOptimizerProps> = ({
  src,
  alt,
  width,
  height,
  className,
  lazy = true
}) => {
  return (
    <img
      src={src}
      alt={alt}
      width={width}
      height={height}
      className={className}
      loading={lazy ? "lazy" : "eager"}
      decoding="async"
      style={{
        contentVisibility: 'auto',
        contain: 'layout style paint'
      }}
    />
  );
};

export default ImageOptimizer;