import { useMutation } from '@tanstack/react-query';
import urls from '../urls';
import axios from 'axios';

interface AuthUser {
    username: string;
    password: string;
}

interface AuthResponse {
    access: string;
    refresh: string;
}

/**
 * Allows users to login
 */
export const useLoginUserMutation = () => {
    const url = urls.auth_api.create;
    const call = ({ username, password }: AuthUser) =>
        axios.post<AuthResponse>(url, {
            username,
            password,
        });

    return useMutation(call, {});
};
