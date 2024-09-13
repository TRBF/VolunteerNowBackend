export function success(object : any) {
    return {"success": true, "result": object}
}
export function fail(reason : string) {
    return {"success": false, "error": reason}
}