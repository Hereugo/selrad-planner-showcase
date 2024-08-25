interface WorkItem {
  id: string;
  name: string;
  description: string;
  statuses: TaskStatus[];
  created_at: string;
  updated_at: string;
}
