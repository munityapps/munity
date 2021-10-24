import { createSlice } from '@reduxjs/toolkit'

interface NotificationPayload {
    type: 'warning' | 'error' | 'info' | 'success',
	message: string ,
	options?: object
}

interface NotificationState {
    notif: NotificationPayload | null
}

const initialState: NotificationState= {
    notif: null
}

export const coreSlice = createSlice({
    name: 'notifications',
    initialState,
    reducers: {
        addNotification: (state:NotificationState, action: {payload:NotificationPayload, type:string}) => {
			state.notif = action.payload;
        },
    }
})

export const { addNotification } = coreSlice.actions

export default coreSlice.reducer

