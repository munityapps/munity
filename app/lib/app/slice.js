var _a;
import { createSlice } from '@reduxjs/toolkit';
var initialState = {
    isReady: false,
    loading: false,
    resourceLoaded: false
};
export var appSlice = createSlice({
    name: 'app',
    initialState: initialState,
    reducers: {
        ready: function (state) {
            state.isReady = true;
        },
        resourceLoaded: function (state) {
            state.resourceLoaded = true;
        }
    },
});
export var ready = (_a = appSlice.actions, _a.ready), resourceLoaded = _a.resourceLoaded;
export default appSlice.reducer;
