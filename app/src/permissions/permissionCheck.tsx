// Libs
import React, { useEffect } from 'react';
import { useHistory, useLocation } from 'react-router';
import { } from 'react-router';
import jwtDecode from 'jwt-decode';

// Tooling
import { useAppDispatch, useAppSelector } from '../hooks';

// Redux
import { useGetUsersQuery, User, UserRoleWorkspace } from '../user/slice';
import { logout, refreshToken, setAccessGranted, setCurrentUser } from '../authentication/slice';
import { addNotification } from '../notifications/slice';

// Components
const PermissionCheck: React.FC<{
    children: object,
    loadingWorkspace: React.FC
}> = props => {
    const dispatch = useAppDispatch();

    // isReady is redux ready and api url set
    const { JWTaccess, JWTrefresh, currentUser, accessGranted } = useAppSelector((state) => state.authentication);
    const { data: users, error: errorGetUsers } = useGetUsersQuery();

    const location = useLocation();
    const history = useHistory();

    // check if we can get users
    useEffect(() => {
        if (errorGetUsers) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot access',
                options: {
                    draggable: true
                }
            }));
            dispatch(logout());
        }
    }, [errorGetUsers, dispatch]);

    // first, set current user when we get users
    useEffect(() => {
        if (JWTaccess && users) {
            console.log('Searching user');
            const jwtData: { exp: string, jti: string, token_type: string, user_id: string } = jwtDecode(JWTaccess);
            const user: User | null = users.results.find((u: User) => {
                return u.id === jwtData.user_id
            }) || null;
            if (user) {
                dispatch(setCurrentUser(user));
            } else {
                dispatch(addNotification({
                    type: 'error',
                    message: 'error:user_cannot_access',
                    options: {
                        draggable: true
                    }
                }));
                dispatch(logout());
            }
        }
    }, [users, JWTaccess, dispatch]);

    // second, permission check
    useEffect(() => {
        if (currentUser) {
            // check if current user has access
            console.log('Cheking if user has access ', currentUser);
            if (currentUser) {
                // case 1 : user is a superuser or a staff member
                if (currentUser.is_superuser || currentUser.has_overmind_access) {
                    // do nothing, he is a great guy!
                    dispatch(setAccessGranted(true));
                    return;
                }

                // case 2 : user has no workspace, disconnect!
                if (currentUser.user_role_workspaces.length === 0) {
                    dispatch(addNotification({
                        type: 'error',
                        message: 'Logging out, access to nothing'
                    }))
                    dispatch(logout());
                    return;
                }
                const pathname = location.pathname;
                const re = new RegExp('/workspace/([^/]+)');
                const result = pathname.match(re);

                const redirectToFirstWorkspace = () => {
                    // history.push(`/workspace/${currentUser.user_role_workspaces[0].workspace}`)
                    window.location.href = (`${window.location.protocol}//${window.location.host}/workspace/${currentUser.user_role_workspaces[0].workspace}`);
                }

                // case 3 : A user is on overmind, need to redirect
                if (result === null) {
                    redirectToFirstWorkspace();
                    return;
                }

                const currentWorkspace = result[1];
                // case 4 : check if user has access to workspace
                if (undefined === currentUser.user_role_workspaces.find((ws_role: UserRoleWorkspace) =>
                    ws_role.workspace === currentWorkspace
                )
                ) {
                    redirectToFirstWorkspace();
                    return;
                }

                // case 5 : User is on his workspace => nice!
                dispatch(setAccessGranted(true));
            }
        }
    }, [
        users,
        errorGetUsers,
        dispatch,
        currentUser,
        history,
        location.pathname
    ]);

    // finally we set the refresh token routune
    useEffect(() => {
        if (accessGranted) {
            dispatch(refreshToken({refresh:JWTrefresh}));
            setInterval(() => dispatch(refreshToken({refresh:JWTrefresh})), 10 * 60 * 1000);
        }
    }, [accessGranted, dispatch]);

    if (!accessGranted) return <props.loadingWorkspace />;

    return <>{props.children}</>
}

export default PermissionCheck;

