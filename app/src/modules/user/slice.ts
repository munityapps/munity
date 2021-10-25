import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../../store'
import { getDefaultAPIUrl } from '../../helper';

export interface User {
    created: Date,
    email: string,
    first_name: string,
    generic_groups: string[],
    id: string,
    is_superuser: boolean,
    last_name: string,
    modified: Date,
    roles: string[],
    username: string
}

export const userSlice = createApi({
    reducerPath: 'user',
    baseQuery: fetchBaseQuery({
        baseUrl: localStorage.getItem('munity_api_url') || getDefaultAPIUrl(),
        prepareHeaders: (headers:Headers, { getState }) => {
            const token = (getState() as RootState).auhentication.access;
            if (token) {
                headers.set('authorization', `Bearer ${token}`)
            }
            return headers;
        }
    }),
    tagTypes: ['User'],
    endpoints: builder => ({
        getUsers: builder.query<{count: number, results: User[]}, void>({
            query: () => {
                return {
                    url:`/users/`,
                }
            },
            providesTags: (result) =>
                result && result.count > 0
                ? [
                    ...result.results.map(({ id }) => ({ type: 'User' as const, id })),
                    { type: 'User', id: 'LIST' },
                    ]
                : [{ type: 'User', id: 'LIST' }]
        }),
        getUser: builder.query<User, number>({
            query: id => {
                return {
                    url:`/users/${id}/`,
                }
            },
            providesTags: (result, error, id) => [{ type: 'User', id }],

        }),
        createUser: builder.mutation<User, Partial<User>>({
            query: body => {
                return {
                    url: `/users/`,
                    method: 'POST',
                    body
                }
            },
            invalidatesTags: () => [{ type: 'User' }],
        }),
        updateUser: builder.mutation<User, Partial<User> & Pick<User, 'id'>>({
            query: body => {
                return {
                    url: `/users/${body.id}/`,
                    method: 'PATCH',
                    body
                }
            },
            invalidatesTags: (result, error, arg) => [{ type: 'User', id: arg.id }],
        }),
        deleteUser: builder.mutation<void, string>({
            query: id => {
                return {
                    url: `/users/${id}/`,
                    method: 'DELETE'
                }
            },
            invalidatesTags: () => [{ type: 'User' }],
        }),
    })
})

// Export the auto-generated hook for the `getPost` query endpoint
export const {
    useGetUsersQuery,
    useGetUserQuery,
    useDeleteUserMutation,
    useUpdateUserMutation,
    useCreateUserMutation,
} = userSlice
