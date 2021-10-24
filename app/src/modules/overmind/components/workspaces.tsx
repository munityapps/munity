import { useGetWorkspacesQuery } from "../../workspaces/slice";
import { Workspace } from '../../workspaces/slice';



const OvermindWorkspaces = () => {
	const { data, error, isFetching, isLoading } = useGetWorkspacesQuery();
	return <div className="p-grid p-mt-2">
		{
			data?.map((workspace: Workspace) =>
				<div key={workspace.slug} className="p-col">
					<div className="box">{workspace.slug}</div>
				</div>
			)
		}
	</div>;
}

export default OvermindWorkspaces;