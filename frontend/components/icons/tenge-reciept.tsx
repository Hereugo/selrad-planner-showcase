import { cn } from '@/lib/utils';
import { FC } from 'react';

interface TengeRecieptProps {
    className?: string;
}

export const TengeReciept: FC<TengeRecieptProps> = ({ ...props }) => {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={cn('lucide lucide-receipt', props['className'])}
        >
            <path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z" />
            <path d="M12 17.5v-8" />
            <path d="M8 9.5h8" />
            <path d="M8 7h8" />
        </svg>
    );
};

export const TengeRecieptIcon = TengeReciept;
