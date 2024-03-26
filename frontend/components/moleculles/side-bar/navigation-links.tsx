import { FileDown, List, MapPinnedIcon } from "lucide-react";
import Link from "next/link";

const NavigationLinks = () => {
    return (
        <div className="flex flex-col gap-2">
            <Link href="/" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded-md duration-100">
                <List className="w-6 h-6" /> Планы
            </Link>
            <Link href="/maps" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded-md duration-100">
                <MapPinnedIcon className="w-6 h-6" /> Карта
            </Link>
            <Link href="/export_excel" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded-md duration-100">
                <FileDown className="w-6 h-6" /> Скачать эксель
            </Link>
        </div>
    )
}

export default NavigationLinks;