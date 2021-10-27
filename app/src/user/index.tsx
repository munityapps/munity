import LayoutDispatcher from "../layouts/LayoutDispatcher";
import { UserForm } from "./form";
import { User } from "./slice";
import { useState } from "react";
import UserList from "./list";


const Users = () => {

    const [editUser, setEditUser] = useState<User | null>(null);

    return <LayoutDispatcher
        layoutName="TwoColumns"
        mainSlot={ <UserForm user={editUser}/> }
        rightPanelSlot={<UserList setEditUser={setEditUser}/>}
    />;
}


export default Users;