import { UserForm } from "./form";
import { User } from "./slice";
import { useState } from "react";
import UserList from "./list";


const Users = () => {

    const [editUser, setEditUser] = useState<User | null>(null);

    return <div className="layout-two-columns">
        <UserForm user={editUser}/>
        <UserList setEditUser={setEditUser}/>
    </div>;
}


export default Users;