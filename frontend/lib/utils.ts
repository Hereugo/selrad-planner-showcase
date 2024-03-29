import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function managerFullName(manager: Manager) {
  return `${manager.first_name} ${manager.last_name}`;
}

export function managerShortName(manager: Manager) {
  return `${manager.first_name} ${manager.last_name[0]}.`;
}

export const formatClientName = (name: string) => {
  return name
    .replaceAll('"', " ")
    .replaceAll("'", " ")
    .replace(/\s+/g, " ")
    .trim();
};
