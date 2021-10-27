import { createSlice } from '@reduxjs/toolkit'

export interface AppState {
    isReady: boolean,
    loading: boolean,
    resourceLoaded: boolean
}

const initialState: AppState = {
    isReady: false,
    loading: false,
    resourceLoaded: false
}

export const appSlice = createSlice({
    name: 'app',
    initialState,
    reducers: {
        ready: (state) => {
            state.isReady = true
        },
        resourceLoaded: (state) => {
            state.resourceLoaded= true;
        }
    },
})

export const { ready, resourceLoaded } = appSlice.actions

export default appSlice.reducer
