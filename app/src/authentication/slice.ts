import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import axios from 'axios';
import { addNotification } from '../notifications/slice';
import { User } from '../user/slice';

export interface AuthenticateState {
    pending: boolean,
    access: string | null,
    refresh: string | null,
    currentUser: User | null
}

const initialState: AuthenticateState = {
    pending: false,
    currentUser: null,
    access: localStorage.getItem('access_token') || '',
    refresh: localStorage.getItem('refresh_token') || ''
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
                access: response.data.access,
                refresh: response.data.refresh
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
            state.access = null;
            state.refresh = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
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
            state.access = action.payload.access
            state.refresh = action.payload.refresh
            localStorage.setItem('access_token', action.payload.access);
            localStorage.setItem('refresh_token', action.payload.refresh);
        })
    }
});

export const { logout, setCurrentUser } = permissionSlice.actions

export default permissionSlice.reducer
