import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../store'
import { getDefaultAPIUrl } from '../helper';
import { Workspace } from '../workspaces/slice';
import { createSlice } from '@reduxjs/toolkit';

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
    username: string,
    workspace: Workspace | null
}

export interface UserState {
    userInEdition: User | null
}

export const initialState: UserState = {
    userInEdition: null
}

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setUserInEdition: (state, payload:{payload:User|null}) => {
            state.userInEdition = payload.payload;
        }
    }
});

export const userAPISlice = createApi({
    reducerPath: 'userAPI',
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

export default userSlice.reducer;
export const { setUserInEdition } = userSlice.actions

export const {
    useGetUsersQuery,
    useGetUserQuery,
    useDeleteUserMutation,
    useUpdateUserMutation,
    useCreateUserMutation,
} = userAPISlice

