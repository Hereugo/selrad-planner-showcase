import { useToast } from '@/components/ui/use-toast';
import { useLoginUserMutation } from '@/lib/backend/auth';
import { FormEvent, useEffect } from 'react';

export const useUserAuth = () => {
	const { toast } = useToast();

	const loginMutation = useLoginUserMutation();

	async function onFormSubmit(event: FormEvent<HTMLFormElement>) {
		event.preventDefault();

		loginMutation.mutate({
			username: event.currentTarget['username'].value,
			password: event.currentTarget['password'].value,
		});
	}

	// throw toast if login mutation failed
	useEffect(() => {
		if (loginMutation.isError) {
			toast({
				title: 'Произошла ошибка',
				description: 'Проверьте правильность введенных данных',
				duration: 3000,
			});
		}
	}, [loginMutation.isError, toast]);

	// throw toast if login mutation success
	useEffect(() => {
		if (loginMutation.isSuccess) {
			toast({
				title: 'Успешно',
				description: 'Вы успешно авторизовались',
				duration: 2000,
			});

			const { access, refresh } = loginMutation.data.data;

			localStorage.setItem('access', access);
			localStorage.setItem('refresh', refresh);

			window.location.href = '/';
		}
	}, [loginMutation.isSuccess, loginMutation.data?.data, toast]);

	return { onFormSubmit, isLoading: loginMutation.isLoading };
};
