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
export var userSlice = createApi({
    reducerPath: 'user',
    baseQuery: fetchBaseQuery({
        baseUrl: localStorage.getItem('munity_api_url') || getDefaultAPIUrl(),
        prepareHeaders: function (headers, _a) {
            var getState = _a.getState;
            var token = getState().auhentication.access;
            if (token) {
                headers.set('authorization', "Bearer " + token);
            }
            return headers;
        }
    }),
    tagTypes: ['User'],
    endpoints: function (builder) { return ({
        getUsers: builder.query({
            query: function () {
                return {
                    url: "/users/",
                };
            },
            providesTags: function (result) {
                return result && result.count > 0
                    ? __spreadArray(__spreadArray([], result.results.map(function (_a) {
                        var id = _a.id;
                        return ({ type: 'User', id: id });
                    }), true), [
                        { type: 'User', id: 'LIST' },
                    ], false) : [{ type: 'User', id: 'LIST' }];
            }
        }),
        getUser: builder.query({
            query: function (id) {
                return {
                    url: "/users/" + id + "/",
                };
            },
            providesTags: function (result, error, id) { return [{ type: 'User', id: id }]; },
        }),
        createUser: builder.mutation({
            query: function (body) {
                return {
                    url: "/users/",
                    method: 'POST',
                    body: body
                };
            },
            invalidatesTags: function () { return [{ type: 'User' }]; },
        }),
        updateUser: builder.mutation({
            query: function (body) {
                return {
                    url: "/users/" + body.id + "/",
                    method: 'PATCH',
                    body: body
                };
            },
            invalidatesTags: function (result, error, arg) { return [{ type: 'User', id: arg.id }]; },
        }),
        deleteUser: builder.mutation({
            query: function (id) {
                return {
                    url: "/users/" + id + "/",
                    method: 'DELETE'
                };
            },
            invalidatesTags: function () { return [{ type: 'User' }]; },
        }),
    }); }
});
// Export the auto-generated hook for the `getPost` query endpoint
export var useGetUsersQuery = userSlice.useGetUsersQuery, useGetUserQuery = userSlice.useGetUserQuery, useDeleteUserMutation = userSlice.useDeleteUserMutation, useUpdateUserMutation = userSlice.useUpdateUserMutation, useCreateUserMutation = userSlice.useCreateUserMutation;
