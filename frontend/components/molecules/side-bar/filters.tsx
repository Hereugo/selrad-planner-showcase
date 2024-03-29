import SearchFilters from "./filters-search";
import CalendarFilters from "./filters-calendar";
import { Separator } from "@/components/ui/separator";

const Filters = () => {
  return (
    <>
      <div className="font-semibold text-center mb-2">Фильтры</div>

      <SearchFilters />

      <Separator orientation="horizontal" className="my-4" />

      <CalendarFilters />
    </>
  );
};

export default Filters;
