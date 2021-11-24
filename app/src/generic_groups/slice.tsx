import { Workspace } from 'munityapps/workspaces/slice';
import { createSlice } from '@reduxjs/toolkit';
import { sliceFactory } from 'munityapps/factory/slice';

export interface GenericGroup {
    created: Date,
    id: string,
    label: String,
    modified: Date,
    workspace: Workspace | null
}

export interface GenericGroupState {
    generic_groupInEdition: GenericGroup | null
}

export const initialState: GenericGroupState = {
    generic_groupInEdition: null
}

export const generic_groupSlice = createSlice({
    name: 'generic_group',
    initialState,
    reducers: {
        setGenericGroupInEdition: (state, payload:{payload:GenericGroup|null}) => {
            state.generic_groupInEdition = payload.payload;
        }
    }
});

export const generic_groupAPISlice = sliceFactory<GenericGroup>({
    reducerName: 'generic_groupAPI',
    endpoint: '/generic_groups/',
    name: 'GenericGroup'
});


export default generic_groupSlice.reducer;
export const { setGenericGroupInEdition } = generic_groupSlice.actions

export const {
    useGetGenericGroupsQuery,
    useGetGenericGroupQuery,
    useDeleteGenericGroupMutation,
    useUpdateGenericGroupMutation,
    useCreateGenericGroupMutation,
} = generic_groupAPISlice