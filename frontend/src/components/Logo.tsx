import { Briefcase } from 'lucide-react';

export function Logo() {
  return (
    <div className="flex items-center gap-2">
      <Briefcase className="w-8 h-8" />
      <span className="text-2xl font-bold">JobHunt</span>
    </div>
  );
}