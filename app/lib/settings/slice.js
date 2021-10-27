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
// const initialState: SettingsState = {
// //     primaryColor: '#999999',
// //     primaryColorText: '#121212',
// //     secondaryColor: '#555',
// //     textColor: 'rgba(255, 255, 255, 0.87)',
// //     textColorSecondary: 'rgba(255, 255, 255, 0.9)',
// //     contentPadding: '1rem',
// //     inlineSpacing: '0.5rem',
// //     surfaceA: '#1e1e1e',
// //     surfaceB: '#121212',
// //     surfaceC: 'hsla(0, 0%, 100%, .04)',
// //     surfaceD: 'hsla(0,0%,100%,.12)',
// //     errorColor: '#ef9a9a',
// //     validColor: '#333',
//     primaryColor: 'rgb(250, 170, 65)',
//     primaryColorText: '#333',
//     secondaryColor: 'rgb(197, 122, 23)',
//     textColor: '#323130',
//     textColorSecondary: '$605e5c',
//     contentPadding: '1rem',
//     inlineSpacing: '0.5rem',
//     surfaceA: '#ffffff',
//     surfaceB: '#faf9f8',
//     surfaceC: '#f3f2f1',
//     surfaceD: '#edebe9',
//     errorColor: '#ef9a9a',
//     validColor: '#54b358',
// }
export var settingSlice = createApi({
    reducerPath: 'settings',
    baseQuery: fetchBaseQuery({
        baseUrl: "/",
        prepareHeaders: function (headers, _a) {
            var getState = _a.getState;
            var token = getState().auhentication.access;
            if (token) {
                headers.set('authorization', "Bearer " + token);
            }
            return headers;
        }
    }),
    tagTypes: ['Setting'],
    endpoints: function (builder) { return ({
        getSettings: builder.query({
            query: function () {
                return {
                    url: "/settings",
                };
            },
            providesTags: function (result, error, arg) {
                return result
                    ? __spreadArray(__spreadArray([], result.map(function (_a) {
                        var key = _a.key;
                        return ({ type: 'Setting', key: key });
                    }), true), ['Setting'], false) : ['Setting'];
            },
        }),
        getSetting: builder.query({
            query: function (key) {
                return {
                    url: "/settings/" + key,
                };
            },
            providesTags: function (result, error, key) { return [{ type: 'Setting', key: key }]; },
        }),
        createSetting: builder.mutation({
            query: function (args) {
                return {
                    url: "/settings",
                    method: 'POST',
                    args: args
                };
            },
            invalidatesTags: function () { return [{ type: 'Setting' }]; },
        }),
        updateSetting: builder.mutation({
            query: function (args) {
                return {
                    url: "/settings/" + args.key,
                    method: 'PATCH',
                    args: args
                };
            },
            invalidatesTags: function (result, error, arg) { return [{ type: 'Setting', uuid: arg.key }]; },
        }),
        deleteSetting: builder.mutation({
            query: function (key) {
                return {
                    url: "/settings/" + key,
                    method: 'DELETE'
                };
            },
            invalidatesTags: function () { return [{ type: 'Setting' }]; },
        }),
    }); }
});
// Export the auto-generated hook for the `getPost` query endpoint
export var useGetSettingsQuery = settingSlice.useGetSettingsQuery, useGetSettingQuery = settingSlice.useGetSettingQuery, useDeleteSettingMutation = settingSlice.useDeleteSettingMutation, useUpdateSettingMutation = settingSlice.useUpdateSettingMutation, useCreateSettingMutation = settingSlice.useCreateSettingMutation;
