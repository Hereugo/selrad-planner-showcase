"use client";

import { FiltersProvider } from "@/components/molecules/side-bar/index.providers";
import { Toaster } from "@/components/ui/toaster";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { useState } from "react";

export default function Providers({ children }: { children: React.ReactNode }) {
  const [client] = useState(
    new QueryClient({
      defaultOptions: {
        queries: {
          refetchOnWindowFocus: false,
        },
      },
    }),
  );

  return (
    <QueryClientProvider client={client}>
      <FiltersProvider>{children}</FiltersProvider>
      <Toaster />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
