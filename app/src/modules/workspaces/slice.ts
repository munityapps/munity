import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../../store'

export interface Workspace {
    uuid: string,
    slug: string,
}

export const workspaceSlice = createApi({
    reducerPath: 'workspace',
    baseQuery: fetchBaseQuery({
        baseUrl: `/`,
        prepareHeaders: (headers:Headers, { getState }) => {
            const token = (getState() as RootState).auhentication.access;
            if (token) {
                headers.set('authorization', `Bearer ${token}`)
            }
            return headers;
        }
    }),
    tagTypes: ['Workspace'],
    endpoints: builder => ({
        getWorkspaces: builder.query<Workspace[], void>({
            query: () => {
                return {
                    url:`/workspaces`,
                }
            },
            providesTags: (result, error, args) =>
                result
                    ? [...result.map(({ uuid }) => ({ type: 'Workspace' as const, uuid })), 'Workspace']
                    : ['Workspace'],
        }),
        getWorkspace: builder.query<Workspace, number>({
            query: uuid => {
                return {
                    url:`/workspaces/${uuid}`,
                }
            },
            providesTags: (result, error, uuid) => [{ type: 'Workspace', uuid }],
        }),
        createWorkspace: builder.mutation<Workspace, Partial<Workspace>>({
            query: args => {
                return {
                    url: `/workspaces`,
                    method: 'POST',
					args
                }
            },
            invalidatesTags: () => [{ type: 'Workspace' }],
        }),
        updateWorkspace: builder.mutation<Workspace, Partial<Workspace> & Pick<Workspace, 'uuid'>>({
            query: args => {
                return {
                    url: `/workspaces/${args.uuid}`,
                    method: 'PATCH',
					args
                }
            },
            invalidatesTags: () => [{ type: 'Workspace' }],
        }),
        deleteWorkspace: builder.mutation<void, number>({
            query: uuid => {
                return {
                    url: `/workspaces/${uuid}`,
                    method: 'DELETE'
                }
            }
        }),
    })
})

// Export the auto-generated hook for the `getPost` query endpoint
export const {
    useGetWorkspacesQuery,
    useGetWorkspaceQuery,
	useDeleteWorkspaceMutation,
	useUpdateWorkspaceMutation,
	useCreateWorkspaceMutation,
} = workspaceSlice

