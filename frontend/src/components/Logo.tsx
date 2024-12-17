import { LucideCheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface LogoProps {
  onClick?: () => void;
}

export function Logo({ onClick }: LogoProps) {
  const navigate = useNavigate();

  const handleClick = () => {
    if (onClick) {
      onClick();
    } else {
      navigate('/');
    }
  };

  return (
    <div 
      className="flex items-center gap-2 cursor-pointer" 
      onClick={handleClick}
    >
      <LucideCheckCircle color="#FF0000" strokeWidth={3} className="w-8 h-8" />
      <span className="text-2xl font-bold">RealTechJobs</span>
    </div>
  );
}