import React, { useState } from 'react';
import { User, Shield, ClipboardList, TrendingUp, Plus } from 'lucide-react';
import type { UserAccount, RFQItem, UserRole } from '../types';

interface AdminDashboardProps {
  usersDB: UserAccount[];
  rfqsDB: RFQItem[];
  onUsersUpdate: (list: UserAccount[]) => void;
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const AdminDashboard: React.FC<AdminDashboardProps> = ({
  usersDB,
  rfqsDB,
  onUsersUpdate,
  showToast
}) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<UserRole>('VENDOR');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !password) {
      showToast('Please fill out all user creation fields', 'error');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showToast('Please enter a valid email for the new user', 'error');
      return;
    }

    if (usersDB.some(u => u.email.toLowerCase() === email.toLowerCase())) {
      showToast('A user account with this email already exists', 'error');
      return;
    }

    const newUser: UserAccount = {
      name,
      email,
      password,
      role,
      status: 'Active'
    };

    onUsersUpdate([...usersDB, newUser]);
    setName('');
    setEmail('');
    setPassword('');
    setRole('VENDOR');
    showToast(`User account for ${newUser.name} created successfully!`, 'success');
  };

  const handleApproveVendor = (userEmail: string) => {
    const updated = usersDB.map(u => {
      if (u.email === userEmail) {
        return { ...u, status: 'Active' as const };
      }
      return u;
    });
    onUsersUpdate(updated);
    showToast(`Approved registration for ${userEmail}. Access activated!`, 'success');
  };

  return (
    <div className="dashboard-main">
      <div className="dashboard-title-row">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <h1 className="dashboard-title">Admin Command Center</h1>
          <span className="role-badge badge-admin">Administrator</span>
        </div>
        <p className="dashboard-desc">Manage system settings, review audit trails, and approve vendor access roles.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Total Registered Users</div>
            <div className="stat-value">{usersDB.length}</div>
          </div>
          <div className="stat-icon-wrapper stat-green">
            <User size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Pending Approvals</div>
            <div className="stat-value">{usersDB.filter(u => u.status === 'Pending').length}</div>
          </div>
          <div className="stat-icon-wrapper stat-butter">
            <Shield size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Active RFQs</div>
            <div className="stat-value">{rfqsDB.filter(r => r.status === 'Open').length}</div>
          </div>
          <div className="stat-icon-wrapper stat-blue">
            <ClipboardList size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">System Performance</div>
            <div className="stat-value">99.9%</div>
          </div>
          <div className="stat-icon-wrapper stat-purple">
            <TrendingUp size={24} />
          </div>
        </div>
      </div>

      <div className="dashboard-grid-split">
        <div className="data-card">
          <div className="card-title-row">
            <div className="card-title-text">Users & Credentials database</div>
          </div>
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Full Name</th>
                  <th>Email Address</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {usersDB.map((usr) => (
                  <tr key={usr.email}>
                    <td className="font-bold">{usr.name}</td>
                    <td>{usr.email}</td>
                    <td>
                      <span className={`role-badge ${
                        usr.role === 'ADMIN' ? 'badge-admin' :
                        usr.role === 'PROCUREMENT' ? 'badge-procurement' :
                        usr.role === 'MANAGER' ? 'badge-manager' : 'badge-vendor'
                      }`}>
                        {usr.role}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${usr.status === 'Active' ? 'status-approved' : 'status-pending'}`}>
                        {usr.status === 'Active' ? 'Active' : 'Pending Approval'}
                      </span>
                    </td>
                    <td>
                      {usr.status === 'Pending' ? (
                        <button
                          className="btn btn-primary"
                          style={{ padding: '6px 12px', fontSize: '12px', width: 'auto' }}
                          onClick={() => handleApproveVendor(usr.email)}
                        >
                          Approve Registration
                        </button>
                      ) : (
                        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Full Access</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="action-card">
          <h3 className="action-card-title">Add New User</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label" htmlFor="admin-name-input">Full Name</label>
              <input
                id="admin-name-input"
                type="text"
                className="form-input"
                style={{ paddingLeft: '12px' }}
                placeholder="Jane Smith"
                value={name}
                onChange={e => setName(e.target.value)}
              />
            </div>
            
            <div className="form-group">
              <label className="form-label" htmlFor="admin-email-input">Email Address</label>
              <input
                id="admin-email-input"
                type="text"
                className="form-input"
                style={{ paddingLeft: '12px' }}
                placeholder="jane@company.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="admin-pwd-input">Temp Password</label>
              <input
                id="admin-pwd-input"
                type="password"
                className="form-input"
                style={{ paddingLeft: '12px' }}
                placeholder="TempPassword123"
                value={password}
                onChange={e => setPassword(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="admin-role-select">Access Role</label>
              <select
                id="admin-role-select"
                className="form-select"
                style={{ paddingLeft: '12px' }}
                value={role}
                onChange={e => setRole(e.target.value as UserRole)}
              >
                <option value="ADMIN">Admin</option>
                <option value="PROCUREMENT">Procurement Officer</option>
                <option value="MANAGER">Manager / Approver</option>
                <option value="VENDOR">Vendor</option>
              </select>
            </div>

            <button type="submit" className="btn btn-primary" style={{ marginTop: '8px' }}>
              Create User <Plus size={16} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
