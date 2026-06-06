import React, { useState } from 'react';
import { ClipboardList, DollarSign, Briefcase, TrendingUp, Plus } from 'lucide-react';
import type { RFQItem, BidProposal } from '../types';

interface VendorDashboardProps {
  rfqsDB: RFQItem[];
  bidsDB: BidProposal[];
  onBidsSubmit: (bid: BidProposal, updatedRfqs: RFQItem[]) => void;
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const VendorDashboard: React.FC<VendorDashboardProps> = ({
  rfqsDB,
  bidsDB,
  onBidsSubmit,
  showToast
}) => {
  const [rfqId, setRfqId] = useState('');
  const [amount, setAmount] = useState('');
  const [delivery, setDelivery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!rfqId || !amount || !delivery) {
      showToast('Please fill out all bid details', 'error');
      return;
    }

    const selectedRfq = rfqsDB.find(r => r.id === rfqId);
    if (!selectedRfq) return;

    const newBid: BidProposal = {
      id: `BID-${400 + bidsDB.length + 1}`,
      rfqId: rfqId,
      rfqDesc: selectedRfq.description,
      amount: parseFloat(amount),
      deliveryTime: delivery,
      status: 'Submitted'
    };

    const updatedRfqs = rfqsDB.map(r => {
      if (r.id === rfqId) {
        return { ...r, bidsCount: r.bidsCount + 1 };
      }
      return r;
    });

    onBidsSubmit(newBid, updatedRfqs);
    setRfqId('');
    setAmount('');
    setDelivery('');
    showToast(`Your quotation bid proposal for ${newBid.rfqId} has been securely submitted!`, 'success');
  };

  return (
    <div className="dashboard-main">
      <div className="dashboard-title-row">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <h1 className="dashboard-title">Vendor Proposal Portal</h1>
          <span className="role-badge badge-vendor">Authorized Vendor</span>
        </div>
        <p className="dashboard-desc">Review published procurement requests, submit contract bids, and check status of submitted quotes.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Available RFQs for Bids</div>
            <div className="stat-value">{rfqsDB.filter(r => r.status === 'Open').length} RFQs</div>
          </div>
          <div className="stat-icon-wrapper stat-green">
            <ClipboardList size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Your Submitted Proposals</div>
            <div className="stat-value">{bidsDB.length} bids</div>
          </div>
          <div className="stat-icon-wrapper stat-butter">
            <DollarSign size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Active Contracts</div>
            <div className="stat-value">2 contract(s)</div>
          </div>
          <div className="stat-icon-wrapper stat-blue">
            <Briefcase size={24} />
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-info">
            <div className="stat-label">Invoiced Revenue</div>
            <div className="stat-value">$48,500</div>
          </div>
          <div className="stat-icon-wrapper stat-purple">
            <TrendingUp size={24} />
          </div>
        </div>
      </div>

      <div className="dashboard-grid-split">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
          <div className="data-card">
            <div className="card-title-row">
              <div className="card-title-text">Open Tenders Available for Bidding</div>
            </div>
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>RFQ ID</th>
                    <th>Procurement Description</th>
                    <th>Target Budget</th>
                    <th>Bids Rec.</th>
                    <th>Deadline</th>
                  </tr>
                </thead>
                <tbody>
                  {rfqsDB.filter(r => r.status === 'Open').map((rfq) => (
                    <tr key={rfq.id}>
                      <td className="font-bold">{rfq.id}</td>
                      <td>{rfq.description}</td>
                      <td className="font-medium">${rfq.budget.toLocaleString()}</td>
                      <td>{rfq.bidsCount} bids submitted</td>
                      <td>{rfq.deadline}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="data-card">
            <div className="card-title-row">
              <div className="card-title-text">Your Bid Proposal History</div>
            </div>
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Proposal ID</th>
                    <th>Target RFQ</th>
                    <th>Quoted Price</th>
                    <th>Delivery Time</th>
                    <th>Bid Status</th>
                  </tr>
                </thead>
                <tbody>
                  {bidsDB.map((bid) => (
                    <tr key={bid.id}>
                      <td className="font-bold">{bid.id}</td>
                      <td>
                        <div className="font-bold">{bid.rfqId}</div>
                        <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{bid.rfqDesc}</div>
                      </td>
                      <td className="font-bold text-primary">${bid.amount.toLocaleString()}</td>
                      <td>{bid.deliveryTime}</td>
                      <td>
                        <span className="status-badge status-open">
                          {bid.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="action-card">
          <h3 className="action-card-title">Submit Bid Proposal</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label" htmlFor="vendor-rfq-select">Select Target RFQ</label>
              <select
                id="vendor-rfq-select"
                className="form-select"
                style={{ paddingLeft: '12px' }}
                value={rfqId}
                onChange={e => setRfqId(e.target.value)}
              >
                <option value="">Choose active RFQ</option>
                {rfqsDB.filter(r => r.status === 'Open').map(r => (
                  <option key={r.id} value={r.id}>
                    {r.id} - {r.description.substring(0, 32)}...
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="vendor-bid-input">Quoted Price ($)</label>
              <input
                id="vendor-bid-input"
                type="number"
                className="form-input"
                style={{ paddingLeft: '12px' }}
                placeholder="68000"
                value={amount}
                onChange={e => setAmount(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="vendor-delivery-input">Estimated Delivery Period</label>
              <input
                id="vendor-delivery-input"
                type="text"
                className="form-input"
                style={{ paddingLeft: '12px' }}
                placeholder="e.g. 10 Days"
                value={delivery}
                onChange={e => setDelivery(e.target.value)}
              />
            </div>

            <button type="submit" className="btn btn-primary" style={{ marginTop: '8px' }}>
              Submit Bid Proposal <Plus size={16} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
