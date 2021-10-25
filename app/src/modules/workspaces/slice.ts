import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../../store'
import { getDefaultAPIUrl } from '../../helper';

export interface Workspace {
    slug: string,
    db_connection: string
}

export const workspaceSlice = createApi({
    reducerPath: 'workspace',
    baseQuery: fetchBaseQuery({
        baseUrl: getDefaultAPIUrl(),
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
        getWorkspaces: builder.query<{count: number, results: Workspace[]}, void>({
            query: () => {
                return {
                    url:`/workspaces/`,
                }
            },
            providesTags: (result, error, args) =>
                result && result.count > 0
                    ? [...result.results.map(({ slug}) => ({ type: 'Workspace' as const, slug})), 'Workspace']
                    : ['Workspace'],
        }),
        getWorkspace: builder.query<Workspace, string>({
            query: slug => {
                return {
                    url:`/workspaces/${slug}/`,
                }
            },
            providesTags: (result, error, slug) => [{ type: 'Workspace', slug}],
        }),
        createWorkspace: builder.mutation<Workspace, Partial<Workspace>>({
            query: body => {
                return {
                    url: `/workspaces/`,
                    method: 'POST',
                    body
                }
            },
            invalidatesTags: () => [{ type: 'Workspace' }],
        }),
        updateWorkspace: builder.mutation<Workspace, Partial<Workspace> & Pick<Workspace, 'slug'>>({
            query: body => {
                return {
                    url: `/workspaces/${body.slug}/`,
                    method: 'PATCH',
                    body
                }
            },
            invalidatesTags: () => [{ type: 'Workspace' }],
        }),
        deleteWorkspace: builder.mutation<void, string>({
            query: slug => {
                return {
                    url: `/workspaces/${slug}/`,
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

