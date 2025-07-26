interface PaymentRegistry {
  id: string;
  date: string;
  manager: Manager;
  payment: number;
  bonus: number;
  comment: string;
  is_confirmed: boolean;
  plans: Plan[];
}
