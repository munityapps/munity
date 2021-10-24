import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../../store'

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
        baseUrl: `http://api.localhost/v1/`,
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
                    url:`/users`,
                }
            },
            // providesTags: (result, error, arg) => {
            //     console.log(result);
            //     return result
            //         ? [result.results.map(({ id }) => ({ type: 'User' as const, id })), 'User']
            //         : ['User']
            // }
        }),
        getUser: builder.query<User, number>({
            query: id => {
                return {
                    url:`/users/${id}`,
                }
            },
            providesTags: (result, error, id) => [{ type: 'User', id }],

        }),
        createUser: builder.mutation<User, Partial<User>>({
            query: args => {
                return {
                    url: `/users`,
                    method: 'POST',
                    args
                }
            },
            invalidatesTags: () => [{ type: 'User' }],
        }),
        updateUser: builder.mutation<User, Partial<User> & Pick<User, 'id'>>({
            query: args => {
                return {
                    url: `/users/${args.id}`,
                    method: 'PATCH',
                    args
                }
            },
            invalidatesTags: (result, error, arg) => [{ type: 'User', id: arg.id }],
        }),
        deleteUser: builder.mutation<void, number>({
            query: id => {
                return {
                    url: `/users/${id}`,
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
