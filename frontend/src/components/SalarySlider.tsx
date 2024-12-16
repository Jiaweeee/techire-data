import { useState, useEffect, useRef } from 'react';

interface SalarySliderProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
}

export function SalarySlider({ 
  value, 
  onChange, 
  min = 0, 
  max = 1000000, 
  step = 5000 
}: SalarySliderProps) {
  const [displayValue, setDisplayValue] = useState(value);
  const [isDragging, setIsDragging] = useState(false);
  const sliderRef = useRef<HTMLDivElement>(null);
  
  const formatValue = (val: number) => {
    if (val >= 1000000) {
      return `$${(val / 1000000).toFixed(1)}M`;
    }
    if (val >= 1000) {
      return `$${(val / 1000).toFixed(0)}K`;
    }
    return `$${val}`;
  };

  const getPercentage = (val: number) => {
    return ((val - min) / (max - min)) * 100;
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging || !sliderRef.current) return;
      
      const rect = sliderRef.current.getBoundingClientRect();
      const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
      const percentage = x / rect.width;
      const newValue = Math.round((percentage * (max - min) + min) / step) * step;
      
      setDisplayValue(newValue);
    };

    const handleMouseUp = () => {
      setIsDragging(false);
      onChange(displayValue);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, max, min, onChange, step, displayValue]);

  useEffect(() => {
    setDisplayValue(value);
  }, [value]);

  return (
    <div className="w-full space-y-2">
      <div className="relative pt-5 pb-8" ref={sliderRef}>
        {/* Track Background */}
        <div className="absolute h-1.5 w-full bg-gray-200 rounded-full top-5" />
        
        {/* Colored Track */}
        <div 
          className="absolute h-1.5 bg-blue-600 rounded-full top-5" 
          style={{ width: `${getPercentage(displayValue)}%` }} 
        />
        
        {/* Value Label */}
        <div 
          className={`
            absolute -bottom-1 transform -translate-x-1/2 cursor-grab
            ${isDragging ? 'cursor-grabbing' : ''}
          `}
          style={{ left: `${getPercentage(displayValue)}%` }}
          onMouseDown={handleMouseDown}
        >
          <div className="flex flex-col items-center">
            <div className="
              px-3 py-1 mb-1
              bg-white rounded-full shadow-md
              text-sm font-medium text-gray-900
              border border-gray-200
              select-none
            ">
              {formatValue(displayValue)}
            </div>
            <span className="text-xs text-gray-500 font-medium select-none">Min</span>
          </div>
        </div>
      </div>
    </div>
  );
} 