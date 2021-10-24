import { useParams } from "react-router";
import LayoutDispatcher from "../core/components/LayoutDispatcher";
import Navbar from "../layouts/components/Navbar";
import { useGetUsersQuery, User } from "../user/slice";

const Workspace = () => {
    let { workspace_slug } = useParams<{workspace_slug: string}>();

    const {data} = useGetUsersQuery();

    console.log(data?.results);

    return <LayoutDispatcher
        layoutName="LayoutNavbar2Columns"
        navbarSlot={<Navbar workspace={workspace_slug} /> }
        mainSlot={<Navbar workspace={workspace_slug} /> }
        rightPanelSlot={<div> {data?.results.map((user:User) => <div key={user.id}>{user.username}</div>)}</div>}
        footbarSlot={<div> Footbar </div>}
    />;
}


export default Workspace;