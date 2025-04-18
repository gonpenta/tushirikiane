import { I_GetWorkSpaceMemberResponse } from "./interfaces/responses";

export const M_People: I_GetWorkSpaceMemberResponse[] = [
  {
    id: "1",
    created_at: "2025-04-01T10:00:00Z",
    updated_at: "2025-04-01T10:00:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-1",
      email: "alice.smith@example.com",
      first_name: "Alice",
      last_name: "Smith",
      middle_name: "Marie",
    },
  },
  {
    id: "2",
    created_at: "2025-04-01T10:05:00Z",
    updated_at: "2025-04-01T10:05:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-2",
      email: "bob.jones@example.com",
      first_name: "Bob",
      last_name: "Jones",
      middle_name: "Alexander",
    },
  },
  {
    id: "3",
    created_at: "2025-04-01T10:10:00Z",
    updated_at: "2025-04-01T10:10:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-3",
      email: "carla.mendez@example.com",
      first_name: "Carla",
      last_name: "Mendez",
      middle_name: "Lucia",
    },
  },
  {
    id: "4",
    created_at: "2025-04-01T10:15:00Z",
    updated_at: "2025-04-01T10:15:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-4",
      email: "daniel.cho@example.com",
      first_name: "Daniel",
      last_name: "Cho",
      middle_name: "Hyun",
    },
  },
  {
    id: "5",
    created_at: "2025-04-01T10:20:00Z",
    updated_at: "2025-04-01T10:20:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-5",
      email: "emma.white@example.com",
      first_name: "Emma",
      last_name: "White",
      middle_name: "Grace",
    },
  },
  {
    id: "6",
    created_at: "2025-04-01T10:25:00Z",
    updated_at: "2025-04-01T10:25:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-6",
      email: "frank.nguyen@example.com",
      first_name: "Frank",
      last_name: "Nguyen",
      middle_name: "Bao",
    },
  },
  {
    id: "7",
    created_at: "2025-04-01T10:30:00Z",
    updated_at: "2025-04-01T10:30:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-7",
      email: "grace.kim@example.com",
      first_name: "Grace",
      last_name: "Kim",
      middle_name: "Yuna",
    },
  },
  {
    id: "8",
    created_at: "2025-04-01T10:35:00Z",
    updated_at: "2025-04-01T10:35:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-8",
      email: "hugo.fernandez@example.com",
      first_name: "Hugo",
      last_name: "Fernandez",
      middle_name: "Luis",
    },
  },
  {
    id: "9",
    created_at: "2025-04-01T10:40:00Z",
    updated_at: "2025-04-01T10:40:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-9",
      email: "isabelle.lee@example.com",
      first_name: "Isabelle",
      last_name: "Lee",
      middle_name: "Min",
    },
  },
  {
    id: "10",
    created_at: "2025-04-01T10:45:00Z",
    updated_at: "2025-04-01T10:45:00Z",
    workspace_id: "ws-123",
    member: {
      id: "u-10",
      email: "jack.thompson@example.com",
      first_name: "Jack",
      last_name: "Thompson",
      middle_name: "Ray",
    },
  },
];

export const M_Tasks = [
  { id: 1, title: "Complete project report", isDone: false },
  { id: 2, title: "Review pull requests", isDone: true },
  { id: 3, title: "Update documentation", isDone: false },
  { id: 4, title: "Fix UI bugs", isDone: true },
  { id: 5, title: "Prepare for meeting", isDone: false },
  { id: 6, title: "Refactor authentication logic", isDone: true },
  { id: 7, title: "Write unit tests", isDone: false },
  { id: 8, title: "Optimize database queries", isDone: true },
  { id: 9, title: "Create onboarding guide", isDone: false },
  { id: 10, title: "Deploy new feature", isDone: true },
];
