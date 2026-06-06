import React from 'react';
import { CheckCircle2 } from 'lucide-react';

interface ToastProps {
  message: string;
}

export const Toast: React.FC<ToastProps> = ({ message }) => {
  return (
    <div className="toast-notification">
      <CheckCircle2 size={18} style={{ color: 'var(--accent-butter)' }} />
      <span>{message}</span>
    </div>
  );
};
