import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../store'

export interface Setting {
    key: string,
    valye: string
}

// const initialState: SettingsState = {
// //     primaryColor: '#999999',
// //     primaryColorText: '#121212',
// //     secondaryColor: '#555',
// //     textColor: 'rgba(255, 255, 255, 0.87)',
// //     secondaryColorText: 'rgba(255, 255, 255, 0.9)',
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
//     secondaryColorText: '$605e5c',
//     contentPadding: '1rem',
//     inlineSpacing: '0.5rem',
//     surfaceA: '#ffffff',
//     surfaceB: '#faf9f8',
//     surfaceC: '#f3f2f1',
//     surfaceD: '#edebe9',
//     errorColor: '#ef9a9a',
//     validColor: '#54b358',
// }

export const settingSlice = createApi({
    reducerPath: 'settings',
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
    tagTypes: ['Setting'],
    endpoints: builder => ({
        getSettings: builder.query<Setting[], void>({
            query: () => {
                return {
                    url:`/settings`,
                }
            },
            providesTags: (result, error, arg) =>
                result
                    ? [...result.map(({ key }) => ({ type: 'Setting' as const, key })), 'Setting']
                    : ['Setting'],
        }),
        getSetting: builder.query<Setting, number>({
            query: key=> {
                return {
                    url:`/settings/${key}`,
                }
            },
            providesTags: (result, error, key) => [{ type: 'Setting', key}],

        }),
        createSetting: builder.mutation<Setting, Partial<Setting>>({
            query: args => {
                return {
                    url: `/settings`,
                    method: 'POST',
                    args
                }
            },
            invalidatesTags: () => [{ type: 'Setting' }],
        }),
        updateSetting: builder.mutation<Setting, Partial<Setting> & Pick<Setting, 'key'>>({
            query: args => {
                return {
                    url: `/settings/${args.key}`,
                    method: 'PATCH',
                    args
                }
            },
            invalidatesTags: (result, error, arg) => [{ type: 'Setting', uuid: arg.key}],
        }),
        deleteSetting: builder.mutation<void, number>({
            query: key => {
                return {
                    url: `/settings/${key}`,
                    method: 'DELETE'
                }
            },
            invalidatesTags: () => [{ type: 'Setting' }],
        }),
    })
})

// Export the auto-generated hook for the `getPost` query endpoint
export const {
    useGetSettingsQuery,
    useGetSettingQuery,
    useDeleteSettingMutation,
    useUpdateSettingMutation,
    useCreateSettingMutation,
} = settingSlice
