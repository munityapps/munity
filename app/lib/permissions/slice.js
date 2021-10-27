import { createSlice } from '@reduxjs/toolkit';
var initialState = {
    perms: []
};
export var permissionSlice = createSlice({
    name: 'permission',
    initialState: initialState,
    reducers: {
        setPerms: function (state, action) {
            state.perms = action.payload.perms;
        }
    }
});
export var setPerms = permissionSlice.actions.setPerms;
export default permissionSlice.reducer;
