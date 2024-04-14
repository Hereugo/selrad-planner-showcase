interface Client {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
  addresses: {
    id: string;
    street: string;
    lon: number;
    lat: number;
    created_at: string;
    updated_at: string;
  }[];
}
