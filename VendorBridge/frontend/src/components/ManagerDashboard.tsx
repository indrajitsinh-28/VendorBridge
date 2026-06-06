import React from 'react';
import { Shield, CheckCircle2, TrendingUp, Briefcase, Check, X } from 'lucide-react';
import type { RequisitionItem } from '../types';

interface ManagerDashboardProps {
  requisitionsDB: RequisitionItem[];
  onRequisitionsUpdate: (list: RequisitionItem[]) => void;
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const ManagerDashboard: React.FC<ManagerDashboardProps> = ({
  requisitionsDB,
  onRequisitionsUpdate,
  showToast
}) => {
  const handleRequisitionStatus = (id: string, newStatus: 'Approved' | 'Rejected') => {
    const updated = requisitionsDB.map(r => {
      if (r.id === id) {
        return { ...r, status: newStatus };
      }
      return r;
    });
    onRequisitionsUpdate(updated);
    showToast(
      `Requisition ${id} has been ${newStatus.toLowerCase()}!`, 
      newStatus === 'Approved' ? 'success' : 'info'
    );
  };

  return (
    <div className="dashboard-main">
      <div className="dashboard-title-row">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <h1 className="dashboard-title">Executive Approval Center</h1>
          <span className="role-badge badge-manager">Manager / Approver</span>
        </div>
        <p className="dashboard-desc">Review and audit high-budget purchase orders, grant approvals, and allocate funding parameters.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Pending Requisitions</div>
            <div className="stat-value">{requisitionsDB.filter(r => r.status === 'Pending').length} requests</div>
          </div>
          <div className="stat-icon-wrapper stat-butter">
            <Shield size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Approved Items (Monthly)</div>
            <div className="stat-value">{requisitionsDB.filter(r => r.status === 'Approved').length} orders</div>
          </div>
          <div className="stat-icon-wrapper stat-green">
            <CheckCircle2 size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Approval Sign-off Rate</div>
            <div className="stat-value">88.5%</div>
          </div>
          <div className="stat-icon-wrapper stat-blue">
            <TrendingUp size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Managed Budget Utilized</div>
            <div className="stat-value">68%</div>
          </div>
          <div className="stat-icon-wrapper stat-purple">
            <Briefcase size={24} />
          </div>
        </div>
      </div>

      <div className="data-card">
        <div className="card-title-row">
          <div className="card-title-text">Requisitions Awaiting Approval</div>
        </div>
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Requisition ID</th>
                <th>Requester Name</th>
                <th>Items & Description</th>
                <th>Total Requisition Amount</th>
                <th>Status Badge</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {requisitionsDB.map((req) => (
                <tr key={req.id}>
                  <td className="font-bold">{req.id}</td>
                  <td>{req.requester}</td>
                  <td>{req.description}</td>
                  <td className="font-bold text-primary">${req.amount.toLocaleString()}</td>
                  <td>
                    <span className={`status-badge ${
                      req.status === 'Approved' ? 'status-approved' : 
                      req.status === 'Rejected' ? 'status-rejected' : 'status-pending'
                    }`}>
                      {req.status}
                    </span>
                  </td>
                  <td>
                    {req.status === 'Pending' ? (
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button
                          className="btn btn-primary"
                          style={{ padding: '6px 12px', fontSize: '13px', width: 'auto', backgroundColor: 'var(--success-green)' }}
                          onClick={() => handleRequisitionStatus(req.id, 'Approved')}
                        >
                          <Check size={14} /> Approve
                        </button>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '6px 12px', fontSize: '13px', width: 'auto', color: 'var(--error-red)', borderColor: 'var(--error-border)' }}
                          onClick={() => handleRequisitionStatus(req.id, 'Rejected')}
                        >
                          <X size={14} /> Reject
                        </button>
                      </div>
                    ) : (
                      <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Reviewed</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
