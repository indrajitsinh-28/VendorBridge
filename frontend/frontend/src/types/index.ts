export type UserRole = 'ADMIN' | 'PROCUREMENT' | 'MANAGER' | 'VENDOR';

export interface UserAccount {
  name: string;
  email: string;
  password?: string;
  role: UserRole;
  status: 'Active' | 'Pending';
}

export interface RFQItem {
  id: string;
  description: string;
  budget: number;
  deadline: string;
  status: 'Open' | 'Under Review' | 'Completed';
  bidsCount: number;
}

export interface RequisitionItem {
  id: string;
  requester: string;
  description: string;
  amount: number;
  status: 'Pending' | 'Approved' | 'Rejected';
}

export interface BidProposal {
  id: string;
  rfqId: string;
  rfqDesc: string;
  amount: number;
  deliveryTime: string;
  status: 'Submitted' | 'Accepted' | 'Declined';
}
