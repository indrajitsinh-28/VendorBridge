import React, { useState, useEffect } from 'react';
import { Mail, Lock, User, Shield, Eye, EyeOff, ArrowRight, AlertTriangle } from 'lucide-react';
import type { UserAccount, UserRole } from '../types';

interface SignupFormProps {
  onSignupSuccess: (user: UserAccount) => void;
  onViewChange: (view: 'LOGIN') => void;
  usersDB: UserAccount[];
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const SignupForm: React.FC<SignupFormProps> = ({
  onSignupSuccess,
  onViewChange,
  usersDB,
  showToast
}) => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState<UserRole | ''>('');
  const [acceptTerms, setAcceptTerms] = useState(false);

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState<'weak' | 'medium' | 'strong' | ''>('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const calculatePasswordStrength = (pwd: string) => {
    if (!pwd) return '';
    let score = 0;
    if (pwd.length >= 6) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^a-zA-Z0-9]/.test(pwd)) score++;
    if (score === 1) return 'weak';
    if (score === 2) return 'medium';
    if (score === 3) return 'strong';
    return 'weak';
  };

  useEffect(() => {
    setPasswordStrength(calculatePasswordStrength(password));
  }, [password]);

  // Real-time confirmation matching
  useEffect(() => {
    if (confirmPassword && password !== confirmPassword) {
      setErrors(prev => ({ ...prev, confirmPassword: 'Passwords do not match' }));
    } else {
      setErrors(prev => {
        const { confirmPassword: _, ...rest } = prev;
        return rest;
      });
    }
  }, [confirmPassword, password]);

  const validateEmailFormat = (val: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};

    if (!fullName.trim()) {
      newErrors.fullName = 'Full Name is required';
    }

    if (!email) {
      newErrors.email = 'Email address is required';
    } else if (!validateEmailFormat(email)) {
      newErrors.email = 'Please enter a valid email address';
    } else {
      const emailExists = usersDB.some(u => u.email.toLowerCase() === email.toLowerCase());
      if (emailExists) {
        newErrors.email = 'An account with this email already exists';
      }
    }

    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (!confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!role) {
      newErrors.role = 'Please select your role';
    }

    if (!acceptTerms) {
      newErrors.acceptTerms = 'You must agree to the Terms & Conditions';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      showToast('Please fix the errors in the registration form', 'error');
      return;
    }

    const newAccount: UserAccount = {
      name: fullName,
      email,
      password,
      role: role as UserRole,
      status: role === 'VENDOR' ? 'Pending' : 'Active'
    };

    onSignupSuccess(newAccount);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="card-header">
        <h2 className="card-title">Create Account</h2>
        <p className="card-subtitle">Register a new access role on VendorBridge ERP</p>
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="signup-name-input">Full Name</label>
        <div className="input-wrapper">
          <User className="input-icon-left" />
          <input
            id="signup-name-input"
            type="text"
            className="form-input"
            placeholder="John Doe"
            value={fullName}
            onChange={(e) => {
              setFullName(e.target.value);
              if (errors.fullName) setErrors(prev => { const { fullName: _, ...rest } = prev; return rest; });
            }}
          />
        </div>
        {errors.fullName && <div className="error-message"><AlertTriangle size={14} />{errors.fullName}</div>}
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="signup-email-input">Email Address</label>
        <div className="input-wrapper">
          <Mail className="input-icon-left" />
          <input
            id="signup-email-input"
            type="text"
            className="form-input"
            placeholder="name@company.com"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (errors.email) setErrors(prev => { const { email: _, ...rest } = prev; return rest; });
            }}
          />
        </div>
        {errors.email && <div className="error-message"><AlertTriangle size={14} />{errors.email}</div>}
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="signup-password-input">Password</label>
        <div className="input-wrapper">
          <Lock className="input-icon-left" />
          <input
            id="signup-password-input"
            type={showPassword ? "text" : "password"}
            className="form-input form-input-password"
            placeholder="At least 6 characters"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              if (errors.password) setErrors(prev => { const { password: _, ...rest } = prev; return rest; });
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
        {password && (
          <div className="password-strength-container">
            <div className="password-strength-bar-bg">
              <div className={`password-strength-bar ${
                passwordStrength === 'weak' ? 'strength-weak' :
                passwordStrength === 'medium' ? 'strength-medium' :
                passwordStrength === 'strong' ? 'strength-strong' : ''
              }`} />
            </div>
            <span className={`password-strength-text ${
              passwordStrength === 'weak' ? 'text-weak' :
              passwordStrength === 'medium' ? 'text-medium' :
              passwordStrength === 'strong' ? 'text-strong' : ''
            }`}>
              Strength: {passwordStrength.charAt(0).toUpperCase() + passwordStrength.slice(1)}
            </span>
          </div>
        )}
        {errors.password && <div className="error-message"><AlertTriangle size={14} />{errors.password}</div>}
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="signup-confirm-password-input">Confirm Password</label>
        <div className="input-wrapper">
          <Lock className="input-icon-left" />
          <input
            id="signup-confirm-password-input"
            type={showConfirmPassword ? "text" : "password"}
            className="form-input form-input-password"
            placeholder="Verify your password"
            value={confirmPassword}
            onChange={(e) => {
              setConfirmPassword(e.target.value);
              if (errors.confirmPassword) setErrors(prev => { const { confirmPassword: _, ...rest } = prev; return rest; });
            }}
          />
          <button
            type="button"
            className="input-icon-right"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            aria-label={showConfirmPassword ? "Hide password" : "Show password"}
          >
            {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
        {errors.confirmPassword && <div className="error-message"><AlertTriangle size={14} />{errors.confirmPassword}</div>}
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="signup-role-input">User Access Role</label>
        <div className="select-wrapper">
          <Shield className="input-icon-left" />
          <select
            id="signup-role-input"
            className="form-select"
            value={role}
            onChange={(e) => {
              setRole(e.target.value as UserRole);
              if (errors.role) setErrors(prev => { const { role: _, ...rest } = prev; return rest; });
            }}
          >
            <option value="" disabled>Select role type</option>
            <option value="ADMIN">Admin</option>
            <option value="PROCUREMENT">Procurement Officer</option>
            <option value="MANAGER">Manager / Approver</option>
            <option value="VENDOR">Vendor (Requires Admin Approval)</option>
          </select>
          <div className="select-arrow">▼</div>
        </div>
        {errors.role && <div className="error-message"><AlertTriangle size={14} />{errors.role}</div>}
      </div>

      <div className="terms-container">
        <label className="checkbox-container">
          <input
            type="checkbox"
            checked={acceptTerms}
            onChange={(e) => {
              setAcceptTerms(e.target.checked);
              if (errors.acceptTerms) setErrors(prev => { const { acceptTerms: _, ...rest } = prev; return rest; });
            }}
          />
          I accept the VendorBridge Terms & Conditions
        </label>
        {errors.acceptTerms && <div className="error-message"><AlertTriangle size={14} />{errors.acceptTerms}</div>}
      </div>

      <button type="submit" className="btn btn-primary">
        Register Account <ArrowRight size={18} />
      </button>

      <p className="switch-mode-text">
        Already have an account? 
        <a
          href="#"
          className="switch-mode-link"
          onClick={(e) => {
            e.preventDefault();
            onViewChange('LOGIN');
          }}
        >
          Sign In
        </a>
      </p>
    </form>
  );
};
