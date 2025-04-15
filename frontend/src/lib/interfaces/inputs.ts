export interface I_CreateBoardInput {
  name: string;
  description: string;
  workspace_id: string;
}

export interface I_CreatCardInput {
  name: string;
}

export interface I_EditCardInput {
  name?: string;
  notes?: string;
  description?: string;
  due_date?: string;
  position?: number;
  is_completed?: boolean;
  labels?: string[];
}

export interface I_EditChecklistInput {
  name?: string;
  is_completed?: boolean;
  assignee_id?: string;
  due_at?: string;
}

export interface I_InviteEmailsInput {
  emails: string[];
}

export interface I_AcceptBoardInviteInput {
  token: string;
}

export interface I_AcceptWorkSpaceInviteInput {
  token: string;
}

export interface I_InviteToBoardInput {
  emails: string[];
}

export interface I_InviteToWorkSpaceInput {
  emails: string[];
}

export interface I_CreateWorkSpaceInput {
  name: string;
}
