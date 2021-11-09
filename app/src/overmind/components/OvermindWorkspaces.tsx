import { useState } from 'react';
import { Workspace } from '../../workspaces/slice';
import { WorkspaceForm } from "../../workspaces/form";
import WorkspaceList from '../../workspaces/list';

const OvermindWorkspaces = ()  => {
    const [editWorkspace, setEditWorkspace] = useState<Workspace | null>(null);

    return <div className="layout-basic">
        {/* <WorkspaceForm workspace={editWorkspace} /> */}
        <WorkspaceList setEditWorkspace={setEditWorkspace}/>
    </div>
}

export default OvermindWorkspaces;