"use client";

import { cn } from "@/lib/utils";
import { useViewFeature } from "@/lib/hooks/useViewFeature";
import { FileDown, List, MapPinnedIcon, Settings, Wallet } from "lucide-react";
import Link from "next/link";

const NavigationLinks = () => {
  const viewFeature = useViewFeature();

  return (
    <div className="flex flex-col gap-2">
      <Link
        href="/"
        className={cn(
          "flex items-center gap-2 p-2 hover:bg-gray-100 rounded-md duration-100",
        )}
      >
        <List className="w-6 h-6" /> Планы
      </Link>
      <Link
        href="/maps"
        className={cn(
          "flex items-center gap-2 p-2 hover:bg-gray-100 rounded-md duration-100",
          viewFeature.canViewMaps ? "" : "hidden",
        )}
      >
        <MapPinnedIcon className="w-6 h-6" /> Карта
      </Link>
      <Link
        href="/export_excel"
        className={cn(
          "flex items-center gap-2 p-2 hover:bg-gray-100 rounded-md duration-100",
        )}
      >
        <FileDown className="w-6 h-6" /> Скачать эксель
      </Link>
      <Link
        href="/payments"
        className={cn(
          "flex items-center gap-2 p-2 hover:bg-gray-100 rounded-md duration-100",
          viewFeature.canViewPaymnetRegistry ? "" : "hidden",
        )}
      >
        <Wallet className="w-6 h-6" /> Выплаты
      </Link>
      <Link
        href="/settings"
        className={cn(
          "flex items-center gap-2 p-2 hover:bg-gray-100 rounded-md duration-100",
          viewFeature.canViewSettings ? "" : "hidden",
        )}
      >
        <Settings className="w-6 h-6" /> Настройки
      </Link>
    </div>
  );
};

export default NavigationLinks;
