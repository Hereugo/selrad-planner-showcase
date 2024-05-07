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
