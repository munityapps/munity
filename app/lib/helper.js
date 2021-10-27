export var getDefaultAPIUrl = function () {
    var apiUrl = localStorage.getItem('munity_api_url');
    if (!apiUrl) {
        apiUrl = window.location.protocol + "//api." + window.location.hostname + "/v1/";
        localStorage.setItem('munity_api_url', apiUrl);
    }
    return apiUrl;
};
