import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

const SearchFilters = () => {
    return (
        <div className="flex">
            <Input
                placeholder="Поиск"
                className="rounded-r-none focus-visible:ring-0"
            />
            <Button className="w-12 p-2 rounded-l-none">
                <Search className="w-4 h-4" />
            </Button>
        </div>
    )
}

export default SearchFilters;