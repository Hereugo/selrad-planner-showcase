interface Client {
    id: string;
    name: string;
    created_at: string;
    updated_at: string;
    address: {
        id: number;
        street: string;
        lon: string;
        lat: string;
        created_at: string;
        updated_at: string;
    };
}
