import React, { createContext, useContext, useState } from 'react';
import { DateRange } from 'react-day-picker';

// the type of the value
interface FiltersContextProps {
    calendarRange: DateRange | undefined;
    setCalendarRange: React.Dispatch<React.SetStateAction<DateRange | undefined>>;
}

interface FiltersProviderProps {
    children: React.ReactNode;
}

const FiltersContext = createContext<FiltersContextProps>({} as FiltersContextProps);

const useFiltersContext = (): FiltersContextProps => {
    return useContext(FiltersContext);
};
export default useFiltersContext;

export const FiltersProvider = ({ children }: FiltersProviderProps) => {
    // set states here
    const [calendarRange, setCalendarRange] = useState<DateRange | undefined>();

    return (
        <FiltersContext.Provider
            // pass states here
            value={{
                calendarRange,
                setCalendarRange,
            }}
        >
            {children}
        </FiltersContext.Provider>
    );
};
