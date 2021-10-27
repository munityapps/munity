var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { getDefaultAPIUrl } from '../helper';
export var workspaceSlice = createApi({
    reducerPath: 'workspace',
    baseQuery: fetchBaseQuery({
        baseUrl: getDefaultAPIUrl(),
        prepareHeaders: function (headers, _a) {
            var getState = _a.getState;
            var token = getState().auhentication.access;
            if (token) {
                headers.set('authorization', "Bearer " + token);
            }
            return headers;
        }
    }),
    tagTypes: ['Workspace'],
    endpoints: function (builder) { return ({
        getWorkspaces: builder.query({
            query: function () {
                return {
                    url: "/workspaces/",
                };
            },
            providesTags: function (result, error, args) {
                return result && result.count > 0
                    ? __spreadArray(__spreadArray([], result.results.map(function (_a) {
                        var slug = _a.slug;
                        return ({ type: 'Workspace', slug: slug });
                    }), true), ['Workspace'], false) : ['Workspace'];
            },
        }),
        getWorkspace: builder.query({
            query: function (slug) {
                return {
                    url: "/workspaces/" + slug + "/",
                };
            },
            providesTags: function (result, error, slug) { return [{ type: 'Workspace', slug: slug }]; },
        }),
        createWorkspace: builder.mutation({
            query: function (body) {
                return {
                    url: "/workspaces/",
                    method: 'POST',
                    body: body
                };
            },
            invalidatesTags: function () { return [{ type: 'Workspace' }]; },
        }),
        updateWorkspace: builder.mutation({
            query: function (body) {
                return {
                    url: "/workspaces/" + body.slug + "/",
                    method: 'PATCH',
                    body: body
                };
            },
            invalidatesTags: function () { return [{ type: 'Workspace' }]; },
        }),
        deleteWorkspace: builder.mutation({
            query: function (slug) {
                return {
                    url: "/workspaces/" + slug + "/",
                    method: 'DELETE'
                };
            }
        }),
    }); }
});
// Export the auto-generated hook for the `getPost` query endpoint
export var useGetWorkspacesQuery = workspaceSlice.useGetWorkspacesQuery, useGetWorkspaceQuery = workspaceSlice.useGetWorkspaceQuery, useDeleteWorkspaceMutation = workspaceSlice.useDeleteWorkspaceMutation, useUpdateWorkspaceMutation = workspaceSlice.useUpdateWorkspaceMutation, useCreateWorkspaceMutation = workspaceSlice.useCreateWorkspaceMutation;
