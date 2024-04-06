"use client";

import { FC, useEffect, useState } from "react";
import { Check, ChevronsUpDown, MapPin } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { useClients } from "./index.hooks";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface ClientPickerProps {
  id?: string;
  setClient: (client: string) => void;
}

const filterFunc = (value: string, search: string) => {
  return Number(
    search.split(" ").reduce((acc, word) => {
      return acc && value.toLowerCase().includes(word.toLowerCase());
    }, true),
  );
};

const ClientPicker: FC<ClientPickerProps> = ({ id, setClient }) => {
  const [open, setOpen] = useState<boolean>(false);
  const [value, setValue] = useState<string>("");

  const { clients } = useClients();

  useEffect(() => {
    setClient(value);
  }, [value]);

  return (
    <>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            id={id}
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className={cn(
              "w-full justify-between font-normal",
              !value && "text-muted-foreground",
            )}
          >
            {value
              ? clients.find((client) => client.id === value)?.name
              : "Выбрать клиента..."}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[29rem] max-w-[calc(100vw-3rem)] p-0 shadow-md">
          <Command filter={filterFunc}>
            <CommandInput placeholder="Найти клиента..." />
            <CommandEmpty>Клиент не найден</CommandEmpty>
            <CommandGroup className="h-96 overflow-y-scroll">
              {clients.map((client) => (
                <CommandItem
                  className="cursor-pointer"
                  key={client.id}
                  title={client.addresses[0].street || ""}
                  onSelect={() => {
                    setValue(client.id === value ? "" : client.id);
                    setOpen(false);
                  }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      value === client.id ? "opacity-100" : "opacity-0",
                    )}
                  />
                  {client.name}
                </CommandItem>
              ))}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </Popover>
      {value && (
        <div className="mt-2">
          <Label htmlFor="address">Адрес</Label>
          <Button
            disabled
            variant="outline"
            id="address"
            className={cn(
              "w-full justify-between font-normal",
              !value && "text-muted-foreground",
            )}
            title={
              clients.find((client) => client.id === value)?.addresses[0]
                .street ?? ""
            }
          >
            <span className="text-start truncate w-[25rem] max-w-[calc(100vw-8rem)]">
              {clients.find((client) => client.id === value)?.addresses[0]
                .street ?? ""}
            </span>
            <MapPin className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </div>
      )}
    </>
  );
};

export default ClientPicker;
