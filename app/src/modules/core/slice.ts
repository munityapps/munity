import { createSlice } from '@reduxjs/toolkit'

interface CoreState {
    isReady: boolean,
    loading: boolean,
    resourceLoaded: boolean,
    primaryColor?: string,
    primaryColorText?: string,
    secondaryColor?: string,
    boxShadow?: string,
    textColor?: string,
    textColorSecondary?: string,
    contentPadding?: string,
    inlineSpacing?: string,
    surfaceA?: string,
    surfaceB?: string,
    surfaceC?: string,
    surfaceD?: string,
    errorColor?: string,
    validColor?: string,
}

const initialState: CoreState = {
    isReady: false,
    loading: false,
    resourceLoaded: false,
//     primaryColor: '#999999',
//     primaryColorText: '#121212',
//     secondaryColor: '#555',
//     textColor: 'rgba(255, 255, 255, 0.87)',
//     textColorSecondary: 'rgba(255, 255, 255, 0.9)',
//     contentPadding: '1rem',
//     inlineSpacing: '0.5rem',
//     surfaceA: '#1e1e1e',
//     surfaceB: '#121212',
//     surfaceC: 'hsla(0, 0%, 100%, .04)',
//     surfaceD: 'hsla(0,0%,100%,.12)',
//     errorColor: '#ef9a9a',
//     validColor: '#333',
    primaryColor: 'rgb(250, 170, 65)',
    primaryColorText: '#333',
    secondaryColor: 'rgb(197, 122, 23)',
    textColor: '#323130',
    textColorSecondary: '$605e5c',
    contentPadding: '1rem',
    inlineSpacing: '0.5rem',
    surfaceA: '#ffffff',
    surfaceB: '#faf9f8',
    surfaceC: '#f3f2f1',
    surfaceD: '#edebe9',
    errorColor: '#ef9a9a',
    validColor: '#54b358',
}

export const coreSlice = createSlice({
    name: 'core',
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

export const { ready, resourceLoaded } = coreSlice.actions

export default coreSlice.reducer
