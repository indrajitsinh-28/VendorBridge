import React, { useState } from 'react';
import { ClipboardList, DollarSign, Briefcase, TrendingUp, Plus } from 'lucide-react';
import type { RFQItem, BidProposal } from '../types';

interface ProcurementDashboardProps {
  rfqsDB: RFQItem[];
  bidsDB: BidProposal[];
  onRfqsUpdate: (list: RFQItem[]) => void;
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const ProcurementDashboard: React.FC<ProcurementDashboardProps> = ({
  rfqsDB,
  bidsDB,
  onRfqsUpdate,
  showToast
}) => {
  const [desc, setDesc] = useState('');
  const [budget, setBudget] = useState('');
  const [deadline, setDeadline] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!desc || !budget || !deadline) {
      showToast('Please fill out all RFQ details', 'error');
      return;
    }

    const newRfq: RFQItem = {
      id: `RFQ-2026-00${rfqsDB.length + 1}`,
      description: desc,
      budget: parseFloat(budget),
      deadline: deadline,
      status: 'Open',
      bidsCount: 0
    };

    onRfqsUpdate([newRfq, ...rfqsDB]);
    setDesc('');
    setBudget('');
    setDeadline('');
    showToast(`RFQ ${newRfq.id} issued and published on the Portal!`, 'success');
  };

  return (
    <div className="dashboard-main">
      <div className="dashboard-title-row">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <h1 className="dashboard-title">Procurement Officer Command</h1>
          <span className="role-badge badge-procurement">Procurement Officer</span>
        </div>
        <p className="dashboard-desc">Draft RFQs, analyze bidding documents, issue requests for quotations, and log supplier proposals.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Active RFQs</div>
            <div className="stat-value">{rfqsDB.filter(r => r.status === 'Open').length}</div>
          </div>
          <div className="stat-icon-wrapper stat-green">
            <ClipboardList size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Total Bids Received</div>
            <div className="stat-value">{bidsDB.length}</div>
          </div>
          <div className="stat-icon-wrapper stat-butter">
            <DollarSign size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Target Procurement Budget</div>
            <div className="stat-value">$312,000</div>
          </div>
          <div className="stat-icon-wrapper stat-blue">
            <Briefcase size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Historical Savings</div>
            <div className="stat-value">+14.2%</div>
          </div>
          <div className="stat-icon-wrapper stat-purple">
            <TrendingUp size={24} />
          </div>
        </div>
      </div>

      <div className="dashboard-grid-split">
        <div className="data-card">
          <div className="card-title-row">
            <div className="card-title-text">Active Requests for Quotation (RFQs)</div>
          </div>
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>RFQ ID</th>
                  <th>Description</th>
                  <th>Budget</th>
                  <th>Deadline</th>
                  <th>Bids Count</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {rfqsDB.map((rfq) => (
                  <tr key={rfq.id}>
                    <td className="font-bold">{rfq.id}</td>
                    <td>{rfq.description}</td>
                    <td className="font-medium">${rfq.budget.toLocaleString()}</td>
                    <td>{rfq.deadline}</td>
                    <td className="text-center font-bold">{rfq.bidsCount} proposals</td>
                    <td>
                      <span className={`status-badge ${rfq.status === 'Open' ? 'status-open' : 'status-completed'}`}>
                        {rfq.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="action-card">
          <h3 className="action-card-title">Issue New RFQ</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label" htmlFor="rfq-desc-input">RFQ Description</label>
              <input
                id="rfq-desc-input"
                type="text"
                className="form-input"
                style={{ paddingLeft: '12px' }}
                placeholder="High-capacity battery systems for server warehouse"
                value={desc}
                onChange={e => setDesc(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="rfq-budget-input">Target Budget ($)</label>
              <input
                id="rfq-budget-input"
                type="number"
                className="form-input"
                style={{ paddingLeft: '12px' }}
                placeholder="30000"
                value={budget}
                onChange={e => setBudget(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="rfq-deadline-input">Closing Deadline</label>
              <input
                id="rfq-deadline-input"
                type="date"
                className="form-input"
                style={{ paddingLeft: '12px' }}
                value={deadline}
                onChange={e => setDeadline(e.target.value)}
              />
            </div>

            <button type="submit" className="btn btn-primary" style={{ marginTop: '8px' }}>
              Publish RFQ <Plus size={16} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
