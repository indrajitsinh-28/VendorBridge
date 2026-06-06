import React from 'react';
import { Shield, LogOut } from 'lucide-react';
import type { UserAccount, RFQItem, RequisitionItem, BidProposal } from '../types';
import { AdminDashboard } from '../components/AdminDashboard';
import { ProcurementDashboard } from '../components/ProcurementDashboard';
import { ManagerDashboard } from '../components/ManagerDashboard';
import { VendorDashboard } from '../components/VendorDashboard';

interface DashboardPageProps {
  currentUser: UserAccount;
  onLogout: () => void;
  usersDB: UserAccount[];
  rfqsDB: RFQItem[];
  requisitionsDB: RequisitionItem[];
  bidsDB: BidProposal[];
  onUsersUpdate: (list: UserAccount[]) => void;
  onRfqsUpdate: (list: RFQItem[]) => void;
  onRequisitionsUpdate: (list: RequisitionItem[]) => void;
  onBidsSubmit: (bid: BidProposal, updatedRfqs: RFQItem[]) => void;
  showToast: (message: string, type: 'success' | 'info' | 'error') => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  currentUser,
  onLogout,
  usersDB,
  rfqsDB,
  requisitionsDB,
  bidsDB,
  onUsersUpdate,
  onRfqsUpdate,
  onRequisitionsUpdate,
  onBidsSubmit,
  showToast
}) => {
  return (
    <div className="dashboard-container">
      {/* Navigation header */}
      <header className="dashboard-header">
        <div className="header-left">
          <div className="logo-wrapper">
            <Shield className="logo-icon" />
            <span className="logo-text">Vendor<span className="logo-accent">Bridge</span></span>
          </div>
          <span style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>ERP Portal v1.2</span>
        </div>

        <div className="header-right">
          <div className="user-profile-badge">
            <div className="profile-avatar">
              {currentUser.name.charAt(0)}
            </div>
            <div>
              <strong>{currentUser.name}</strong>
            </div>
          </div>
          <button className="btn-logout" onClick={onLogout}>
            <LogOut size={14} /> Log Out
          </button>
        </div>
      </header>

      {/* Role-based dashboard selection */}
      {currentUser.role === 'ADMIN' && (
        <AdminDashboard
          usersDB={usersDB}
          rfqsDB={rfqsDB}
          onUsersUpdate={onUsersUpdate}
          showToast={showToast}
        />
      )}
      {currentUser.role === 'PROCUREMENT' && (
        <ProcurementDashboard
          rfqsDB={rfqsDB}
          bidsDB={bidsDB}
          onRfqsUpdate={onRfqsUpdate}
          showToast={showToast}
        />
      )}
      {currentUser.role === 'MANAGER' && (
        <ManagerDashboard
          requisitionsDB={requisitionsDB}
          onRequisitionsUpdate={onRequisitionsUpdate}
          showToast={showToast}
        />
      )}
      {currentUser.role === 'VENDOR' && (
        <VendorDashboard
          rfqsDB={rfqsDB}
          bidsDB={bidsDB}
          onBidsSubmit={onBidsSubmit}
          showToast={showToast}
        />
      )}
    </div>
  );
};
