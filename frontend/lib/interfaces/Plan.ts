interface Plan {
    id: string;
    assigned_date: string;
    work_items: WorkItem[];
    client: Client;
    shipment_cost: number;
    shipment_cost_formula: string;
    comment: string;
    managers: Manager[];
    box_count: number;

    invoice_date: string | null;
    accountant_comment: string;

    created_at: string;
    updated_at: string;
}
