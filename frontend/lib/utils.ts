import { type ClassValue, clsx } from "clsx";
import { DateRange } from "react-day-picker";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function toTitle(s: string) {
  return s[0].toUpperCase() + s.slice(1).toLowerCase();
}

// todo: remove
export function managerFullName(manager: Manager) {
  return toTitle(manager.name);
}

// todo: remove
export function managerShortName(manager: Manager) {
  return toTitle(manager.name);
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

export function decodeContentDisposition(encodedString: string) {
  // Extract encoding type and encoded filename
  const matches = encodedString.match(/=\?([^?]+)\?(b|B)\?([^?]+)\?=/);
  if (!matches || matches.length !== 4) {
    return null; // Invalid input
  }

  const encoding = matches[1];
  const encodedFilename = matches[3];

  // Decode the filename based on the encoding type
  let decodedFilename = "";
  if (encoding.toLowerCase() === "utf-8") {
    decodedFilename = decodeURIComponent(escape(window.atob(encodedFilename)));
  } else {
    // Add support for other encodings if needed
    return null; // Unsupported encoding
  }

  return decodedFilename;
}

export const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

export function calendarRangeDuration(range: DateRange | undefined) {
  if (!range) return 1e6;
  if (!range.from && !range.to) return 1e6;
  if (!range.from || !range.to) return 0;
  const days = Math.ceil(
    (range.to.getTime() - range.from.getTime()) / (1000 * 60 * 60 * 24),
  );
  return days;
}

export const formatDateBackend = (date: Date | undefined) => {
  return date?.toLocaleDateString("ru-RU").split(".").reverse().join("-");
};

export const isPlanAReturn = (plan: Plan) => {
  return plan.work_items.some((item) => item.content_type === "Return");
};
export const isPlanAShipment = (plan: Plan) => {
  return plan.work_items.some((item) => item.content_type === "Shipment");
};
