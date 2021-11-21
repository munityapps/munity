import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../store'
import { getAPIUrl } from '../helper';
import { createSlice } from '@reduxjs/toolkit';

export interface Workspace {
    slug: string,
    db_connection: string
}

export interface WorkspaceState {
    workspaceInEdition: Workspace | null
}

export const initialState: WorkspaceState = {
    workspaceInEdition: null
}

export const workspaceSlice = createSlice({
    name: 'workspace',
    initialState,
    reducers: {
        setWorkspaceInEdition: (state, payload:{payload:Workspace|null}) => {
            state.workspaceInEdition= payload.payload;
        }
    }
});

export const workspaceAPISlice = createApi({
    reducerPath: 'workspaceAPI',
    baseQuery: fetchBaseQuery({
        baseUrl: getAPIUrl(),
        prepareHeaders: (headers:Headers, { getState }) => {
            const token = (getState() as RootState).authentication.JWTaccess;
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
            },
            invalidatesTags: () => [{ type: 'Workspace' }],
        }),
    })
})
export default workspaceSlice.reducer;
export const { setWorkspaceInEdition } = workspaceSlice.actions

// Export the auto-generated hooks
export const {
    useGetWorkspacesQuery,
    useGetWorkspaceQuery,
    useDeleteWorkspaceMutation,
    useUpdateWorkspaceMutation,
    useCreateWorkspaceMutation,
} = workspaceAPISlice;
