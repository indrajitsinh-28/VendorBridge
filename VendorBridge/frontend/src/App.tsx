import { useState, useEffect } from 'react';
import type { UserAccount, RFQItem, RequisitionItem, BidProposal } from './types';
import { AuthPage } from './pages/AuthPage';
import { DashboardPage } from './pages/DashboardPage';
import { Toast } from './components/Toast';
import './App.css';

type ViewState = 'LOGIN' | 'SIGNUP' | 'FORGOT_PASSWORD' | 'DASHBOARD';

function App() {
  const [view, setView] = useState<ViewState>('LOGIN');
  const [currentUser, setCurrentUser] = useState<UserAccount | null>(null);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'info' | 'error' } | null>(null);

  // Mock Databases
  const [usersDB, setUsersDB] = useState<UserAccount[]>([]);
  const [rfqsDB, setRfqsDB] = useState<RFQItem[]>([]);
  const [requisitionsDB, setRequisitionsDB] = useState<RequisitionItem[]>([]);
  const [bidsDB, setBidsDB] = useState<BidProposal[]>([]);

  // Initialize and check session
  useEffect(() => {
    const localUsers = localStorage.getItem('vb_users_db');
    const localRfqs = localStorage.getItem('vb_rfqs_db');
    const localReqs = localStorage.getItem('vb_reqs_db');
    const localBids = localStorage.getItem('vb_bids_db');

    if (localUsers) {
      setUsersDB(JSON.parse(localUsers));
    } else {
      const defaultUsers: UserAccount[] = [
        { name: 'Sarah Jenkins', email: 'admin@vendorbridge.com', password: 'Password123!', role: 'ADMIN', status: 'Active' },
        { name: 'Michael Chen', email: 'officer@vendorbridge.com', password: 'Password123!', role: 'PROCUREMENT', status: 'Active' },
        { name: 'Elena Rostova', email: 'approver@vendorbridge.com', password: 'Password123!', role: 'MANAGER', status: 'Active' },
        { name: 'Acme Logistics Bids', email: 'vendor@acme.com', password: 'Password123!', role: 'VENDOR', status: 'Active' },
        { name: 'Globex Procurement', email: 'globex@vendor.com', password: 'Password123!', role: 'VENDOR', status: 'Active' }
      ];
      setUsersDB(defaultUsers);
      localStorage.setItem('vb_users_db', JSON.stringify(defaultUsers));
    }

    if (localRfqs) {
      setRfqsDB(JSON.parse(localRfqs));
    } else {
      const defaultRfqs: RFQItem[] = [
        { id: 'RFQ-2026-001', description: 'Enterprise Server Upgrade (Rackmount & SSDs)', budget: 75000, deadline: '2026-06-25', status: 'Open', bidsCount: 3 },
        { id: 'RFQ-2026-002', description: 'Eco-Friendly Office Stationaries & Paper', budget: 12000, deadline: '2026-06-18', status: 'Open', bidsCount: 1 },
        { id: 'RFQ-2026-003', description: 'Logistics Courier Services - Q3/Q4 Contract', budget: 180000, deadline: '2026-07-01', status: 'Open', bidsCount: 2 },
        { id: 'RFQ-2026-004', description: 'Data Center Cooling System Maintenance', budget: 45000, deadline: '2026-05-15', status: 'Completed', bidsCount: 4 }
      ];
      setRfqsDB(defaultRfqs);
      localStorage.setItem('vb_rfqs_db', JSON.stringify(defaultRfqs));
    }

    if (localReqs) {
      setRequisitionsDB(JSON.parse(localReqs));
    } else {
      const defaultReqs: RequisitionItem[] = [
        { id: 'REQ-901', requester: 'Michael Chen', description: 'Bulk Purchase Laptop Workstations (x15)', amount: 22500, status: 'Pending' },
        { id: 'REQ-902', requester: 'Alex Mercer', description: 'Data Center Security Software Annual Subscription', amount: 8400, status: 'Pending' },
        { id: 'REQ-903', requester: 'Michael Chen', description: 'Office HVAC Repair and Compressor replacement', amount: 6200, status: 'Approved' },
        { id: 'REQ-904', requester: 'Sarah Jenkins', description: 'Procurement Consulting services - Quarter 2', amount: 15000, status: 'Rejected' }
      ];
      setRequisitionsDB(defaultReqs);
      localStorage.setItem('vb_reqs_db', JSON.stringify(defaultReqs));
    }

    if (localBids) {
      setBidsDB(JSON.parse(localBids));
    } else {
      const defaultBids: BidProposal[] = [
        { id: 'BID-401', rfqId: 'RFQ-2026-001', rfqDesc: 'Enterprise Server Upgrade (Rackmount & SSDs)', amount: 72000, deliveryTime: '14 Days', status: 'Submitted' },
        { id: 'BID-402', rfqId: 'RFQ-2026-003', rfqDesc: 'Logistics Courier Services - Q3/Q4 Contract', amount: 175000, deliveryTime: '30 Days', status: 'Submitted' }
      ];
      setBidsDB(defaultBids);
      localStorage.setItem('vb_bids_db', JSON.stringify(defaultBids));
    }

    // Load active session
    const sessionToken = sessionStorage.getItem('vb_jwt_token');
    const sessionUser = sessionStorage.getItem('vb_current_user');
    if (sessionToken && sessionUser) {
      setCurrentUser(JSON.parse(sessionUser));
      setView('DASHBOARD');
    }
  }, []);

  const showToast = (message: string, type: 'success' | 'info' | 'error' = 'success') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 4000);
  };

  const handleUsersUpdate = (updatedList: UserAccount[]) => {
    setUsersDB(updatedList);
    localStorage.setItem('vb_users_db', JSON.stringify(updatedList));
  };

  const handleRfqsUpdate = (updatedList: RFQItem[]) => {
    setRfqsDB(updatedList);
    localStorage.setItem('vb_rfqs_db', JSON.stringify(updatedList));
  };

  const handleRequisitionsUpdate = (updatedList: RequisitionItem[]) => {
    setRequisitionsDB(updatedList);
    localStorage.setItem('vb_reqs_db', JSON.stringify(updatedList));
  };

  const handleBidsSubmit = (newBid: BidProposal, updatedRfqs: RFQItem[]) => {
    const updatedBids = [newBid, ...bidsDB];
    setBidsDB(updatedBids);
    localStorage.setItem('vb_bids_db', JSON.stringify(updatedBids));

    setRfqsDB(updatedRfqs);
    localStorage.setItem('vb_rfqs_db', JSON.stringify(updatedRfqs));
  };

  const handleLoginSuccess = (user: UserAccount) => {
    setCurrentUser(user);
    setView('DASHBOARD');
    showToast(`Welcome back, ${user.name}! Successfully authenticated.`, 'success');
  };

  const handleSignupSuccess = (user: UserAccount) => {
    const updated = [...usersDB, user];
    handleUsersUpdate(updated);

    if (user.status === 'Pending') {
      showToast('Account registered successfully! Registration is pending Admin approval.', 'info');
      setView('LOGIN');
    } else {
      const mockJWTHeader = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
      const mockJWTPayload = btoa(JSON.stringify({ sub: user.email, name: user.name, role: user.role }));
      const token = `${mockJWTHeader}.${mockJWTPayload}.mock_sig`;

      sessionStorage.setItem('vb_jwt_token', token);
      sessionStorage.setItem('vb_current_user', JSON.stringify(user));

      setCurrentUser(user);
      setView('DASHBOARD');
      showToast(`Welcome to VendorBridge, ${user.name}! Account created and authenticated.`, 'success');
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('vb_jwt_token');
    sessionStorage.removeItem('vb_current_user');
    setCurrentUser(null);
    setView('LOGIN');
    showToast('Logged out securely. Session ended.', 'info');
  };

  return (
    <>
      {view === 'DASHBOARD' && currentUser ? (
        <DashboardPage
          currentUser={currentUser}
          onLogout={handleLogout}
          usersDB={usersDB}
          rfqsDB={rfqsDB}
          requisitionsDB={requisitionsDB}
          bidsDB={bidsDB}
          onUsersUpdate={handleUsersUpdate}
          onRfqsUpdate={handleRfqsUpdate}
          onRequisitionsUpdate={handleRequisitionsUpdate}
          onBidsSubmit={handleBidsSubmit}
          showToast={showToast}
        />
      ) : (
        <AuthPage
          view={view === 'DASHBOARD' ? 'LOGIN' : view}
          onViewChange={(v) => setView(v)}
          onLoginSuccess={handleLoginSuccess}
          onSignupSuccess={handleSignupSuccess}
          usersDB={usersDB}
          showToast={showToast}
        />
      )}

      {toast && <Toast message={toast.message} />}
    </>
  );
}

export default App;
