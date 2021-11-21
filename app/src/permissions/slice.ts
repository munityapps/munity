import { sliceFactory } from '../factory/slice';

export interface Ressource {
    id: number,
    app_mode: string,
    label: string,
}

export interface Permission {
	id: string,
	action: string,
	ressource: Ressource
}

export interface Role {
	id: string,
	name: string,
	permissions: Permission[]
}

export const roleAPISlice = sliceFactory<Role>({
    reducerName: 'roleAPI',
    endpoint: '/roles/',
    name: 'Role'
});


export const {
    useGetRolesQuery,
    useGetRoleQuery,
    useDeleteRoleMutation,
    useUpdateRoleMutation,
    useCreateRoleMutation,
} = roleAPISlice
