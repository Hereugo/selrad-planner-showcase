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

export const isClientSkif = (client: Client) => {
  const clientName = client.name.toLowerCase();
  return clientName.includes("скиф");
};

export const invoiceNumberWord = (invoiceCount: number) => {
  if (invoiceCount === 1) {
    return "НАКЛАДНАЯ";
  } else if (invoiceCount > 1 && invoiceCount < 5) {
    return "НАКЛАДНЫЕ";
  } else {
    return "НАКЛАДНЫХ";
  }
};

export const generateAccountantComment = ({
  isReturn,
  isShipment,
  hasManager,
  invoiceSum,
  invoiceCount,
  client,
}: {
  isReturn: boolean;
  isShipment: boolean;
  invoiceSum: number;
  hasManager: boolean;
  invoiceCount: number;
  client?: Client;
}) => {
  let comment = "";

  // 1) Поле бух комментариев появляется только когда есть - Отгрузка, Возврат или оба
  if (!isReturn && !isShipment) {
    return comment;
  }

  // 2) Когда сумма отгрузки > 0 то пишется «1 НАКЛАДНАЯ»
  // 3) Если сумма отгрузки написана как «Х + Y» то есть 2 и более числа, то пишется «2 НАКЛАДНЫЕ» итд.
  if (invoiceSum > 0) {
    comment += `${invoiceCount} ${invoiceNumberWord(invoiceCount)}. `;
  }

  // 4) Любой клиент кроме Скифа, пишется «АДМИРАЛ», если Скиф «СЕЛРАД».
  if (client) {
    const isSkif = isClientSkif(client);
    const companyName = isSkif ? "СЕЛРАД" : "АДМИРАЛ";
    comment += `${companyName}. `;
  }
  // 5) Если есть возврат и указан менеджер то в коментах пишется «ДОВЕРЕННОСТЬ».
  if (isReturn && hasManager) {
    comment += "ДОВЕРЕННОСТЬ. ";
  }

  // Вообщем комментарий выглядит вот так если все выполняется по максу «2 НАКЛАДНЫЕ.АДМИРАЛ.ДОВЕРЕННОСТЬ.»
  return comment;
};

export const isPlanOld = (plan: Plan) => {
  return plan.assigned_date < new Date().toISOString().slice(0, 10);
};
