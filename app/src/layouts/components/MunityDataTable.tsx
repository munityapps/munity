import { Button } from 'primereact/button';
import { DataTable, DataTableFilterMeta, DataTableProps } from 'primereact/datatable';
import { InputText } from 'primereact/inputtext';
import React, { ChangeEvent, MouseEventHandler, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import './MunityDataTable.scss';

const MunityDataTable : React.FunctionComponent<DataTableProps & {createNew:MouseEventHandler<HTMLButtonElement>}> = props => {
    const [filters, setFilters] = useState(props.filters);
    const [globalFilter, setGlobalFilter] = useState("");
    const { t } = useTranslation();

    const onGlobalFilterChange = (e:ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        const _filters:DataTableFilterMeta = {...filters};
        if(_filters.global) {
            _filters['global'] = { value: value, matchMode: "contains" }
            setFilters(_filters);
            setGlobalFilter(value);
        }
    }

    const initFilters = () => {
        setFilters({
            ...props.filters,
            'global': {
                value: null,
                matchMode: "contains"
            }
        });
        setGlobalFilter("");
    }

    useEffect(() => {
        initFilters();
    }, [])

    const header = <div className="p-d-flex p-jc-between">
        <div>
            <Button type="button" icon="pi pi-plus" label="Nouveau" className="p-button" onClick={props.createNew} />
            &nbsp;
            <Button type="button" icon="pi pi-filter-slash" label={t('app:remove_filters')} className="p-button-outlined" onClick={initFilters} />
        </div>
        <span className="p-input-icon-left">
            <i className="pi pi-search" />
            <InputText value={globalFilter} onChange={onGlobalFilterChange} placeholder={t('app:keyword_search')} />
        </span>
    </div>
    return <DataTable
        value={props.value}
        className={`${props.className} munity-datatable`}
        dataKey={props.dataKey}
        filters={filters}
        filterDisplay={props.filterDisplay}
        globalFilterFields={props.globalFilterFields}
        header={header}
        emptyMessage={props.emptyMessage}
    >
        {props.children}
    </DataTable>;
};

export default MunityDataTable;