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

export function formatPrice(price: number | undefined) {
  if (!price && price !== 0) return undefined;

  const sign = "₸";
  const priceStr = price.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ");
  return `${priceStr} ${sign}`;
}

export function parsePriceFormula(formula: string) {
  if (!formula) return "0";

  formula = formula.replace(/[^0-9\+\.]/g, ""); // remove all non-numeric characters except "+" and "."
  formula = formula.replace(/\++/g, "+"); // replace multiple "+" with single "+"
  if (formula.startsWith("+")) formula = formula.slice(1);
  formula = formula
    .split("+")
    .map((x) => parseInt(x) || "")
    .join("+"); // parse integers and join with "+"
  return formula;
}
