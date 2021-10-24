import { createSlice } from '@reduxjs/toolkit'

interface Perm {
	role: string,
	action: string,
	filter: object
}

interface PermissionState {
	perms: Array<Perm>
}

const initialState: PermissionState = {
    perms: []
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

