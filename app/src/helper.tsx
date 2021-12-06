export const getAPIUrl = () => {
    return `${window.location.protocol}//api.${window.location.hostname}/v1`;
}

export const getURLForFile= (filePath:string) => {
    return `${window.location.protocol}//api.${window.location.hostname}${filePath}`;
}

export const getWorkspaceEndpoint = (endpoint:string) => {
    const pathname = window.location.pathname;
    const re = new RegExp('/workspace/([^/]+)');
    const result = pathname.match(re);
    const workspace = result ? result[1] : null;
    if (workspace) {
        return `/workspaces/${workspace}${endpoint}`
    } else {
        return endpoint;
    }
}
