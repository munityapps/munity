import { Button } from "primereact/button";
import { Divider } from "primereact/divider";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faUserEdit, faUserPlus } from "@fortawesome/free-solid-svg-icons";
import { useDeleteUserMutation, useGetUsersQuery, User } from "./slice";


const UserList = (props:{setEditUser:Function}) => {
    const { data: users } = useGetUsersQuery();
    const [deleteUser ] = useDeleteUserMutation();

    return <div>
        {users?.results.map((user: User) =>
            <div>
                <div key={user.id}>{user.username}</div>
                <Button className="p-button" onClick={() => props.setEditUser(user)}><FontAwesomeIcon icon={faUserEdit} /></Button>
                <Button className="p-button" onClick={() => deleteUser(user.id)}><FontAwesomeIcon icon={faTrash} /></Button>
            </div>
        )}
        <Divider />
        <Button className="p-button" onClick={() => props.setEditUser(null)}><FontAwesomeIcon icon={faUserPlus} />&nbsp;Create new user</Button>
    </div>;
}


export default UserList;
