import { createSlice } from '@reduxjs/toolkit'

interface CoreState {
    ready: boolean,
    resourceLoaded: boolean
}

const initialState: CoreState = {
    ready: false,
    resourceLoaded: false
}

export const coreSlice = createSlice({
    name: 'core',
    initialState,
    reducers: {
        ready: (state) => {
            state.ready = true;
        },
        resourceLoaded: (state) => {
            state.resourceLoaded= true;
        }
    },
})

export const { ready, resourceLoaded } = coreSlice.actions

export default coreSlice.reducer
