import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function toTitle(s: string) {
  return s[0].toUpperCase() + s.slice(1).toLowerCase();
}

export function managerFullName(manager: Manager) {
  let out = toTitle(manager.first_name);

  if (manager.last_name) {
    out += " " + toTitle(manager.last_name);
  }

  return out;
}

export function managerShortName(manager: Manager) {
  let out = toTitle(manager.first_name);

  if (manager.last_name) {
    let initials = manager.last_name[0].toUpperCase();
    out += ` ${initials}.`;
  }

  return out;
}

export const formatClientName = (name: string) => {
  return name
    .replaceAll('"', " ")
    .replaceAll("'", " ")
    .replace(/\s+/g, " ")
    .trim();
};
