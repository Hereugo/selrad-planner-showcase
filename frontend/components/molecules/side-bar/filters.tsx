import SearchFilters from "./filters-search";
import CalendarFilters from "./filters-calendar";
import { Separator } from "@/components/ui/separator";
import WorkFilter from "./filters-workitem";
import ManagerFilter from "./filters-manager";

const Filters = () => {
  return (
    <div className="flex flex-col gap-4">
      <div className="font-semibold text-center">Фильтры</div>

      <SearchFilters />

      <Separator orientation="horizontal" />

      <CalendarFilters />

      <Separator orientation="horizontal" />

      <ManagerFilter />

      <WorkFilter />
    </div>
  );
};

export default Filters;
