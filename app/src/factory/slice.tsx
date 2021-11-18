import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../store'
import { getDefaultAPIUrl } from '../helper';

export interface SliceFactory {
    reducerName: string,
    endpoint: string,
    name: string,
}

export interface GenericModel {
    id: string
}

export function sliceFactory<Model extends GenericModel>({ reducerName, endpoint, name }: SliceFactory):any {
    return createApi({
        reducerPath: reducerName,
        baseQuery: fetchBaseQuery({
            baseUrl: getDefaultAPIUrl(),
            prepareHeaders: (headers: Headers, { getState }) => {
                const token = (getState() as RootState).authentication.access;
                if (token) {
                    headers.set('authorization', `Bearer ${token}`)
                }
                return headers;
            }
        }),
        tagTypes: [name],
        endpoints: builder => ({
            [`get${name}s`]: builder.query<{count: number, results:Model[]}, void>({
                query: () => {
                    return {
                        url: endpoint,
                    }
                },
                providesTags: (result, error, arg) =>
                    result && result.count > 0
                        ? [...result.results.map(({id}) => ({ type: name, id})), name]
                        : [name],
            }),
            [`get${name}`]: builder.query<Model, number>({
                query: id => {
                    return {
                        url: `${endpoint}${id}/`,
                    }
                },
                providesTags: (result, error, id) => [{ type: name, id}],

            }),
            [`create${name}`]: builder.mutation<Model, Partial<Model>>({
                query: args => {
                    return {
                        url: endpoint,
                        method: 'POST',
                        body: args
                    }
                },
                invalidatesTags: () => [{ type: name }],
            }),
            [`update${name}`]: builder.mutation<Model, Partial<Model>>({
                query: args => {
                    return {
                        url: `${endpoint}${args.id}/`,
                        method: 'PATCH',
                        body:args
                    }
                },
                invalidatesTags: (result, error, arg) => [{ type: name, uuid: arg.id}],
            }),
            [`delete${name}`]: builder.mutation<void, number>({
                query: id => {
                    return {
                        url: `${endpoint}${id}/`,
                        method: 'DELETE'
                    }
                },
                invalidatesTags: () => [{ type: name }],
            }),
        })
    });
}
