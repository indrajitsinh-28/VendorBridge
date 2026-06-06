import React from 'react';
import { Shield } from 'lucide-react';
import { LoginForm } from '../components/LoginForm';
import { SignupForm } from '../components/SignupForm';
import { ForgotPasswordForm } from '../components/ForgotPasswordForm';
import type { UserAccount } from '../types';
import procurementIllustration from '../assets/procurement_illustration.png';

interface AuthPageProps {
  view: 'LOGIN' | 'SIGNUP' | 'FORGOT_PASSWORD';
  onViewChange: (view: 'LOGIN' | 'SIGNUP' | 'FORGOT_PASSWORD') => void;
  onLoginSuccess: (user: UserAccount) => void;
  onSignupSuccess: (user: UserAccount) => void;
  usersDB: UserAccount[];
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({
  view,
  onViewChange,
  onLoginSuccess,
  onSignupSuccess,
  usersDB,
  showToast
}) => {
  return (
    <div className="auth-container">
      {/* LEFT PANEL: Marketing, Branding, Illustration */}
      <div className="auth-left">
        <div className="bg-shape shape-1" />
        <div className="bg-shape shape-2" />
        <div className="bg-shape shape-3" />

        <div className="left-content">
          <div className="logo-wrapper">
            <Shield className="logo-icon" />
            <span className="logo-text">Vendor<span className="logo-accent">Bridge</span></span>
          </div>

          <div className="illustration-container">
            <img 
              src={procurementIllustration} 
              alt="Procurement Logistics Illustration" 
              className="procurement-illustration"
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.style.display = 'none';
              }}
            />
          </div>

          <div className="left-copy">
            <h1 className="left-headline">Smart Procurement Starts Here</h1>
            <p className="left-support-text">
              Manage vendors, RFQs, quotations, approvals, purchase orders, and invoices from a single, unified enterprise platform.
            </p>
          </div>
        </div>
      </div>

      {/* RIGHT PANEL: Auth Card with Center Forms */}
      <div className="auth-right">
        <div className="auth-card">
          {view === 'LOGIN' && (
            <LoginForm
              onLoginSuccess={onLoginSuccess}
              onViewChange={onViewChange}
              usersDB={usersDB}
              showToast={showToast}
            />
          )}
          {view === 'SIGNUP' && (
            <SignupForm
              onSignupSuccess={onSignupSuccess}
              onViewChange={onViewChange}
              usersDB={usersDB}
              showToast={showToast}
            />
          )}
          {view === 'FORGOT_PASSWORD' && (
            <ForgotPasswordForm
              onViewChange={onViewChange}
              showToast={showToast}
            />
          )}
        </div>
      </div>
    </div>
  );
};
