// Libs
import React from 'react';
import ReactDOM from 'react-dom';
import { Route } from 'react-router';
import { Provider as ReduxProvider } from 'react-redux'

// Component
import MunityApp from './app';
import Providers from './providers';
import Navbar from './workspaces/components/Navbar';
import LoadingMunity from './layouts/components/LoadingMunity';
import NavbarLeft from './workspaces/components/NavbarComponents/NavbarLeft';
import NavbarCenter from './workspaces/components/NavbarComponents/NavbarCenter';
import NavbarRight from './workspaces/components/NavbarComponents/NavbarRight';
import OvermindSidebar from './overmind/components/Sidebar';
import OvermindNavbar from './overmind/components/Navbar';
import OvermindNavbarLeft from './overmind/components/NavbarComponents/NavbarLeft';
import OvermindNavbarCenter from './overmind/components/NavbarComponents/NavbarCenter';
import OvermindNavbarRight from './overmind/components/NavbarComponents/NavbarRight';

// Configuration
import reportWebVitals from './reportWebVitals';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';


// Style
import './styles.scss';
import logo from './assets/logo.png';

import store from './store';

ReactDOM.render(
    <ReduxProvider store={store}>
        <Providers>
            <React.StrictMode>
                <MunityApp
                    workspaceNavbar={<Navbar
                        leftPart={NavbarLeft}
                        centerPart={NavbarCenter}
                        rightPart={NavbarRight}
                    />}
                    overmindNavbar={<OvermindNavbar
                        leftPart={OvermindNavbarLeft}
                        centerPart={OvermindNavbarCenter}
                        rightPart={OvermindNavbarRight}
                    />}
                    overmindSidebar={<OvermindSidebar newMenuButton={[
                        // <div className="menu">
                        //     <Button className="p-button-link ">
                        //         Integration 2
                        //     </Button>
                        // </div>
                    ]}/>}
                    newOvermindRoutes={[
                        <Route key={'foobar'} path="/foobar" component={() => <>OVERMIND FOOBAR</>} />
                    ]}
                    newWorkspaceRoutes={[
                        <Route key={'foobar'} path="/workspace/:workspace_slug/foobar" component={() => <>WORKSPACE FOOBAR</>} />
                    ]}
                    loadingWorkspace={LoadingMunity}
                    logoLogin={logo}
                >
                    {/* Custom routes */}
                </MunityApp>
            </React.StrictMode>
        </Providers>
    </ReduxProvider>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
serviceWorkerRegistration.register();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
