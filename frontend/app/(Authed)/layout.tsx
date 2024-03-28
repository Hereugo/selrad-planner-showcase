import type { Metadata } from "next";
import "../globals.css";
import Providers from "../providers";
import TopBar from "@/components/molecules/top-bar";
import SideBar from "@/components/molecules/side-bar";

export const metadata: Metadata = {
    title: "Планировщик",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="ru">
            <body>
                <Providers>
                    <TopBar className="w-screen h-16 fixed top-0 left-0" />
                    <SideBar className="w-64 h-full fixed top-16 left-0" />
                    <div className="ml-64 mt-16 p-4 h-[calc(100vh-4rem)] overflow-y-auto">
                        {children}
                    </div>
                </Providers>
            </body>
        </html>
    );
}
