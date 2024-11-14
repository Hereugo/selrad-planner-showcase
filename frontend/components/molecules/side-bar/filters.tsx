import SearchFilters from "./filters-search";
import CalendarFilters from "./filters-calendar";
import { Separator } from "@/components/ui/separator";
import WorkFilter from "./filters-workitem";
import ManagerFilter from "./filters-manager";
import { useMeQuery } from "@/lib/backend/users";

const Filters = () => {
  const { data: me } = useMeQuery();

  return (
    <div className="flex flex-col gap-4">
      <div className="font-semibold text-center">Фильтры</div>

      <SearchFilters />

      <Separator orientation="horizontal" />

      <CalendarFilters />

      {!me?.data.is_accountant && (
        <>
          <Separator orientation="horizontal" />

          <ManagerFilter />

          <WorkFilter />
        </>
      )}
    </div>
  );
};

export default Filters;
