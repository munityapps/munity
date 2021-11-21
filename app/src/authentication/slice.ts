import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import axios from 'axios';
import { addNotification } from '../notifications/slice';
import { User } from '../user/slice';

export interface AuthenticateState {
    pending: boolean,
    JWTaccess: string | null,
    JWTrefresh: string | null,
    currentUser: User | null,
    accessGranted: boolean
}

const initialState: AuthenticateState = {
    pending: false,
    currentUser: null,
    accessGranted: false,
    JWTaccess: localStorage.getItem('access_token') || '',
    JWTrefresh: localStorage.getItem('refresh_token') || ''
}

export const authenticate = createAsyncThunk(
    'authenticate',
    async (args: {username:string, password:string}, {dispatch}) => {
        try {
            // return {
            //     access_token: 'access_token',
            //     refresh_token: 'refresh_token'
            // }
            const response = await axios.post('/auth/jwt/create/', args);
            return {
                JWTaccess: response.data.access,
                JWTrefresh: response.data.refresh
            };
        } catch (err: unknown) {
            if (typeof err === "string") {
                dispatch(addNotification({
                    type: 'error',
                    message: err,
                    options: {
                        draggable: true
                    }
                }))
            } else if (err instanceof Error) {
                dispatch(addNotification({
                    type: 'error',
                    message: 'errors:cannot_login',
                    options: {
                        draggable: true
                    }
                }))
            }
            throw err;
        }
    }
);

export const permissionSlice = createSlice({
    name: 'authentication',
    initialState,
    reducers: {
        logout: (state) => {
            state.JWTaccess = null;
            state.JWTrefresh = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        },
        setAccessGranted: (state, payload:{payload:boolean}) => {
            state.accessGranted= payload.payload;
        },
        setCurrentUser: (state, payload:{payload:User|null}) => {
            state.currentUser = payload.payload;
        },
    },
    extraReducers: builder => {
        builder.addCase(authenticate.pending, (state, action) => {
            state.pending = true
        })
        builder.addCase(authenticate.rejected, (state, action) => {
            state.pending = false
        })
        builder.addCase(authenticate.fulfilled, (state, action) => {
            state.pending = false
            state.JWTaccess = action.payload.JWTaccess
            state.JWTrefresh = action.payload.JWTrefresh
            localStorage.setItem('access_token', action.payload.JWTaccess);
            localStorage.setItem('refresh_token', action.payload.JWTrefresh);
        })
    }
});

export const { logout, setCurrentUser, setAccessGranted } = permissionSlice.actions

export default permissionSlice.reducer
