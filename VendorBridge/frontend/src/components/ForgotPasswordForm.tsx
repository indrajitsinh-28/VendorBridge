import React, { useState } from 'react';
import { Mail, ArrowRight, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface ForgotPasswordFormProps {
  onViewChange: (view: 'LOGIN') => void;
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const ForgotPasswordForm: React.FC<ForgotPasswordFormProps> = ({
  onViewChange,
  showToast
}) => {
  const [email, setEmail] = useState('');
  const [linkSent, setLinkSent] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateEmailFormat = (val: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      setErrors({ email: 'Email is required' });
      return;
    }
    if (!validateEmailFormat(email)) {
      setErrors({ email: 'Please enter a valid email address' });
      return;
    }

    setErrors({});
    setLinkSent(true);
    showToast('Secure password reset token generated and sent to email!', 'success');
  };

  return (
    <div>
      <div className="card-header">
        <h2 className="card-title">Reset Password</h2>
        <p className="card-subtitle">Enter your email and we'll send you a recovery reset link</p>
      </div>

      {!linkSent ? (
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="forgot-email-input">Email Address</label>
            <div className="input-wrapper">
              <Mail className="input-icon-left" />
              <input
                id="forgot-email-input"
                type="text"
                className="form-input"
                placeholder="name@company.com"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (errors.email) setErrors({});
                }}
              />
            </div>
            {errors.email && <div className="error-message"><AlertTriangle size={14} />{errors.email}</div>}
          </div>

          <button type="submit" className="btn btn-primary">
            Send Reset Link <ArrowRight size={18} />
          </button>

          <p className="switch-mode-text">
            <a
              href="#"
              className="switch-mode-link"
              onClick={(e) => {
                e.preventDefault();
                onViewChange('LOGIN');
              }}
            >
              Back to Login
            </a>
          </p>
        </form>
      ) : (
        <div className="success-state">
          <div className="success-icon-wrapper">
            <CheckCircle2 size={32} />
          </div>
          <h3 className="success-title">Check your inbox</h3>
          <p className="success-text">
            We have sent a secure password reset link to <strong>{email}</strong>. 
            Please follow the instruction in the email to recover your credentials.
          </p>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => {
              onViewChange('LOGIN');
              setEmail('');
              setLinkSent(false);
            }}
          >
            Return to Sign In
          </button>
        </div>
      )}
    </div>
  );
};
