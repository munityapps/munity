import { sliceFactory } from '../factory/slice';

export interface File {
    id: string,
    name: string,
    type: string,
    size: number,
    file: string,
    workspace: string|null,
    created: Date,
    modified: Date,
}

export const fileAPISlice = sliceFactory<File>({
    reducerName: 'fileAPI',
    endpoint: '/files/',
    name: 'File'
});


export const {
    useGetFilesQuery,
    useGetFileQuery,
    useDeleteFileMutation,
    useUpdateFileMutation,
    useCreateFileMutation,
} = fileAPISlice
