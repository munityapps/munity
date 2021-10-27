import { createSlice } from '@reduxjs/toolkit';
var initialState = {
    notif: null
};
export var coreSlice = createSlice({
    name: 'notifications',
    initialState: initialState,
    reducers: {
        addNotification: function (state, action) {
            state.notif = action.payload;
        },
    }
});
export var addNotification = coreSlice.actions.addNotification;
export default coreSlice.reducer;
