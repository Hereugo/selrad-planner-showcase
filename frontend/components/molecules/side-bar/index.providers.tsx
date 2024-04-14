import React, { createContext, useContext, useState } from "react";
import { DateRange } from "react-day-picker";

// the type of the value
interface FiltersContextProps {
  calendarRange: DateRange | undefined;
  setCalendarRange: React.Dispatch<React.SetStateAction<DateRange | undefined>>;
  searchQuery: string | undefined;
  setSearchQuery: React.Dispatch<React.SetStateAction<string | undefined>>;
  workId: string | undefined;
  setWorkId: React.Dispatch<React.SetStateAction<string | undefined>>;
  managerId: string | undefined;
  setManagerId: React.Dispatch<React.SetStateAction<string | undefined>>;
}

interface FiltersProviderProps {
  children: React.ReactNode;
}

const FiltersContext = createContext<FiltersContextProps>(
  {} as FiltersContextProps,
);

const useFiltersContext = (): FiltersContextProps => {
  return useContext(FiltersContext);
};
export default useFiltersContext;

export const FiltersProvider = ({ children }: FiltersProviderProps) => {
  // set states here
  const [calendarRange, setCalendarRange] = useState<DateRange | undefined>();
  const [searchQuery, setSearchQuery] = useState<string | undefined>();
  const [workId, setWorkId] = useState<string | undefined>();
  const [managerId, setManagerId] = useState<string | undefined>();

  return (
    <FiltersContext.Provider
      // pass states here
      value={{
        calendarRange,
        setCalendarRange,
        searchQuery,
        setSearchQuery,
        workId,
        setWorkId,
        managerId,
        setManagerId,
      }}
    >
      {children}
    </FiltersContext.Provider>
  );
};
