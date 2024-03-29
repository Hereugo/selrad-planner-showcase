interface Client {
    pk: string;
    name: string;
    created_at: string;
    updated_at: string;
    address: {
        pk: number;
        street: string;
        lon: string;
        lat: string;
        created_at: string;
        updated_at: string;
    }
}