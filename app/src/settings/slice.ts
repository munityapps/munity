import { GenericModel, sliceFactory } from '../factory/slice';

export interface Setting extends GenericModel {
    key: string,
    valye: string
}

export const settingAPISlice = sliceFactory<Setting>({
    reducerName: 'settingsAPI',
    endpoint: '/settings/',
    name: 'Settings'
});

export const {
    useGetSettingsQuery,
    useGetSettingQuery,
    useDeleteSettingMutation,
    useUpdateSettingMutation,
    useCreateSettingMutation,
} = settingAPISlice;
