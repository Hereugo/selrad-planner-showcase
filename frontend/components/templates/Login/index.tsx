import UserAuthForm from './user-auth-form';
import { CalendarDays } from 'lucide-react';

const LoginTemplate = () => {
    return (
        <>
            <div className="container relative grid h-screen flex-col items-center justify-center lg:max-w-none lg:grid-cols-2 lg:px-0">
                <div className="relative hidden h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex">
                    <div className="absolute inset-0 bg-red-900" />
                    <div className="relative z-20 flex items-center text-lg font-medium">
                        <CalendarDays className="mr-2 h-8 w-8" />
                        Планировщик
                    </div>
                </div>
                <div className="lg:p-8">
                    <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
                        <div className="flex flex-col space-y-2 text-center">
                            <h1 className="text-2xl font-semibold tracking-tight">Вход</h1>
                            <p className="text-sm text-muted-foreground">Войдите в свой аккаунт</p>
                        </div>
                        <UserAuthForm />
                        <p className="px-8 text-center text-sm text-muted-foreground">
                            {`Нажимая на кнопку "Войти", вы соглашаетесь с нашими
                            правилами и условиями. Правда пока у нас их нет, но
                            скоро будут. Поэтому лучше согласитесь. Пожалуйста.`}
                        </p>
                    </div>
                </div>
            </div>
        </>
    );
};

export default LoginTemplate;
