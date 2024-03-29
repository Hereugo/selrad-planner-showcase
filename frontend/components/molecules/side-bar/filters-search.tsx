"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, SearchXIcon } from "lucide-react";
import useFiltersContext from "./index.providers";
import { cn } from "@/lib/utils";

const SearchFilters = () => {
    const { searchQuery, setSearchQuery } = useFiltersContext();

    return (
        <div className="flex">
            <Input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Поиск"
                className="rounded-r-none focus-visible:ring-0"
            />
            <Button
                className={cn("w-12 p-2 rounded-l-none", searchQuery && "bg-red-500 hover:bg-red-400")}
                onClick={() => setSearchQuery("")}
            >
                {
                    searchQuery ?
                        <SearchXIcon className="w-4 h-4" /> :
                        <Search className="w-4 h-4" />
                }
            </Button>
        </div>
    )
}

export default SearchFilters;