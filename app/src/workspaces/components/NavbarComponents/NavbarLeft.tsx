import logo from '../../../assets/logo.png';
import { Button } from 'primereact/button';
import { useAppSelector } from '../../../hooks';

import { useHistory } from 'react-router';
import { useGetWorkspacesQuery } from '../../slice';

const NavbarLeft = () => {
    const history = useHistory();
    const workspace_slug = useAppSelector((state) => state.app.workspace_slug);
    const { data: workspaces } = useGetWorkspacesQuery();
    return <div className="left-part p-d-flex p-ai-center">
        <Button onClick={() => history.push(`/workspace/${workspace_slug}`)} className="p-button-link">
            <img src={logo} alt="logo" />
        </Button>
        <div className="workspace_name">{workspaces?.results.find(w => w.slug === workspace_slug)?.name}</div>
    </div>;
}

export default NavbarLeft;