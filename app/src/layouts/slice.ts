import { createSlice } from '@reduxjs/toolkit'

export interface LayoutState {
    navbarColor?: string,
    navbarColorText?: string,
    primaryColor?: string,
    primaryColorText?: string,
    secondaryColor?: string,
    boxShadow?: string,
    textColor?: string,
    secondaryColorText?: string,
    contentPadding?: string,
    inlineSpacing?: string,
    surfaceA?: string,
    surfaceB?: string,
    surfaceC?: string,
    surfaceD?: string,
    errorColor?: string,
    validColor?: string,
}

const initialState: LayoutState = {
    // Button, Input border
    navbarColor: '#661A94',
    navbarColorText: 'white',
    primaryColor: '#FCC535',
    primaryColorText: '#222',
    // Button over
    secondaryColor: '#FCC535',
    secondaryColorText: '#333',
    // Input text
    textColor: 'black',
    contentPadding: '1rem',
    inlineSpacing: '0.5rem',
    surfaceA: '#ffffff',
    surfaceB: '#faf9f8',
    surfaceC: '#f3f2f1',
    surfaceD: '#edebe9',
    errorColor: '#ef9a9a',
    validColor: '#54b358',
}

export const layoutSlice = createSlice({
    name: 'layout',
    initialState: initialState,
    reducers: {
    },
})

export default layoutSlice.reducer

