import React, { useState, useEffect } from 'react';
import { Mail, Lock, Eye, EyeOff, ArrowRight, AlertTriangle } from 'lucide-react';
import type { UserAccount } from '../types';

interface LoginFormProps {
  onLoginSuccess: (user: UserAccount) => void;
  onViewChange: (view: 'SIGNUP' | 'FORGOT_PASSWORD') => void;
  usersDB: UserAccount[];
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({
  onLoginSuccess,
  onViewChange,
  usersDB,
  showToast
}) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    const rememberedEmail = localStorage.getItem('vb_remembered_email');
    if (rememberedEmail) {
      setEmail(rememberedEmail);
      setRememberMe(true);
    }
  }, []);

  const validateEmailFormat = (val: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};

    if (!email) {
      newErrors.email = 'Email address is required';
    } else if (!validateEmailFormat(email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      showToast('Please fix the errors in the login form', 'error');
      return;
    }

    const foundUser = usersDB.find(
      u => u.email.toLowerCase() === email.toLowerCase() && u.password === password
    );

    if (foundUser) {
      if (foundUser.status === 'Pending') {
        showToast('Your account approval is pending. Please contact the administrator.', 'error');
        return;
      }

      if (rememberMe) {
        localStorage.setItem('vb_remembered_email', email);
      } else {
        localStorage.removeItem('vb_remembered_email');
      }

      // Simulate JWT payload generation
      const mockJWTHeader = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
      const mockJWTPayload = btoa(JSON.stringify({ 
        sub: foundUser.email, 
        name: foundUser.name, 
        role: foundUser.role,
        exp: Math.floor(Date.now() / 1000) + (60 * 60)
      }));
      const mockJWTSignature = "hmac_signature_vendorbridge_erp_secure_key";
      const simulatedToken = `${mockJWTHeader}.${mockJWTPayload}.${mockJWTSignature}`;

      sessionStorage.setItem('vb_jwt_token', simulatedToken);
      sessionStorage.setItem('vb_current_user', JSON.stringify(foundUser));

      onLoginSuccess(foundUser);
    } else {
      setErrors({
        email: 'Invalid credentials. Check your email or password.',
        password: ' '
      });
      showToast('Authentication failed. Invalid credentials.', 'error');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="card-header">
        <h2 className="card-title">Welcome back</h2>
        <p className="card-subtitle">Sign in to continue to VendorBridge</p>
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="email-input">Email Address</label>
        <div className="input-wrapper">
          <Mail className="input-icon-left" />
          <input
            id="email-input"
            type="text"
            className="form-input"
            placeholder="name@company.com"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (errors.email) setErrors(prev => { const { email, ...rest } = prev; return rest; });
            }}
          />
        </div>
        {errors.email && <div className="error-message"><AlertTriangle size={14} />{errors.email}</div>}
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="password-input">Password</label>
        <div className="input-wrapper">
          <Lock className="input-icon-left" />
          <input
            id="password-input"
            type={showPassword ? "text" : "password"}
            className="form-input form-input-password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              if (errors.password) setErrors(prev => { const { password, ...rest } = prev; return rest; });
            }}
          />
          <button
            type="button"
            className="input-icon-right"
            onClick={() => setShowPassword(!showPassword)}
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
        {errors.password && errors.password !== ' ' && <div className="error-message"><AlertTriangle size={14} />{errors.password}</div>}
      </div>

      <div className="form-actions-row">
        <label className="checkbox-container">
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
          />
          Remember me
        </label>
        <a
          href="#"
          className="forgot-password-link"
          onClick={(e) => {
            e.preventDefault();
            onViewChange('FORGOT_PASSWORD');
          }}
        >
          Forgot Password?
        </a>
      </div>

      <button type="submit" className="btn btn-primary">
        Sign In <ArrowRight size={18} />
      </button>

      <div className="divider">or</div>

      <button
        type="button"
        className="btn btn-secondary"
        onClick={() => {
          setEmail('admin@vendorbridge.com');
          setPassword('Password123!');
          showToast('Pre-filled Demo Credentials: Administrator', 'info');
        }}
      >
        Use Admin Demo Account
      </button>

      <p className="switch-mode-text">
        Don't have an account? 
        <a
          href="#"
          className="switch-mode-link"
          onClick={(e) => {
            e.preventDefault();
            onViewChange('SIGNUP');
          }}
        >
          Create Account
        </a>
      </p>
    </form>
  );
};
