interface Plan {
    id: string;
    assigned_date: string;
    worklist: Work[];
    client: Client;
    shipment_cost: string;
    comment: string;
    managers: Manager[];
    box_count: string;

    created_at: string;
    updated_at: string;
}
