import { createSlice } from '@reduxjs/toolkit'

interface Perm {
	role: string,
	action: string,
	filter: object
}

const initialState: PermissionState = {
    perms: []
}

export interface PermissionState {
	perms: Array<Perm>
}

export const permissionSlice = createSlice({
    name: 'permission',
    initialState,
    reducers: {
        setPerms: (state, action) => {
            state.perms = action.payload.perms;
        }
    }
})

export const { setPerms } = permissionSlice.actions

export default permissionSlice.reducer

