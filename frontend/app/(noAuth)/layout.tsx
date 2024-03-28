import '../globals.css';
import type { Metadata } from 'next';
import Providers from '../providers';
import { FC } from 'react';

export const metadata: Metadata = {
    title: 'Планировщик Login',
};

interface RootLayoutProps {
    children: React.ReactNode;
}

const RootLayout: FC<RootLayoutProps> = ({ children }) => {
    return (
        <html lang="ru">
            <body>
                <Providers>{children}</Providers>
            </body>
        </html>
    );
};

export default RootLayout;
