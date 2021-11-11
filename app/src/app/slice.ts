import { createSlice } from '@reduxjs/toolkit'

export interface AppState {
    isReady: boolean,
    loading: boolean,
    resourceLoaded: boolean,
    workspace_slug: string | null
}

const initialState: AppState = {
    isReady: false,
    loading: false,
    resourceLoaded: false,
    workspace_slug: null
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
        },
        setWorkspace: (state, ws_slug) => {
            state.workspace_slug = ws_slug.payload;
        }
    }
})

export const { ready, resourceLoaded, setWorkspace } = appSlice.actions

export default appSlice.reducer
